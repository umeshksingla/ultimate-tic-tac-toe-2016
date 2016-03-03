freeMove = False
import random


# done
class Player72:
	
	# done
	def __init__(self):	
		pass

	# done
	def move(self, temp_board, temp_block_status, old_move, player_flag):
		
		first_moves = [(3, 3), (3, 5), (5, 3), (5, 5)]
		if old_move == (-1, -1):
			move = first_moves[random.randrange(len(first_moves))]
			return (5, 5)

		if player_flag == 'x':
			opponent_flag = 'o'
		else:
			opponent_flag = 'x'

		player_board = temp_board[:]
		player_block = temp_block_status[:]

		depth_limit = 4

		next_move = alphabetaPruning(old_move, player_board[:], player_block[:], depth_limit, -1000, 1000, True, player_flag, opponent_flag, -1, -1, -1, -1)
		# print next_move[0], next_move[1]
		return (next_move[0], next_move[1])

# done
def alphabetaPruning(old_move, board, block_status, depth, alpha, beta, isMax, player_flag, opponent_flag, row, col, current_row, current_col):

		cells = getCells(board, block_status, old_move)
		if depth == 0 or len(cells) == 0:
			# from now on we'll assume player_flag to be 'x' and if not the case, we'll just invert the utility obtained
			utility = check(board, block_status, current_row, current_col, player_flag) 
			if player_flag == 'o':
				utility = -utility
			#print "utility", utility
			return (row, col, utility)

		for cell in cells:
			#print cell
			# place the move here to test
			if isMax:
				board[cell[0]][cell[1]] = player_flag
			else:
				board[cell[0]][cell[1]] = opponent_flag
			if isMax:
				val = alphabetaPruning(cell, board, block_status, depth - 1, alpha, beta, False, player_flag, opponent_flag, row, col, cell[0], cell[1])
				if val[2] > alpha :
					alpha = val[2]
					row = cell[0]
					col = cell[1]
			else:
				val = alphabetaPruning(cell, board, block_status, depth - 1, alpha, beta, True, player_flag, opponent_flag, row, col, cell[0], cell[1])
				if val[2] < beta:
					beta = val[2]
					row = cell[0]
					col = cell[1]
			# remove the last move, since we haven't yet decided which move to go for
			board[cell[0]][cell[1]] = '-'
			if alpha > beta:
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
	if count_x == 3:
		gain = 100
	if count_o == 3:
		gain = -100
	if count_x == 1 and count_o == 0 and count_empty == 2:
		# x-- or --x or -x-
		gain = 1
	if count_x == 0 and count_o == 1 and count_empty == 2:
		# o-- or --o or -o-
		gain = -1
	if count_x == 2 and count_o == 0 and count_empty == 1:
		# xx- or -xx or x-x
		gain = 10
	if count_x == 0 and count_o == 2 and count_empty == 1:
		# oo- or -oo or o-o
		gain = -10
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
			return calculate(empty, count_x, count_o) # clear win, thus return
			win_in_previous_check = True
			break
		elif count_o == 3:
			return calculate(empty, count_x, count_o)	# clear lose, thus return
			win_in_previous_check = True
			break
		else:
			#print "here in calculate row"
			current_block_utility += calculate(empty, count_x, count_o)	# else add to current_block_utility


	if not win_in_previous_check:	
		#print "inside columns"	
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
				return calculate(empty, count_x, count_o) # clear win, thus return
				win_in_previous_check = True
				break
			elif count_o == 3:
				return calculate(empty, count_x, count_o)	# clear lose, thus return
				win_in_previous_check = True
				break
			else:
				current_block_utility += calculate(empty, count_x, count_o)	# else add to current_block_utility


	if not win_in_previous_check:
		#print "inside d1"	
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
			return calculate(empty, count_x, count_o)
			win_in_previous_check = True
		elif count_o == 3:
			return calculate(empty, count_x, count_o)
			win_in_previous_check = True
		else:	
			current_block_utility += calculate(empty, count_x, count_o)


	if not win_in_previous_check:
		#print "inside d2"
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
			return calculate(empty, count_x, count_o)
			win_in_previous_check = True
		elif count_o == 3:
			return calculate(empty, count_x, count_o)
			win_in_previous_check = True
		else:
			current_block_utility += calculate(empty, count_x, count_o)
	#print "out"		
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
def OnCenter(hx, hy, board):
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
def OnTopLeftOrBottomRight(hx, hy, board):
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
def OnTopRightOrBottomLeft(hx, hy, board):
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
def countEmpty(board, block_no):

	#print "here in count empty"
	count_x = 0;
	count_o = 0;
	count_empty = 0;

	# calculate block's starting row and column in the board in [0..9][0..9]
	block_row = block_no / 3;
	block_col = block_no % 3;
	#print "proceeding"
	# count number of - in the entire block
	for j in range(0, 3):
		#print "came here"
		for i in range(0, 3):
			if board[block_row * 3 + i][block_col * 3 + j] == '-':
				count_empty += 1
				# save that -'s coordinate 
				empty_x = block_row * 3 + i
				empty_y = block_col * 3 + j
			if board[block_row * 3 + i][block_col * 3 + j] == 'x':
				count_x += 1
			if board[block_row * 3 + i][block_col * 3 + j] == 'o':
				count_o += 1
		#print "out of inside for countempty"
	#print "after for in count empty"			
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
	##print "out of count empty"
	return 0


def checkOpponentFreeMove(board, cell_row, cell_col, block_status, player_flag):
	cells = getCells(board, block_status, (cell_row, cell_col))
	if freeMove:
		return True
	return False


def checkOpponentWinning(board, cell_row, cell_col, block_status, player_flag):
	
	# calculate cells available for opponent
	cells = getCells(board, block_status, (cell_row, cell_col))
	
	for cell in cells:
		if player_flag == 'x':
			opponent_flag = 'o'
		else:
			opponent_flag = 'x'
		
		# place the opponent flag
		board[cell[0]][cell[1]] = opponent_flag
		
		block_start_row = cell[0] - cell[0] % 3
		block_start_col = cell[1] - cell[1] % 3

		count_opponent = 0

		for i in range(0, 3):
			if board[block_start_row + i][block_start_col] == opponent_flag:
				count_opponent += 1
		if count_opponent == 3:
			board[cell[0]][cell[1]] = '-'
			#print "passed", cell_row, cell_col
			#print "opponent won in col", cell[0], cell[1]
			return True

		count_opponent = 0
		for i in range(0, 3):
			if board[block_start_row][block_start_col + i] == opponent_flag:
				count_opponent += 1
		if count_opponent == 3:
			board[cell[0]][cell[1]] = '-'
			#print "opponent won in row"
			return True

		count_opponent = 0
		if cell_row % 3 == cell_col % 3:
			for i in range(0, 3):
				if board[block_start_row + i][block_start_col + i] == opponent_flag:
					count_opponent += 1
			if count_opponent == 3:
				board[cell[0]][cell[1]] = '-'
				#print "opponent won in d1"
				return True

		count_opponent = 0
		if cell_row % 3 == 2 - cell_col % 3:
			for i in range(0, 3):
				if board[block_start_row + i][block_start_col + 2 - i] == opponent_flag:
					count_opponent += 1
			if count_opponent == 3:
				board[cell[0]][cell[1]] = '-'
				#print "opponent won in d2"
				return True

		board[cell[0]][cell[1]] = '-'

	return False

# done
def getCellUtility(board, block_status, cell_row, cell_col):
	
	board_row = cell_row - cell_row % 3;
	board_col = cell_col - cell_col % 3;
	
	utility = 0
	
	# row
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

	if count_x == 3:
			return calculate(empty, count_x, count_o)
	if count_o == 3:
			return calculate(empty, count_x, count_o)

	utility += calculate(empty, count_x, count_o)


	# column
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

	if count_x == 3:
			return calculate(empty, count_x, count_o)
	if count_o == 3:
			return calculate(empty, count_x, count_o)

	utility += calculate(empty, count_x, count_o)

	# diagnol 1
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
		
		if count_x == 3:
			return calculate(empty, count_x, count_o)
		if count_o == 3:
			return calculate(empty, count_x, count_o)
		utility += calculate(empty, count_x, count_o)

	# diagnol 2
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
		
		if count_x == 3:
			return calculate(empty, count_x, count_o)
		if count_o == 3:
			return calculate(empty, count_x, count_o)
		utility += calculate(empty, count_x, count_o)

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
	elif 1 < sum and sum < 2:
		factor = (10 - 1)
	elif 2 < sum and sum < 3:
		factor = (100 - 10)
	return factor

# done
def getUtilityValue(hsum, factor):
	value = int(pow(10, abs(int(hsum)) - 1)) + (hsum - int(hsum)) * factor
	if hsum < 0:
		return -value
	return value

# done
def checkCorners(normalized_block):
	count_us_corners = 0
	count_opponent_corners = 0
	# calculate utility of us and opponent at corners
	if normalized_block[0][0] != 'draw':
		if normalized_block[0][0] > 0:
			count_us_corners += normalized_block[0][0]
		else:
			count_opponent_corners += normalized_block[0][0]
	if normalized_block[0][2] != 'draw':	
		if normalized_block[0][2] > 0:
			count_us_corners += normalized_block[0][2]
		else:
			count_opponent_corners += normalized_block[0][2]
	if normalized_block[2][0] != 'draw':
		if normalized_block[2][0] > 0:
			count_us_corners += normalized_block[2][0]
		else:
			count_opponent_corners += normalized_block[2][0]
	if normalized_block[2][2] != 'draw':	
		if normalized_block[2][2] > 0:
			count_us_corners += normalized_block[2][2]
		else:
			count_opponent_corners += normalized_block[2][2]

	return (count_us_corners, count_opponent_corners)

# left
def check_utility(index, normalized_block):
	# called to check next block
	flag = 0
	in_flag=0

	# along rows
	if index < 3:
		for j in range(0, 3):
			if normalized_block[index][j] == -1 or normalized_block[index][j] == 1:
			 	save_value = normalized_block[index][j]
			 	save_index = j
				in_flag = 1
				break
		# we got x or o at any place, then we'll check next			
		if in_flag == 1:		
			for k in range(save_index + 1, 3):
		    		if normalized_block[index][k] == -save_value:	# opposite of what is there in our cell
		    			flag = 1 	# next is opposite of what we have
		    			break
	
	# along columns	 	   			
	elif index > 2 and index < 6:
		for j in range(0,3):
			if normalized_block[j][index-3] == -1 or normalized_block[j][index-3] == 1:
				save_value = normalized_block[j][index-3]
				save_index = j
				in_flag = 1
				break
		if in_flag==1:		
			for k in range(j, 3):
		    		if normalized_block[k][index - 3] == -save_value:
		    			flag = 1
		    			break
	elif index == 6:
		for k in range(0,3):
			if normalized_block[k][k] == -1 or normalized_block[k][k] == 1:
				save_value = normalized_block[k][k]
				in_flag = 1
				break
		if in_flag == 1: 		
			for i in range(k, 3):
				if normalized_block[i][i] == -save_value:
					flag = 1
					break

	elif index == 7:
		for k in range(0, 3):
			if normalized_block[k][2-k] == -1 or normalized_block[k][2-k] == 1:
				save_value = normalized_block[k][2-k]
				in_flag = 1
				break
		if in_flag == 1:		
			for i in range(k, 3):
				if normalized_block[i][2-i] == -save_value:
					flag = 1
					break
	# flag is 1 here, if next is opposite of what we have and hence no chance of winning
	return flag 

# done
def getBlockGlobalUtility(block_status, block_utility_array):
	# this is the whole block reprsented in 3*3

	normalized_block = [[0 for x in range(0, 3)] for x in range(0, 3)]

	for i in range(0, 9):
		x = i / 3;
		y = i % 3;
		if block_utility_array[i] == 100:
			normalized_block[x][y] = 1 			# i.e. clear win in that particular small block
		elif block_utility_array[i] == -100:
			normalized_block[x][y] = -1 		# i.e. clear lose in that particular small block
		elif block_utility_array[i] == -200:
			normalized_block[x][y] = 'draw'		# i.e. draw in that particular small block
		else:
			normalized_block[x][y] = float(block_utility_array[i]) / 100; 
	#print "ouside for"		
	utility_array = [0 for x in range(0, 8)]	# for each row, then cloumn, then diagnol1 and then diagnol2, hence (3+3+1+1 = 8)

	index = 0	# start with first row
	count_us = 0
	count_opponent = 0
	
	# going over each row/col/d1/d2 which actually are small blocks
	for i in range(0, 3):	
		# initialize sums here, we'll check for rows/cols/diagnol1/diagnol2 all here, some may get checked again -  doesn't matter
		row_sum = flag_row = flag_next_row = 0
		col_sum = flag_col = flag_next_col = 0
		d1_sum = flag_d1 = flag_next_d1 = 0
		d2_sum = flag_d2 = flag_next_d2 = 0
		# initilze draw flags here
		ultimate_win_flag = 0
		for j in range(0, 3):
			# row
			if normalized_block[i][j] == 'draw':
				flag_row = 1
			else:
				row_sum += normalized_block[i][j]
			# column
			if normalized_block[j][i] == 'draw':
				flag_col = 1
			else:
				col_sum += normalized_block[j][i]
			# diagnol1
			if normalized_block[j][j] == 'draw':
				flag_d1 = 1
			else:
				#print "diagnol 1", normalized_block[j][j]
				d1_sum += normalized_block[j][j]	
			# diagnol2	
			if normalized_block[j][2 - j] == 'draw':
				flag_d2 = 1
			else:
				d2_sum += normalized_block[j][2 - j]
			# keep count of blocks won by us and opponent
			if normalized_block[i][j] == 1:
				count_us += 1
			if normalized_block[i][j] == -1:
				count_opponent += 1
		#print row_sum, col_sum, d1_sum, d2_sum
		factor_row = calculateFactor(row_sum)
		factor_col = calculateFactor(col_sum)
		factor_d1 = calculateFactor(d1_sum)
		factor_d2 = calculateFactor(d2_sum)
		#print factor_row, factor_col, factor_d1, factor_d2
		#print "calcluted factors"
		# check conditions patiently
		# if sum of row/col/d1/d2 is 3 or -3, then clear win/lose
		if row_sum == 3 or row_sum == -3:	# clear win/lose
			ultimate_win_flag = row_sum
			break
		if col_sum == 3 or col_sum == -3:	# clear win/lose
			ultimate_win_flag = col_sum
			break
		if d1_sum == 3 or d1_sum == -3:	# clear win/lose
			ultimate_win_flag = d1_sum
			break
		if d2_sum == 3 or d2_sum == -3:	# clear win/lose
			ultimate_win_flag = d2_sum
			break
		#print "ultimare"	
		# if not, then we'll check next to that block
		if row_sum == -1 or row_sum == 1:
			flag_next_row = check_utility(index, normalized_block)
		if col_sum == -1 or col_sum == 1:
			flag_next_col = check_utility(index + 3, normalized_block)
		if d1_sum == -1 or d1_sum == 1:
			flag_next_d1 = check_utility(6, normalized_block)
		if d2_sum == -1 or d2_sum == 1:
			flag_next_d2 = check_utility(7, normalized_block)
		#print "change_utility"
		if flag_row == 1 or flag_next_row == 1:
			utility_array[index] = 0
		else:
			utility_array[index] = getUtilityValue(row_sum, factor_row)
			#print "row ", index, utility_array[index]
		if flag_col == 1 or flag_next_col == 1:
			utility_array[index + 3] = 0
		else:
			utility_array[index + 3] = getUtilityValue(col_sum, factor_col)
			#print "col ", index, utility_array[index + 3]
		if flag_d1 == 1 or flag_next_d1 == 1:
			utility_array[6] = 0
		else:
			utility_array[6] = getUtilityValue(d1_sum, factor_d1)
			#print "diagnol1 ", 6, utility_array[6]
		if flag_d2 == 1 or flag_next_d2 == 1:
			utility_array[7] = 0
		else:
			utility_array[7] = getUtilityValue(d2_sum, factor_d2)
			#print "diagnol2 ", 7, utility_array[7]
		# move to next element
		index += 1
	#print "outside whole loop"	
	return (utility_array, normalized_block, count_us, count_opponent, ultimate_win_flag)	# this is the whole block reprsented in 3*3

	normalized_block = [[0 for x in range(0, 3)] for x in range(0, 3)]

	for i in range(0, 9):
		x = i / 3;
		y = i % 3;
		if block_utility_array[i] == 100:
			normalized_block[x][y] = 1 			# i.e. clear win in that particular small block
		elif block_utility_array[i] == -100:
			normalized_block[x][y] = -1 		# i.e. clear lose in that particular small block
		elif block_utility_array[i] == -200:
			normalized_block[x][y] = 'draw'		# i.e. draw in that particular small block
		else:
			normalized_block[x][y] = float(block_utility_array[i]) / 100; 
	#print "ouside for"		
	utility_array = [0 for x in range(0, 8)]	# for each row, then cloumn, then diagnol1 and then diagnol2, hence (3+3+1+1 = 8)

	index = 0	# start with first row
	count_us = 0
	count_opponent = 0
	
	# going over each row/col/d1/d2 which actually are small blocks
	for i in range(0, 3):	
		# initialize sums here, we'll check for rows/cols/diagnol1/diagnol2 all here, some may get checked again -  doesn't matter
		row_sum = flag_row = flag_next_row = 0
		col_sum = flag_col = flag_next_col = 0
		d1_sum = flag_d1 = flag_next_d1 = 0
		d2_sum = flag_d2 = flag_next_d2 = 0
		# initilze draw flags here
		ultimate_win_flag = 0
		for j in range(0, 3):
			# row
			if normalized_block[i][j] == 'draw':
				flag_row = 1
			else:
				row_sum += normalized_block[i][j]
			# column
			if normalized_block[j][i] == 'draw':
				flag_col = 1
			else:
				col_sum += normalized_block[j][i]
			# diagnol1
			if normalized_block[j][j] == 'draw':
				flag_d1 = 1
			else:
				d1_sum += normalized_block[j][j]	
			# diagnol2	
			if normalized_block[j][2 - j] == 'draw':
				flag_d2 = 1
			else:
				d1_sum += normalized_block[j][2 - j]
			# keep count of blocks won by us and opponent
			if normalized_block[i][j] == 1:
				count_us += 1
			if normalized_block[i][j] == -1:
				count_opponent += 1
		factor_row = calculateFactor(row_sum)
		factor_col = calculateFactor(col_sum)
		factor_d1 = calculateFactor(d1_sum)
		factor_d2 = calculateFactor(d2_sum)
		#print "calcluted factors"
		# check conditions patiently
		# if sum of row/col/d1/d2 is 3 or -3, then clear win/lose
		if row_sum == 3 or row_sum == -3:	# clear win/lose
			ultimate_win_flag = row_sum
			break
		if col_sum == 3 or col_sum == -3:	# clear win/lose
			ultimate_win_flag = col_sum
			break
		if d1_sum == 3 or d1_sum == -3:	# clear win/lose
			ultimate_win_flag = d1_sum
			break
		if d2_sum == 3 or d2_sum == -3:	# clear win/lose
			ultimate_win_flag = d2_sum
			break
		#print "ultimare"	
		# if not, then we'll check next to that block
		if row_sum == -1 or row_sum == 1:
			flag_next_row = check_utility(index, normalized_block)
		if col_sum == -1 or col_sum == 1:
			flag_next_col = check_utility(index + 3, normalized_block)
		if d1_sum == -1 or d1_sum == 1:
			flag_next_d1 = check_utility(6, normalized_block)
		if d2_sum == -1 or d2_sum == 1:
			flag_next_d2 = check_utility(7, normalized_block)
		#print "change_utility"
		if flag_row == 1 or flag_next_row == 1:
			utility_array[index] = 0
		else:
			utility_array[index] = getUtilityValue(row_sum, factor_row)
		if flag_col == 1 or flag_next_col == 1:
			utility_array[index] = 0
		else:
			utility_array[index] = getUtilityValue(col_sum, factor_col)
		if flag_d1 == 1 or flag_next_d1 == 1:
			utility_array[index] = 0
		else:
			utility_array[index] = getUtilityValue(d1_sum, factor_d1)
		if flag_d2 == 1 or flag_next_d2 == 1:
			utility_array[index] = 0
		else:
			utility_array[index] = getUtilityValue(d1_sum, factor_d2)
		# move to next element
		index += 1
	#print "outside whole loop"	
	return (utility_array, normalized_block, count_us, count_opponent, ultimate_win_flag)

# done
def finalGlobalUtility(global_utility, count_us, count_opponent, count_us_corners, count_opponent_corners, ultimate_win_flag):
	
	utility_board = 0
	for k in range(0, 8):
		if ultimate_win_flag == 3 or ultimate_win_flag == -3:	# clear win/lose
			utility_board = 100 * (ultimate_win_flag) / 3
			break
		utility_board += global_utility[k]		# else need to calculate
        if ultimate_win_flag != 3 and ultimate_win_flag != -3:
        	utility_board += (count_us - count_opponent) * 10
        	utility_board += (abs(count_us_corners) - abs(count_opponent_corners)) * 5
	return utility_board


def checkCurrentPosition(board, current_row, current_col):
	
	# if corners
	if current_row in [0, 2, 3, 5, 6, 8] and current_col in [0, 2, 3, 5, 6, 8]:
		return 4
	elif current_row in [1, 4, 7] and current_col in [1, 4 ,7]:
		return -2
	return 0

# done
def check(board, block_status, current_row, current_col, player_flag):
	#print "here in check"
	block_utility = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	
	
	for block_no in range(0 ,9):
		
		current_block_utility = getEachBlockUtility(board, block_no)
		#print "after each block"
		if current_block_utility == 0:
			#print "inside count empty"
			# still zero, then we need to consider additonal effects
			# it'll be zero only in case of 'xox' or 'xo-' type rows/cols/d1/d2 
			# i.e. either 0 empty cell or 1 empty cell in the block, 
			# where we won't have any direct profit if we place there
			# then we need to check other conditions like draw and any point of putting it there or not
			current_block_utility = countEmpty(board, block_no)
		#print "after count empty"
		block_utility[block_no] = current_block_utility
	
	
	# utility specific to corners in a cell
	specific_block_utility = 0
	#block_no = 3 * ((current_row - current_row % 3) / 3) + (current_col - current_col % 3) / 3
	#specific_block_utility = checkCurrentPosition(board, current_row, current_col)
	#block_utility[block_no] += specific_block_utility
	#print "out of each block"
	cell_utility = getCellUtility(board, block_status, current_row, current_col) + specific_block_utility
	#print 'cell_utility: ', cell_utility

	(global_utility, normalized_utility, count_us, count_opponent, ultimate_win_flag) = getBlockGlobalUtility(block_status, block_utility)
	#print "global"
	(count_us_corners, count_opponent_corners) = checkCorners(normalized_utility)

	final = finalGlobalUtility(global_utility, count_us, count_opponent, count_us_corners, count_opponent_corners, ultimate_win_flag)

	
	#final += cell_utility/10
	#if checkOpponentWinning(board,current_row, current_col, block_status, player_flag):
	#	final -= 20
	
	#print "here after corners"
	# specific_block_winning_utility = 0
	# if cell_utility == 10000:
	# 	if block_no == 4:
	# 		specific_block_winning_utility = 1000
	# 	if block_no in [0, 2, 6, 8]:
	# 		specific_block_winning_utility = 800 

	##print "cell utility:", cell_utility
	##print "global utility:", globalUtility
	##print "specific utility:", specific_block_winning_utility
	#total = cell_utility / 10.0 + globalUtility + specific_block_winning_utility / 10.0
	##print "total:", total
	#print "final", final
	return final

