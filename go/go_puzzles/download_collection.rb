require_relative 'puzzle'

raise ArgumentError, 'Missing ID of the puzzle to check' if ARGV.length == 0
collection_id = ARGV[0].to_i
folder_name = ARGV[1].nil? ? collection_id.to_s : ARGV[1]
raise ArgumentError, 'not a numeric puzzle id' if collection_id.nil?

Dir.mkdir(folder_name) unless Dir.exist?(folder_name)
Dir.chdir(folder_name)

puzzles = Puzzle.collection_summary(collection_id)
len = (puzzles.size + 1).to_s.length
puzzles.each_with_index { |puzzle, index|
  Puzzle.from_url(puzzle['id']).save(sprintf("%0#{len}d.sgf", puzzle['id']))

}
