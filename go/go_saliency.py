import random
import os
import socket
import time

from absl import app, flags
from tensorflow import gfile

import numpy as np
import copy

import coords
import dual_net
import preprocessing
from go import Position, LibertyTracker
from strategies import MCTSPlayer
import math
import matplotlib.pyplot as plt
from scipy.stats import entropy
from scipy.misc.pilutil import imresize

import utils

from sgf_wrapper import replay_sgf, replay_sgf_file, translate_sgf_move, make_sgf


flags.DEFINE_string('load_file', None, 'Path to model save files.')
flags.DEFINE_string('selfplay_dir', None, 'Where to write game data.')
flags.DEFINE_string('holdout_dir', None, 'Where to write held-out game data.')
flags.DEFINE_string('sgf_dir', None, 'Where to write human-readable SGFs.')
flags.DEFINE_float('holdout_pct', 0.05, 'What percent of games to hold out.')
flags.DEFINE_float('resign_disable_pct', 0.05,
                   'What percent of games to disable resign for.')

# From strategies.py
flags.declare_key_flag('verbose')
flags.declare_key_flag('num_readouts')

save_path = 'results/'

FLAGS = flags.FLAGS
N = 19
readouts = 50

def cross_entropy_mcts(dict1, dict2, a_b):
    '''
		This function calculates cross entropy of probability distributions of actions in dict2 wrt dict1 (without considering a_b)
    '''
    P1 = [] #values of moves in dictP^dictQ wrt P
    P2 = [] #values of moves in dictP^dictQ wrt Q
    for move in dict1:
        if move is not a_b and move in dict2:
            P1.append(dict1[move])
            P2.append(dict2[move])
    P1 = np.asarray(P1)
    P2 = np.asarray(P2)
    KL = entropy(P1, P2)
    if math.isinf(KL) or math.isnan(KL):
        print("***********************", a_b, "**************")
        return -1
    print("KL ", KL)
    return (KL)/(KL + 1.)

def perturb_position(pos, new_board=None, memodict={}):
    '''
		This function returns Position of the perturbed board (new_board)
    '''
    if new_board is None:
        new_board = np.copy(pos.board)
    new_lib_tracker = LibertyTracker.from_board(new_board)
    return Position(new_board, pos.n, pos.komi, pos.caps, new_lib_tracker, pos.ko, pos.recent, pos.board_deltas, pos.to_play)

def get_mcts_player(network, pos):
    if random.random() < FLAGS.resign_disable_pct:
        resign_threshold = -1.0
    else:
        resign_threshold = None
    player = MCTSPlayer(network, resign_threshold=resign_threshold)
    player.initialize_game(position=pos)
    # Must run this once at the start to expand the root node.
    first_node = player.root.select_leaf()
    prob, val = network.run(first_node.position)
    first_node.incorporate_results(prob, val, first_node)

    # while True:
    start = time.time()
    player.root.inject_noise()
    current_readouts = player.root.N
    # we want to do "X additional readouts", rather than "up to X readouts".
    while player.root.N < current_readouts + readouts:
        player.tree_search()
    return player

def cross_entropy(policy, new_policy, best_move):
    '''
		This function calculates normalized cross entropy of new policy wrt policy (without considering best_move)
    '''
     
    p = policy[:best_move]
    p = np.append(p, policy[best_move+1:])

    new_p = new_policy[:best_move]
    new_p = np.append(new_p, new_policy[best_move+1:])
    

    KL =  entropy(p, new_p)

    K = KL/(1. + KL)

    return K

def saliency_combine(saliency, frame, blur, channel=2):
    '''
		Combines heatmaps in different channels
    '''
    pmax = saliency.max()
    S = saliency
    S -= S.min() ; S = blur*pmax * S / S.max()
    I = frame.astype('uint16')
    I[:,:,channel] += S.astype('uint16')
    I = I.clip(1,255).astype('uint8')
    return I


def play_network(network, board=None):
    '''
		Generates saliency maps of 3 methods given a board position
    '''
    pos = Position(board=board)
    original_moves = {}
    heatmap = np.zeros((N,N), dtype=np.float)
    
    policy, V = network.run(pos)
    
    best_move = np.argmax(policy)
    print("Best Move is", coords.to_gtp(coords.from_flat(best_move)))
    p = np.max(policy)
    
    player = get_mcts_player(network, pos)
    node = player.root

    old_Q = node.child_Q[best_move]

    atariV = np.zeros([N, N], dtype=np.float)
    atariP = np.zeros([N, N], dtype=np.float)
    delQ = np.zeros([N, N], dtype=np.float)
    heatmap = np.zeros([N, N], dtype=np.float)
    for i in range(N):
        for j in range(N):
            if board[i, j] == 1 or board[i, j] == -1:
                print(i, j)
                print("---------------------")

                new_board = np.copy(board)
                new_board[i, j] = 0
                new_pos = perturb_position(pos, new_board)
                new_policy, new_V = network.run(new_pos)
                new_p = new_policy[best_move]

                player = get_mcts_player(network, pos)
                node = player.root
                # print(node.describe())
                new_Q = node.child_Q[best_move]

                atariV[i, j] = 0.5*((V - new_V)**2)
                atariP[i, j] = 0.5*np.linalg.norm(policy - new_policy)
                dP = p - new_p
                
                dQ = old_Q - new_Q
                K = cross_entropy(policy, new_policy, best_move)
                if dP>0:
                    heatmap[i, j] = 2*dP/(1 + dP*K)

                if dQ>0:
                    delQ[i, j] = dQ

    atariV = (atariV - np.min(atariV))/(np.max(atariV) - np.min(atariV))
    atariP = (atariP - np.min(atariP))/(np.max(atariP) - np.min(atariP))

    # heatmap[heatmap < np.max(heatmap)/3] = 0
    # atariV[atariV < np.max(atariV)/3] = 0
    # atariP[atariP < np.max(atariP)/3] = 0
    # delQ[delQ < np.max(delQ)/3] = 0
    

    frame = np.zeros((N,N,3))
    frame = saliency_combine(atariV, frame, blur=256, channel=2)
    frame = saliency_combine(atariP, frame, blur=256, channel=0)

    plt.figure(1)
    plt.imshow(atariV, cmap = 'Reds')
    plt.colorbar()
    plt.savefig(save_path + 'atariV.png')
    plt.show()
    
    plt.figure(2)
    plt.imshow(atariP, cmap= 'Reds')
    plt.colorbar()
    plt.savefig(save_path + 'atariP.png')
    plt.show()

    plt.figure(3)
    plt.imshow(frame)
    plt.savefig(save_path + 'atari.png')
    plt.show()


    plt.figure(4)
    plt.imshow(delQ, cmap = 'Reds')
    plt.colorbar()
    plt.savefig(save_path + 'deltaQ.png')
    plt.show()

    plt.figure(5)
    plt.imshow(heatmap, cmap = 'Reds')
    plt.colorbar()
    plt.savefig(save_path + 'entropy.png')
    plt.show()

def simulate(network, board = None, steps=20):
    '''
		Simulates rollout of network for given number of steps (to help understand the tactic)
    '''
    pos = Position(board=board)
    for i in range(steps):
        policy, V = network.run(pos)
        
        best_move = np.argmax(policy)
        print('Best move', coords.to_gtp(coords.from_flat(best_move)))
        pos = pos.play_move(coords.from_flat(best_move))
        print(pos)

def play_mcts(network, board=None):
    pos = Position(board=board)

    player = get_mcts_player(network, pos)
    node = player.root
    children = node.rank_children()
    soft_n = node.child_N / max(1, sum(node.child_N))

    original_moves = {}

    heatmap = np.zeros((N, N), dtype=np.float)
    a_b = None
    for i in children:
        if node.child_N[i] == 0:
            break
        if a_b is None:
            a_b = coords.from_flat(i)
        original_moves[coords.to_gtp(coords.from_flat(i))] = soft_n[i]

    a_b = player.pick_move()
    
    # player.play_move(move)
    a_b_coords = a_b
    a_b = coords.to_gtp(a_b)

    print(original_moves)
    print("best action: ", a_b)
    print(node.position)
    p = original_moves[a_b]
    print(p)

    for i in range(N):
        for j in range(N):
            if board[i][j] == -1 or board[i][j] == 1:
                new_board = np.copy(board)
                new_board[i, j] = 0
                new_pos = perturb_position(pos, new_board)
                if new_pos.is_move_legal(a_b_coords):
                    player = get_mcts_player(network, new_pos)
                    node = player.root
                    print(node.position)
                    new_moves = {}
                    children = node.rank_children()
                    soft_n = node.child_N / max(1, sum(node.child_N))
                    for ch in children:
                        if node.child_N[ch] == 0:
                            break
                        new_moves[coords.to_gtp(coords.from_flat(ch))] = soft_n[ch]

                    new_a_b = player.pick_move()
                    # player.play_move(move)
                    new_a_b = coords.to_gtp(new_a_b)
                    # if new_a_b == 'F5':
                    print("---------------------")
                    # print("Moves: ", new_moves)    
                    if a_b in new_moves:
                        new_p = new_moves[a_b]
                    else:
                        new_p = 0.
                    print("New best move", new_a_b)
                    print("p", new_p)
                    print("------------------")

                    K = cross_entropy_mcts(original_moves, new_moves, a_b)
                    if K == -1:
                        print("index", i, j)
                        heatmap[i, j] = -1.0
                        continue
                    dP = p - new_p
                    if dP > 0:
                        heatmap[i, j] = 2.0*dP/(1. + dP*K)
                else:
                    heatmap[i, j] = -1.0

    heatmap[heatmap == -1] = np.max(heatmap)
    heatmap[heatmap<np.max(heatmap)/1.5] = 0
    plt.imshow(heatmap, cmap='jet')
    plt.colorbar()
    plt.show()
    return player


def main(argv):
    network = dual_net.DualNetwork('minigo-models/models/000737-fury')		# add path to model

    board = np.zeros([N, N], dtype=np.int8)
    # pos_w_con = list(replay_sgf_file('go_puzzles/14511/14511.sgf'))


    # pos_w_con = list(replay_sgf_file('go_puzzles/10/10.sgf'))
    # board += pos_w_con[0].position.board

    # pos_w_con = list(replay_sgf_file('go_puzzles/9225/9225.sgf'))
    # board += pos_w_con[0].position.board

    # pos_w_con = list(replay_sgf_file('go_puzzles/14571/14587.sgf'))
    # board += pos_w_con[0].position.board

    # pos_w_con = list(replay_sgf_file('go_puzzles/14054/14064.sgf'))
    # board += pos_w_con[0].position.board
    
    # pos_w_con = list(replay_sgf_file('go_puzzles/10458/7592.sgf'))
    # board += pos_w_con[0].position.board

    # pos_w_con = list(replay_sgf_file('go_puzzles/10458/10458.sgf'))
    # board += pos_w_con[0].position.board

    # pos_w_con = list(replay_sgf_file('go_puzzles/10458/10495.sgf'))
    # board += pos_w_con[0].position.board
    

    pos_w_con = list(replay_sgf_file('go_puzzles/10458/10494.sgf'))
    board += pos_w_con[0].position.board
    
    # pos_w_con = list(replay_sgf_file('go_puzzles/10458/7593.sgf'))
    # board += pos_w_con[0].position.board

    pos_w_con = list(replay_sgf_file('go_puzzles/14511/14515.sgf'))
    board += pos_w_con[0].position.board

    # pos_w_con = list(replay_sgf_file('go_puzzles/10458/7589.sgf'))
    # board += pos_w_con[0].position.board
    




    # for i in pos_w_con:
    #     print(i.position)
    # board[5, 7] = -1
    # board[6][7] = -1
    # board[8][4:6] = -1
    # board[3][8] = -1
    # board[5][3] = -1

    # board[[11,12,13],:] = 0
    pos = Position(board = board)
    # board = board + pos_w_con[0].position.board
    # print(pos)
    # board[0][3] = -1
    # board[0][4] = 1
    
    # board[1][1] = -1
    # board[1][3] = -1
    # board[1][4] = 1

    # board[2][0] = -1
    # board[2, 2] = -1
    # board[2,3:5] = 1

    # board[3, 0:2] = -1
    # board[3, [2, 4]] = 1

    # board[4, 0] = -1
    # board[4, [1, 3]] = 1

    # board[5, :3] = 1 
    
    # snap back
    # board = np.zeros([19, 19], dtype=np.int8)
    # board[0, 2] = 1
    # board[0, [5,6]] = -1
    # board[1][[1,5]] = 1
    # board[1][[2,3,4,6]] = -1
    # board[2][[0, 2,3,4,5]] = 1
    # board[[2,3], 6] = -1



    # Noise 
    # board[2,-2] = 1
    # # board[4, 11] = -1
    # board[5, 15] = 1
    # board[8, 15] = -1
    # board[10, -1] = 1
    # # board[12, 10] = -1
    # # board[12, 13] = 1
    # board[17, 16] = -1

    # board[abs(board)==1] *= -1	# to invert the board colors

    pos = Position(board = board)
    print(pos)
    # simulate(network, board, steps=10)
    play_network(network, board)

if __name__ == '__main__':
    app.run(main)
