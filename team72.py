
freeMove = False

class Player72:

	def __init__(self):
		pass

	def move(self, temp_board, temp_block_status, old_move, player_flag):

		if old_move == (-1, -1):
			print "old move"
			return (2, 4)

		if player_flag == 'x':
			opponent_flag = 'o'
		else:
			opponent_flag = 'x'

		player_board = temp_board[:];
		player_block = temp_block_status[:];

		alphabeta_node = old_move
		depth_limit = 4
		

		next_move = alphabetaPruning(alphabeta_node, player_board[:], player_block[:], depth_limit, -100000, 100000, True, player_flag, opponent_flag, -1, -1)
		print next_move[0], next_move[1]
		return (next_move[0], next_move[1])


def alphabetaPruning(node, board, block_status, depth, alpha, beta, isMax, flag1, flag2, row, col):


		cells = getCells(board, block_status, node)
		if depth == 0 or len(cells) == 0:
			utility = 0
			if freeMove:
				utility += 1000
			utility += check(board, block_status, row, col, flag1)
			return (row, col, utility)

		for cell in cells:
			
			if isMax:
				board[cell[0]][cell[1]] = flag1
			else:
				board[cell[0]][cell[1]] = flag2

			if isMax:
				val = alphabetaPruning(cell, board, block_status, depth-1, alpha, beta, False, flag1, flag2, row, col)
				if val[2] > alpha :
					alpha = val[2]
					row = cell[0]
					col = cell[1]
			else:
				val = alphabetaPruning(cell, board, block_status, depth-1, alpha, beta, True, flag1, flag2, row, col)
				if val[2] < beta:
					beta = val[2]
					row = cell[0]
					col = cell[1]

			board[cell[0]][cell[1]] = '-'
			if alpha >= beta:
				break

		if isMax:
			return (row, col, alpha)
		else:
			return (row, col, beta)

def getCells(board, block_status, old_move):

		if old_move == (-1, -1):
			allowed_blocks = [0, 1, 2, 3, 4, 5, 6, 7, 8]
		else:
			allowed_blocks = []
			if old_move[0]%3 == 1 and old_move[1]%3 == 1:
				allowed_blocks = [4]
			else:
				if old_move[1]%3 == 0 and old_move[0]%3 == 0:
					allowed_blocks = [1, 3]
				elif old_move[1]%3 == 1 and old_move[0]%3 == 0:
					allowed_blocks = [0, 2]
				elif old_move[1]%3 == 2 and old_move[0]%3 == 0:
					allowed_blocks = [1, 5]
				elif old_move[1]%3 == 0 and old_move[0]%3 == 1:
					allowed_blocks = [0, 6]
				elif old_move[1]%3 == 2 and old_move[0]%3 == 1:
					allowed_blocks = [2, 8]
				elif old_move[1]%3 == 0 and old_move[0]%3 == 2:
					allowed_blocks = [3, 7]
				elif old_move[1]%3 == 1 and old_move[0]%3 == 2:
					allowed_blocks = [6, 8]
				elif old_move[1]%3 == 2 and old_move[0]%3 == 2:
					allowed_blocks = [7, 5]
				else:
					print "not a valid old move"

		for i in reversed(allowed_blocks):
				if block_status[i] != '-':
					allowed_blocks.remove(i)

		cells = getValidEmptyCells(board, block_status, allowed_blocks)
		return cells

def getValidEmptyCells(board, block_status, allowed_blocks):

		cells = []
		freeMove = False
		for block in allowed_blocks:
			if block_status[block] == '-':
				id1 = block / 3;
				id2 = block % 3;
				for i in range(id1*3,id1*3+3):
					for j in range(id2*3,id2*3+3):
						if board[i][j] == '-':
							cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			freeMove = True
			for i in range(9):
				for j in range(9):
	                		no = (i/3)*3
	                		no += (j/3)
					if board[i][j] == '-' and block_status[no] == '-':
						cells.append((i,j))	
		return cells

def calculate(count_empty, count_x, count_o, player_flag):
	
	gain = 0

	if player_flag == 'x':
		player_count = count_x
		opponent_count = count_o
	else:
		player_count = count_o
		opponent_count = count_x

	# if opponent_count == 0:
	# 	gain += pow(10, player_count) * 5
	# if opponent_count == 3:
	# 	gain -= pow(10, opponent_count) * 5

	if player_count == 3 and opponent_count == 0 and count_empty == 0:
		return gain + 10000
	if player_count == 0 and opponent_count == 3 and count_empty == 0:
		return gain - 10000
	if player_count == 1 and opponent_count == 2 and count_empty == 0:
		return gain + 1000
	if player_count == 2 and opponent_count == 0 and count_empty == 1:
		return gain + 100
	if player_count == 0 and opponent_count == 2 and count_empty == 1:
		return gain - 100
	if player_count == 1 and opponent_count == 0 and count_empty == 2:
		return gain + 10
	if player_count == 0 and opponent_count == 1 and count_empty == 2:
		return gain - 10
	if player_count == 0 and opponent_count == 0 and count_empty == 3:
		return gain + 1
	if player_count == 2 and opponent_count == 1 and count_empty == 0:
		return gain + 0
	if player_count == 1 and opponent_count == 1 and count_empty == 1:
		return gain + 0
	else:
		print player_count, opponent_count, count_empty
	return 0

def getBlockUtility(board, block_no, player_flag):
	block_row = block_no / 3;
	block_col = block_no % 3;
	utility = 0
	empty = 0
	count_x = 0
	count_o = 0

	for i in range(0, 3):
		empty = 0
		count_x = 0
		count_o = 0
		for j in range(0, 3):
			if board[block_row * 3 + i][block_col * 3 + j] == '-':
				empty += 1
			if board[block_row * 3 + i][block_col * 3 + j] == 'x':
				count_x += 1
			if board[block_row * 3 + i][block_col * 3 + j] == 'o':
				count_o += 1
		if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
		if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

		utility += calculate(empty, count_x, count_o, player_flag)

	empty = 0
	count_x = 0
	count_o = 0

	for j in range(0, 3):
		empty = 0
		count_x = 0
		count_o = 0
		for i in range(0, 3):
			if board[block_row * 3 + i][block_col * 3 + j] == '-':
				empty += 1
			if board[block_row * 3 + i][block_col * 3 + j] == 'x':
				count_x += 1
			if board[block_row * 3 + i][block_col * 3 + j] == 'o':
				count_o += 1
		if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
		if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

		utility += calculate(empty, count_x, count_o, player_flag)

	empty = 0
	count_x = 0
	count_o = 0

	for i in range(0, 3):
		if board[block_row * 3 + i][block_col * 3 + i] == '-':
				empty += 1
		if board[block_row * 3 + i][block_col * 3 + i] == 'x':
				count_x += 1
		if board[block_row * 3 + i][block_col * 3 + i] == 'o':
				count_o += 1

		if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
		if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

	utility += calculate(empty, count_x, count_o, player_flag)

	empty = 0
	count_x = 0
	count_o = 0

	for i in range(0, 3):
		if board[block_row * 3  + i][block_col * 3 + 2 - i] == '-':
			empty += 1
		if board[block_row * 3 + i][block_col * 3 + 2 - i] == 'x':
			count_x += 1
		if board[block_row * 3 + i][block_col * 3 + 2 - i] == 'o':
			count_o += 1
		
		if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
		if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

	utility += calculate(empty, count_x, count_o, player_flag)

	return utility

def checkOpponentFreeMove(board, cell_row, cell_col, block_status, player_flag):
	cells = getCells(board, block_status, (cell_row, cell_col))
	if freeMove:
		return True
	return False

def checkOpponentWinning(board, cell_row, cell_col, block_status, player_flag):
	
	cells = getCells(board, block_status, (cell_row, cell_col))
	freeMove = False
	for cell in cells:
		if player_flag == 'x':
			opponent_flag = 'o'
		else:
			opponent_flag = 'x'
		
		board[cell[0]][cell[1]] = opponent_flag
		
		block_start_row = cell[0] - cell[0] % 3
		block_start_col = cell[1] - cell[1] % 3
		count_opponent = 0
		for i in range(0, 3):
			if board[block_start_row + i][block_start_col] == opponent_flag:
				count_opponent += 1
		if count_opponent == 3:
			board[cell[0]][cell[1]] = '-'
			return True

		count_opponent = 0
		for i in range(0, 3):
			if board[block_start_row][block_start_col + i] == opponent_flag:
				count_opponent += 1
		if count_opponent == 3:
			board[cell[0]][cell[1]] = '-'
			return True

		count_opponent = 0
		if cell_row % 3 == cell_col % 3:
			for i in range(0, 3):
				if board[block_start_row + i][block_start_col] == opponent_flag:
					count_opponent += 1
			if count_opponent == 3:
				board[cell[0]][cell[1]] = '-'
				return True

		count_opponent = 0
		if cell_row % 3 == 2 - cell_col % 3:
			for i in range(0, 3):
				if board[block_start_row + i][block_start_col] == opponent_flag:
					count_opponent += 1
			if count_opponent == 3:
				board[cell[0]][cell[1]] = '-'
				return True

		board[cell[0]][cell[1]] = '-'

	return False




def getCellUtility(board, block_status, cell_row, cell_col, player_flag):
	board_row = cell_row - cell_row % 3;
	board_col = cell_col - cell_col % 3;
	utility = 0
	empty = 0
	count_x = 0
	count_o = 0

	for i in range(0, 3):
		if board[cell_row][board_col + i] == '-':
			empty += 1;
		if board[cell_row][board_col + i] == 'x':
			count_x += 1;
		if board[cell_row][board_col + i] == 'o':
			count_o += 1;

	if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
	if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

	utility += calculate(empty, count_x, count_o, player_flag)


	empty = 0
	count_x = 0
	count_o = 0
	for i in range(0, 3):
		if board[board_row + i][cell_col] == '-':
			empty += 1;
		if board[board_row + i][cell_col] == 'x':
			count_x += 1;
		if board[board_row + i][cell_col] == 'o':
			count_o += 1;
	utility += calculate(empty, count_x, count_o, player_flag)

	if cell_row % 3 == cell_col % 3:
		empty = 0
		count_x = 0
		count_o = 0
		for i in range(0, 3):
			if board[board_row + i][board_col + i] == '-':
				empty += 1;
			if board[board_row + i][board_col + i] == 'x':
				count_x += 1;
			if board[board_row + i][board_col + i] == 'o':
				count_o += 1;
		
		if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
		if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

		utility += calculate(empty, count_x, count_o, player_flag)

	if cell_row % 3 == 2 - cell_col % 3:
		empty = 0
		count_x = 0
		count_o = 0
		for i in range(0, 3):
			if board[board_row + i][board_col + 2 - i] == '-':
				empty += 1;
			if board[board_row + i][board_col + 2 - i] == 'x':
				count_x += 1;
			if board[board_row + i][board_col + 2 - i] == 'o':
				count_o += 1;
		
		if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
		if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

		utility += calculate(empty, count_x, count_o, player_flag)

	if checkOpponentWinning(board, cell_row, cell_col, block_status, player_flag):
		utility += -10000
	if checkOpponentFreeMove(board, cell_row, cell_col, block_status, player_flag):
		utility += -100

	return utility

def calculateFactor(count_x, count_o, player_flag):
	
	factor = pow(10, abs(count_x - count_o))
	
	if player_flag == 'x' and count_o > count_x:
		factor = -factor
	if player_flag == 'o' and count_x > count_o:
		factor = -factor
	
	return factor


def getBlockGlobalUtility(block_status, block_no, block_utility, player_flag):
	
	board_start_row = (block_no / 3)
	board_start_col = (block_no % 3)
	utility = 0
	

	count_empty = 0
	count_x = 0
	count_o = 0
	probability = 0

	for i in range(0, 3):
		
		check_block_no = board_start_row * 3 + i
		probability += block_utility[check_block_no]

		if block_status[check_block_no] == '-':
			count_empty += 1
		if block_status[check_block_no] == 'x':
			count_x += 1
		if block_status[check_block_no] == 'o':
			count_o += 1
	if player_flag == 'x' and count_x == 3:
		return 1000
	if player_flag == 'o' and count_o == 3:
		return -1000

	factor = calculateFactor(count_x, count_o, player_flag)
	
	utility +=  factor * (probability / 30000)

	count_empty = 0
	count_x = 0
	count_o = 0
	probability = 0
	for i in range(0, 3):
		
		check_block_no = board_start_col + i * 3
		probability += block_utility[check_block_no]

		if block_status[check_block_no] == '-':
			count_empty += 1
		if block_status[check_block_no] == 'x':
			count_x += 1
		if block_status[check_block_no] == 'o':
			count_o += 1
	if player_flag == 'x' and count_x == 3:
		return 1000
	if player_flag == 'o' and count_o == 3:
		return -1000

	factor = calculateFactor(count_x, count_o, player_flag)

	utility += factor * (probability / 30000)

	if board_start_row == board_start_col:
		count_empty = 0
		count_x = 0
		count_o = 0
		probability = 0
		for i in range(0, 3):
			
			check_block_no = 3 * i + i
			probability += block_utility[check_block_no]
			
			if block_status[check_block_no] == '-':
				count_empty += 1
			if block_status[check_block_no] == 'x':
				count_x += 1
			if block_status[check_block_no] == 'o':
				count_o += 1
		if player_flag == 'x' and count_x == 3:
			return 1000
		if player_flag == 'o' and count_o == 3:
			return -1000

		factor = calculateFactor(count_x, count_o, player_flag)

		utility += factor * (probability / 30000)

	if board_start_row == 2 - board_start_col:
		count_empty = 0
		count_x = 0
		count_o = 0
		probability = 0
		for i in range(0, 3):
			
			check_block_no = 2 * (i + 1)
			probability += block_utility[check_block_no]
			
			if block_status[check_block_no] == '-':
				count_empty += 1
			if block_status[check_block_no] == 'x':
				count_x += 1
			if block_status[check_block_no] == 'o':
				count_o += 1
			if player_flag == 'x' and count_x == 3:
				return 1000
			if player_flag == 'o' and count_o == 3:
				return -1000

		factor = calculateFactor(count_x, count_o, player_flag)

		utility += factor * (probability / 30000)
	return utility

def check(board, block_status, row, col, player_flag):
	block_utility = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for block_no in range(0 ,9):
		block_utility[block_no] = getBlockUtility(board, block_no, player_flag)
	
	cell_utility = getCellUtility(board, block_status, row, col, player_flag)

	block_no = 3 * ((row - row % 3) / 3) + (col - col % 3) / 3

	globalUtility = getBlockGlobalUtility(block_status, block_no, block_utility, player_flag)

	specific_block_winning_utility = 0
	if cell_utility == 10000:
		if block_no == 4:
			specific_block_winning_utility = 1000
		if block_no in [0, 2, 6, 8]:
			specific_block_winning_utility = 800 

	return cell_utility / 10 + globalUtility + specific_block_winning_utility / 10






