freeMove = False

# done
class Player72:
	# done
	def __init__(self):
		pass

	# done
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

		depth_limit = 4

		next_move = alphabetaPruning(old_move, player_board[:], player_block[:], depth_limit, -100000, 100000, True, player_flag, opponent_flag, -1, -1)
		print next_move[0], next_move[1]
		return (next_move[0], next_move[1])

# done
def alphabetaPruning(old_move, board, block_status, depth, alpha, beta, isMax, player_flag, opponent_flag, row, col):

		cells = getCells(board, block_status, old_move)
		if depth == 0 or len(cells) == 0:
			# from now on we'll assume player_flag to be 'x' and if not the case, we'll just invert the utility obtained
			utility = check(board, block_status, row, col, player_flag) 
			if player_flag == 'o':
				return (row, col, -utility)
			return (row, col, utility)

		for cell in cells:
			# place the move here to test
			if isMax:
				board[cell[0]][cell[1]] = player_flag
			else:
				board[cell[0]][cell[1]] = opponent_flag
			if isMax:
				val = alphabetaPruning(cell, board, block_status, depth-1, alpha, beta, False, player_flag, opponent_flag, row, col)
				if val[2] > alpha :
					alpha = val[2]
					row = cell[0]
					col = cell[1]
			else:
				val = alphabetaPruning(cell, board, block_status, depth-1, alpha, beta, True, player_flag, opponent_flag, row, col)
				if val[2] < beta:
					beta = val[2]
					row = cell[0]
					col = cell[1]
			# remove the last move, since we haven't yet decided which move to go for
			board[cell[0]][cell[1]] = '-'
			if alpha >= beta:
				break

		if isMax:
			return (row, col, alpha)
		else:
			return (row, col, beta)

# done
def getCells(board, block_status, old_move):

		if old_move == (-1, -1):
			allowed_blocks = [0, 1, 2, 3, 4, 5, 6, 7, 8]	# all blocka allowed
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

		# if already won by 'x' or 'o', then remove from allowed blocks
		for i in reversed(allowed_blocks):
				if block_status[i] != '-':
					allowed_blocks.remove(i)

		cells = getValidEmptyCells(board, block_status, allowed_blocks)
		return cells

# done
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

# done
def calculate(count_empty, count_x, count_o):
	
	gain = 0
	if count_x == 1 and count_o == 0 and count_empty == 2:
		# x-- or --x or -x-
		gain = 1;
	if count_x == 0 and count_o == 1 and count_empty == 2:
		# o-- or --o or -o-
		gain = -1;
	if count_x == 2 and count_o == 0 and count_empty == 1:
		# xx- or -xx or x-x
		gain = 10;
	if count_x == 0 and count_o == 2 and count_empty == 1:
		# oo- or -oo or o-o
		gain = -10;
	# if any other is there, then it's useless for us
	# like xo- or xoo or xox, therefore for that we'll return 0	
	return gain
	
# done
def getEachBlockUtility(board, block_no):
	
	# calculate block's starting row and column in the board in [0..9][0..9]
	block_row = block_no / 3;
	block_col = block_no % 3;
	
	current_block_utility = 0
	
	win_in_previous_check = False
	# check for each row
	for i in range(0, 3):
		
		# initialize counts here
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
		if count_x == 3:
			current_block_utility = calculate(empty, count_x, count_o) # clear win, thus return
			win_in_previous_check = True
			break
		elif count_o == 3:
			current_block_utility = calculate(empty, count_x, count_o)	# clear lose, thus return
			win_in_previous_check = True
			break
		else:
			current_block_utility += calculate(empty, count_x, count_o)	# else add to current_block_utility


	if not win_in_previous_check:		
		# check for each column
		for j in range(0, 3):
			
			# initialize counts here
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
			if count_x == 3:
				current_block_utility = calculate(empty, count_x, count_o) # clear win, thus return
				win_in_previous_check = True
				break
			elif count_o == 3:
				current_block_utility = calculate(empty, count_x, count_o)	# clear lose, thus return
				win_in_previous_check = True
				break
			else:
				current_block_utility += calculate(empty, count_x, count_o)	# else add to current_block_utility


	if not win_in_previous_check:
		# then check for diagnol 1
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

		if count_x == 3:
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		if count_o == 3:
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		else:	
			current_block_utility += calculate(empty, count_x, count_o)


	if not win_in_previous_check:
		# if still hasn't won anywhere, then check for diagnol 2
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
			
		if count_x == 3:
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		if count_o == 3:
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		else:
			current_block_utility += calculate(empty, count_x, count_o)

	# will have all the effect, if win at some time then only that part's contribution, else addition of all other values
	return current_block_utility	# final gain

# done
def OnEdge(hx, hy, board):
	cx=0
	co=0
	cd=0
	for i in range(0,3):
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1		
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	return 0

# done
def OnCenter(hx, hy,board):
	cx=0
	co=0
	cd=0
	for i in range(0,3):
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gx = hx - hx%3
		gy = hy - hy%3
		if board[gx+i][gy+i] == '-':
			cd += 1;
		if board[gx+i][gy+i] == 'x':
			cx += 1;
		if board[gx+i][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gx = gx - gx%3
		gy = gy + gy%3
		if board[gx+i][gy-i] == '-':
			cd += 1;
		if board[gx+i][gy-i] == 'x':
			cx += 1;
		if board[gx+i][gy-i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	return 0

# done
def OnTopLeftOrBottomRight(hx, hy,board):
	cx=0
	co=0
	cd=0
	for i in range(0,3):
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gx = hx - hx%3
		gy = hy - hy%3
		if board[gx+i][gy+i] == '-':
			cd += 1;
		if board[gx+i][gy+i] == 'x':
			cx += 1;
		if board[gx+i][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	return 0

# done
def OnTopRightOrBottomLeft(hx, hy,board):
	cx = 0
	co = 0
	cd = 0
	for i in range(0,3):
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	for i in range(0,3):
		gx = gx - gx%3
		gy = gy + gy%3
		if board[gx+i][gy-i] == '-':
			cd += 1;
		if board[gx+i][gy-i] == 'x':
			cx += 1;
		if board[gx+i][gy-i] == 'o':
			co += 1
		next=calculate(cx, cd, co)
		if next > 0:
			return next
	return 0

# done
def CountEmpty(board, block_no):

	count_x = 0;
	count_o = 0;
	count_empty = 0;

	# calculate block's starting row and column in the board in [0..9][0..9]
	block_row = block_no / 3;
	block_col = block_no % 3;

	# count number of - in the entire block
	for j in range(0,3):
		for i in range(0,3):
			if board[block_row * 3 + i][block_col * 3 + j] == '-':
				count_empty += 1
				# save that -'s coordinate 
				empty_x = (block_row * 3 + i)
				empty_y = (block_col * 3 + j)
			if board[block_row * 3 + i][block_col * 3 + j] == 'x':
				count_x += 1
			if board[block_row * 3 + i][block_col * 3 + j] == 'o':
				count_y += 1

	if count_empty == 0:
		# then no point of putting it there, therefore huge disadvantage
		return -200
	if count_empty == 1:
		# we got the - at ...
		# we'll go through that cell's row/col/d1/d2 (wherever it is placed accordingly) and then see if there's any point of putting it there or not
		gain = 0
		if empty_x % 3 == 1 and empty_y % 3 == 1: 		# ... center of that block
			gain = OnCenter(empty_x, empty_y, board)
		elif empty_x % 3 == 0 and empty_y % 3==1:		# ... top center of that block
			gain = OnEdge(empty_x, empty_y, board)
		elif empty_x % 3==1 and empty_y % 3 == 0:		# ... left center
			gain = OnEdge(empty_x, empty_y, board)
		elif empty_x % 3 == 2 and empty_y % 3 == 1:		# ... bottom center
			gain = OnEdge(empty_x, empty_y, board)
		elif empty_x % 3==1 and empty_y % 3 == 2:		# ... right center
			gain = OnEdge(empty_x, empty_y, board)	
		elif empty_x % 3==0 and empty_y % 3==0:			# ... top left corner
			gain = OnTopLeftOrBottomRight(empty_x, empty_y, board)
		elif empty_x % 3 == 2 and empty_y % 3 == 2:		# ... bottom right corner
			gain = OnTopLeftOrBottomRight(empty_x, empty_y, board)
		elif empty_x % 3 == 0 and empty_y % 3 == 2:		# ... top right corner
			gain = OnTopRightOrBottomLeft(empty_x, empty_y, board)
		elif empty_x % 3 == 2 and empty_y % 3 == 0:		# ... bottom left corner
			gain = OnTopRightOrBottomLeft(empty_x, empty_y, board)

		if gain == 0:
			# if gain is still 0, then no point of putting it there, therefore huge disadvantage
			return -200
	return 0


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

	if player_flag == 'x' and count_x == 3:
			return calculate(empty, count_x, count_o, player_flag)
	if player_flag == 'o' and count_o == 3:
			return calculate(empty, count_x, count_o, player_flag)

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
		utility += 0 # here -10000
	if checkOpponentFreeMove(board, cell_row, cell_col, block_status, player_flag):
		utility += 0 # here -100

	return utility

# done
def calculateFactor(sum):
	
	factor = 0
	# opponent's favor
	if -3 < sum and sum < -2:
		factor = -(100 - 10)
	elif -2 < sum and sum < -1:
		factor = -(10 - 1)
	elif -1 < sum and sum < 0:
		factor = -(1 - 0)
	# in our favor
    elif 0 < sum and sum < 1:
		factor = (1 - 0)
	elif 1<sum and sum < 2:
		factor = (10 - 1)
	elif 2 < sum and sum < 3:
		factor = (100 - 10)
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
		return 1000

	factor = calculateFactor(count_x, count_o, player_flag)
	
	utility +=  factor * ((float)(probability / 30000.0))

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
		return 1000

	factor = calculateFactor(count_x, count_o, player_flag)

	utility += factor * ((float)(probability / 30000.0))

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
			return 1000

		factor = calculateFactor(count_x, count_o, player_flag)

		utility += factor * ((float)(probability / 30000.0))

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
				return 1000

		factor = calculateFactor(count_x, count_o, player_flag)

		utility += factor * ((float)(probability / 30000.0))
	return utility


def check(board, block_status, row, col, player_flag):
	
	block_utility = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for block_no in range(0 ,9):
		
		current_block_utility = getEachBlockUtility(board, block_no)
		if current_block_utility == 0:
			# still zero, then we need to consider additonal effects
			# it'll be zero only in case of 'xox' or 'xo-' type rows/cols/d1/d2 
			# i.e. either 0 empty cell or 1 empty cell in the block, 
			# where we won't have any direct profit if we place there
			# then we need to check other conditions like draw and any point of putting it there or not
			count_empty = CountEmpty(board, block_no)
		block_utility[block_no] = current_block_utility
	
	#################
	cell_utility = getCellUtility(board, block_status, row, col, player_flag)

	block_no = 3 * ((row - row % 3) / 3) + (col - col % 3) / 3

	globalUtility = getBlockGlobalUtility(block_status, block_no, block_utility, player_flag)

	specific_block_winning_utility = 0
	if cell_utility == 10000:
		if block_no == 4:
			specific_block_winning_utility = 1000
		if block_no in [0, 2, 6, 8]:
			specific_block_winning_utility = 800 

	#print "cell utility:", cell_utility
	#print "global utility:", globalUtility
	#print "specific utility:", specific_block_winning_utility
	total = cell_utility / 10.0 + globalUtility + specific_block_winning_utility / 10.0
	#print "total:", total
	return total



