import chess #version: 0.27.3
import chess.uci
import chess.pgn
import sys
import math
import time
import numpy as np
from collections import defaultdict
import sarfa_saliency

# load your engine:
handler = chess.uci.InfoHandler()
# Loading stockfish-11 engine 
# Linux
engine = chess.uci.popen_engine('engines/stockfish-11-linux/stockfish-11-linux/Linux/stockfish_20011801_x64')

# Windows
# engine = chess.uci.popen_engine('engines/stockfish-11-win/stockfish-11-win/Windows/stockfish_20011801_x64.exe')

# Mac
# engine = chess.uci.popen_engine('engines/stockfish-11-win/stockfish-11-mac/Mac/stockfish-11-64')

# To use other engines like Leela-Chess-Zero give path to the engine and 

engine.setoption({'MultiPV': 100})
engine.info_handlers.append(handler)
# board

import numpy as np


def get_dict_q_vals(board, legal_moves, eval_time, original_move):
    """
    This function returns a dictionary of Q-values for every move.
    Input:
        board: chess.Board()
        legal_moves: List of legal moves of original state
        eval_time: Search time for stockfish
        original_move: original best move (chess.Move()) 
    Output:
        q_vals_dict: Dictionary of move with respective Q-value
        q_vals: np array of Q values of required moves
        max_move: chess.Move() - Best move in perturbed state
        second_max_move: chess.Move() - Second best move in perturbed state
    """
    
    i = 0
    q_vals_dict = {}
    
    
    set_current_legal_moves = set(board.legal_moves)
    set_original_legal_moves = set(legal_moves)
    intersection_set = set_current_legal_moves.intersection(set_original_legal_moves)

    print('querying engine with perturbed position')
    engine.position(board)
    evaluation = engine.go(movetime=eval_time)
    # print(evaluation)
    if original_move is None:
        # no initial move supplied
        original_move = evaluation.bestmove
    dict_moves_to_score = defaultdict(int)
    
    for move_id in handler.info['pv'].keys():
        move_string = str(handler.info['pv'][move_id][0])
        move_score = 0
        if handler.info["score"][move_id].cp is None:
            mate_in_moves = handler.info["score"][move_id].mate
            if mate_in_moves > 0:
                # white will win in some number of moves
                move_score = 40
            else:
                # black will win 
                move_score = -40
        else:
            move_score = round(handler.info["score"][move_id].cp/100.0,2)
        dict_moves_to_score[move_string] = move_score
    
    # print(dict_moves_to_score)
    
    print('Total Legal Moves : ', len(intersection_set))

    for el in legal_moves:
        if el in intersection_set:
            i += 1
            score = dict_moves_to_score[str(el)]
            q_vals_dict[el.uci()] = score
    
    return q_vals_dict, evaluation.bestmove



def computeSaliency(FEN = 'rnbq1rk1/pp2bppp/4p3/3p3n/3P1B2/3B1N2/PPPNQPPP/R3K2R w KQkq - 0 1'):
    print("***********************", FEN, "**********************")
    board = chess.Board(FEN)
    evaltime = 6000
    legal_moves = list(board.legal_moves)[:]

    # Q-values for original state
    dict_q_values_before_perturbation, original_move  = get_dict_q_vals(board, legal_moves, evaltime, None)
    print('original move = ', original_move)
     
    answer = {
        'a1' : {'int': chess.A1, 'saliency': -2},
        'a2' : {'int': chess.A2, 'saliency': -2},
        'a3' : {'int': chess.A3, 'saliency': -2},
        'a4' : {'int': chess.A4, 'saliency': -2},
        'a5' : {'int': chess.A5, 'saliency': -2},
        'a6' : {'int': chess.A6, 'saliency': -2},
        'a7' : {'int': chess.A7, 'saliency': -2},
        'a8' : {'int': chess.A8, 'saliency': -2},
        'b1' : {'int': chess.B1, 'saliency': -2},
        'b2' : {'int': chess.B2, 'saliency': -2},
        'b3' : {'int': chess.B3, 'saliency': -2},
        'b4' : {'int': chess.B4, 'saliency': -2},
        'b5' : {'int': chess.B5, 'saliency': -2},
        'b6' : {'int': chess.B6, 'saliency': -2},
        'b7' : {'int': chess.B7, 'saliency': -2},
        'b8' : {'int': chess.B8, 'saliency': -2},
        'c1' : {'int': chess.C1, 'saliency': -2},
        'c2' : {'int': chess.C2, 'saliency': -2},
        'c3' : {'int': chess.C3, 'saliency': -2},
        'c4' : {'int': chess.C4, 'saliency': -2},
        'c5' : {'int': chess.C5, 'saliency': -2},
        'c6' : {'int': chess.C6, 'saliency': -2},
        'c7' : {'int': chess.C7, 'saliency': -2},
        'c8' : {'int': chess.C8, 'saliency': -2},
        'd1' : {'int': chess.D1, 'saliency': -2},
        'd2' : {'int': chess.D2, 'saliency': -2},
        'd3' : {'int': chess.D3, 'saliency': -2},
        'd4' : {'int': chess.D4, 'saliency': -2},
        'd5' : {'int': chess.D5, 'saliency': -2},
        'd6' : {'int': chess.D6, 'saliency': -2},
        'd7' : {'int': chess.D7, 'saliency': -2},
        'd8' : {'int': chess.D8, 'saliency': -2},
        'e1' : {'int': chess.E1, 'saliency': -2},
        'e2' : {'int': chess.E2, 'saliency': -2},
        'e3' : {'int': chess.E3, 'saliency': -2},
        'e4' : {'int': chess.E4, 'saliency': -2},
        'e5' : {'int': chess.E5, 'saliency': -2},
        'e6' : {'int': chess.E6, 'saliency': -2},
        'e7' : {'int': chess.E7, 'saliency': -2},
        'e8' : {'int': chess.E8, 'saliency': -2},
        'f1' : {'int': chess.F1, 'saliency': -2},
        'f2' : {'int': chess.F2, 'saliency': -2},
        'f3' : {'int': chess.F3, 'saliency': -2},
        'f4' : {'int': chess.F4, 'saliency': -2},
        'f5' : {'int': chess.F5, 'saliency': -2},
        'f6' : {'int': chess.F6, 'saliency': -2},
        'f7' : {'int': chess.F7, 'saliency': -2},
        'f8' : {'int': chess.F8, 'saliency': -2},
        'g1' : {'int': chess.G1, 'saliency': -2},
        'g2' : {'int': chess.G2, 'saliency': -2},
        'g3' : {'int': chess.G3, 'saliency': -2},
        'g4' : {'int': chess.G4, 'saliency': -2},
        'g5' : {'int': chess.G5, 'saliency': -2},
        'g6' : {'int': chess.G6, 'saliency': -2},
        'g7' : {'int': chess.G7, 'saliency': -2},
        'g8' : {'int': chess.G8, 'saliency': -2},
        'h1' : {'int': chess.H1, 'saliency': -2},
        'h2' : {'int': chess.H2, 'saliency': -2},
        'h3' : {'int': chess.H3, 'saliency': -2},
        'h4' : {'int': chess.H4, 'saliency': -2},
        'h5' : {'int': chess.H5, 'saliency': -2},
        'h6' : {'int': chess.H6, 'saliency': -2},
        'h7' : {'int': chess.H7, 'saliency': -2},
        'h8' : {'int': chess.H8, 'saliency': -2},

        }
    
    for square_string in sorted(answer.keys()):
        entry = answer[square_string]
        entry_keys = ['saliency', 'dP', 'K', 'QMaxAnswer', 'actionGapBeforePerturbation', 'actionGapAfterPerturbation']
        print('perturbing square = ', square_string)
        # perturb board
        piece_removed = board.remove_piece_at(entry['int'])
        
        if piece_removed is None:
            # square was empty, so proceed without changing anything
            print('square was empty, so skipped')
            # print(board)
            print('------------------------------------------')
        
            continue
        
        elif (piece_removed == chess.Piece(6,True) or piece_removed == chess.Piece(6,False)) or board.was_into_check():
            # illegal piece was removed
            print('illegal piece was removed')
            for key in entry_keys:
                entry[key] = 0
        else:
            # set perturbed state
            engine.position(board)

            # Check if the original move is still valid
            if board.is_legal(original_move):
                # Find the q values 
                dict_q_values_after_perturbation, _ = get_dict_q_vals(board, legal_moves, evaltime, original_move)
                entry['saliency'], entry['dP'], entry['K'], entry['QMaxAnswer'],\
                    entry['actionGapBeforePerturbation'], entry['actionGapAfterPerturbation']\
                         = sarfa_saliency.computeSaliencyUsingSarfa(str(original_move), dict_q_values_before_perturbation, dict_q_values_after_perturbation)
                print('saliency for this square = ', entry)
                
            else:
                # illegal original move in perturbed state, therefore piece removed is probably important 
                # print(board.is_legal(original_move))
                # print(board)
                print('original move illegal in perturbed state')
                for key in entry_keys:
                    entry[key] = -1
                entry['saliency'] = 1 
                
        # undo perturbation
        print('------------------------------------------')
                
        board.set_piece_at(entry['int'], piece_removed)
        

    print(answer)
    return(answer)

# computeSaliency(FEN='2r1r1k1/b4ppp/p3p3/Pp2Nq2/1Pbp1B2/R7/2PQ1PP1/4R1K1 w - - 0 1')
# computeSaliency()
# computeSaliency(FEN='r1b4k/3q3r/8/2pP1Q2/1pB3n1/8/PP4PP/3R2K1 w - - 0 2')
# computeSaliency(FEN='R4rk1/5bb1/1N1Qpq1p/3pn1p1/3N4/2P2P1P/P5P1/5B1K w - - 0 1')
