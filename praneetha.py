class Player72:

	def __init__(self):
		pass

	def move(self, temp_board, temp_block, old_move, player_flag):

		if old_move == (-1, -1):
			return (4, 4)

		if(player_flag == 'x')
			opponent_flag = 'o'
		else
			opponent_flag = 'x'

		player_board = temp_board[:];
		player_block = temp_block[:];

		alphabeta_node = old_move
		depth_limit = 4

		next_move = alphabetaPruning(alphabeta_node, player_board[:], player_block[:], depth_limit, -1000, 1000, True, player_flag, opponent_flag, -1, -1)

		return (next_move[0], next_move[1])


	def alphabetaPruning(node, board, block, depth, alpha, beta, isMax, flag1, flag2, row, col):

		cells = getCells(board, block, node)
		
		if depth == 0 or len(cells) == 0:
			utility = check(board, block)
			if(flag1 == 'o')
				return (row, col, -utility)
			return (row, col, utility)

		for cell in cells:
			
			if isMax:
				board[cell[0]][cell[1]] = flag1
			else
				board[cell[0]][cell[1]] = flag2

			if isMax:
				val = alphabetaPruning(cell, board, block, depth-1, alpha, beta, False, flag1, flag2, row, col)
				if(val[2] > alpha)
					alpha = val[2]
					row = cell[0]
					col = cell[1]
			else
				val = alphabetaPruning(cell, board, block, depth-1, alpha, beta, True, flag1, flag2, row, col)
				if(val[2] < beta)
					beta = val[2]
					row = cell[0]
					col = cell[1]

			board[cell[0]][cell[1]] = '-'
			if(alpha >= beta)
				break

		if isMax:
			return (row, col, alpha)
		else
			return (row, col, beta)

	def getCells(board, block, old_move):

		if old_move == (-1, -1):
			allowed_blocks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
		else:
			allowed_blocks = []
			if old_move[0]%3 == 1 and old_move[1]%3 == 1:
				allowed_blocks = [4]
			else:
				if old_move[1]%3 == 0 and old_move[0]%3 == 0:
					allowed_blocks = [1, 3]
				else if old_move[1]%3 == 1 and old_move[0]%3 == 0:
					allowed_blocks = [0, 2]
				else if old_move[1]%3 == 2 and old_move[0]%3 == 0:
					allowed_blocks = [1, 5]
				else if old_move[1]%3 == 0 and old_move[0]%3 == 1:
					allowed_blocks = [0, 6]
				else if old_move[1]%3 == 2 and old_move[0]%3 == 1:
					allowed_blocks [2, 8]
				else if old_move[1]%3 == 0 and old_move[0]%3 == 2:
					allowed_blocks [3, 7]
				else if old_move[1]%3 == 1 and old_move[0]%3 == 2:
					allowed_blocks [6, 8]
				else if old_move[1]%3 == 2 and old_move[0]%3 == 2:
					allowed_blocks [7, 5]
				else:
					print "not a valid old move"

		for i in reversed(allowed_blocks):
				if block[i] != '-':
					allowed_blocks.remove(i)

		cells = getValidEmptyCells(board, block, allowed_blocks)
		return cells

	def getValidEmptyCells(board, block_status, allowed_blocks):

		cells = []
		for block in allowed_blocks:
			if allowed_blocks[block] == '-':
				id1 = block / 3;
				id2 = block % 3;
				for i in range(id1*3,id1*3+3):
					for j in range(id2*3,id2*3+3):
						if board[i][j] == '-':
							cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			for i in range(9):
				for j in range(9):
	                no = (i/3)*3
	                no += (j/3)
					if gameb[i][j] == '-' and block_stat[no] == '-':
						cells.append((i,j))	
		return cells



