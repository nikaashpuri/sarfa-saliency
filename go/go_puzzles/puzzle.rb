# Convert a Puzzle from Online Go Server [https://online-go.com/puzzles] to SGF.
require 'httparty'

class Puzzle
  include HTTParty
  base_uri 'https://online-go.com/api/v1/puzzles/'

  attr_accessor :id, :name, :description, :initial_state_white, :initial_state_black, :game_size, :tree, :initial_player, :source

  def initialize
    initial_state_white = Array.new
    initial_state_black = Array.new
  end

  # Convert the JSON object returned from OGS into a puzzle we can actually use.
  def self.from_json object
    # did we actually get an object?
    raise ArgumentError, 'no valid object as JSON result given' if object.nil?

    # most relevant information is stored in the puzzle node
    p = object['puzzle']

    puzzle = Puzzle.new

    # extract basic information about the puzzle
    puzzle.id = object['id'].to_i
    puzzle.name = "#{object['collection']['name']} - #{object['name']}"
    puzzle.description = p['puzzle_description']
    puzzle.source = "https://online-go.com/puzzle/#{puzzle.id}"
    # print('****************puzzle source is ', puzzle.source)
    # print('****************puzzle name is ', puzzle.name)
    # extract the game size; albeit this can presumably only be 9x9, 13x13 or 19x19, making the check for width != height redundant
    puzzle.game_size = p['width'].to_i
    height = p['height'].to_i
    puzzle.game_size = "#{puzzle.game_size}:#{height}" if puzzle.game_size != height

    # initial state
    puzzle.initial_state_white = p['initial_state']['white'].scan /../
    puzzle.initial_state_black = p['initial_state']['black'].scan /../
    puzzle.initial_player = p['initial_player'][0].upcase

    # the most important bit is obviously the move tree
    puzzle.tree = p['move_tree']

    puzzle
  end

  def self.from_url id
    response = get(id.to_s).body
    from_json(JSON.parse(response, max_nesting: 2000))
  end

  def self.collection_summary id
    get("#{id}/collection_summary")
  end

  def save(filename = 'test.sgf')
    File.open(filename, 'w') { |file|
      file.write '(;'

      # SGF version
      file.write 'FF[4]'

      # Let's play go!
      file.write 'GM[1]'

      # on a goban of the given size
      file.write "SZ[#{game_size}]"

      # application name (not like we have any)
      file.write "AP[online-go.com:1]\n"

      # source where we obtained it from
      file.write "SO[#{source.escape_for_sgf}]\n"

      # name of the puzzle
      file.write "GN[#{name.escape_for_sgf}]\n"

      # the moves set up on the board before you played.
      file.write initial_state_to_sgf('W', initial_state_white)
      file.write initial_state_to_sgf('B', initial_state_black)

      # who is to play initially?
      file.write "PL[#{initial_player}]"

      # what should we do for the puzzle?
      file.write "C[#{description.escape_for_sgf}]\n"

      # save the move tree
      save_moves file, tree, initial_player

      # end of the SGF structure
      file.write ")"
    }
  end

  private

  # We want to save a single move out of a puzzle
  def save_moves file, tree, player
    # If we have -1, -1 as coordinates, which we just skip
    if tree['x'] != -1 and tree['y'] != -1 then
      # color and coordinates
      file.write ";#{player}[#{sgf_board_position(tree)}]"

      # the other player is to play next
      player = invert_color(player)

      # do we have any move comments?
      comment = tree['text']

      # Is this the answer (right or wrong) already?
      if tree['correct_answer'] == true then
        comment = "Correct.\n#{comment}"
      elsif tree['wrong_answer'] == true then
        comment = "Wrong.\n#{comment}"
      end

      file.write "C[#{comment.escape_for_sgf}]" unless comment.nil? or comment.empty?
    end

    # do we have any marks?
    unless tree['marks'].nil? or tree['marks'].size == 0
      tree['marks'].each { |mark|
        position = sgf_board_position mark
        type = mark['marks']

        file.write "CR[#{position}]" unless type['circle'].nil?
        file.write "TR[#{position}]" unless type['triangle'].nil?
        file.write "MA[#{position}]" unless type['cross'].nil?
        file.write "SQ[#{position}]" unless  type['square'].nil?
        file.write "LB[#{position}:#{type['letter']}]" unless type['letter'].nil?
      }
    end

    # do we have follow-ups?
    unless tree['branches'].nil? or tree['branches'].size == 0
      if tree['branches'].size > 1 then
        # multiple possible moves
        tree['branches'].each { |branch|
          file.write '('
          save_moves file, branch, player
          file.write ")\n"
        }

      elsif tree['branches'].size == 1 then
        # a single follow-up move
        save_moves file, tree['branches'][0], player
      end
    end
  end

  def invert_color color
     color == 'W' ? 'B' : 'W'
  end

  # convert the x/y coordinates of 0-18, 0-18 to SGF's a-s, a-s
  def sgf_board_position tree
    x = ('a'.ord + tree['x']).chr
    y = ('a'.ord + tree['y']).chr
    "#{x}#{y}"
  end

  # convert the array of initial moves to SGF
  def initial_state_to_sgf(color, state)
    return '' if state.empty?
    'A' + color + state.map {|s| "[#{s}]" }.join + "\n"
  end
end

class String
  def escape_for_sgf
    gsub(']', '\\]').strip
  end
end
