
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
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		elif count_o == 3:
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		else:	
			current_block_utility += calculate(empty, count_x, count_o)

	#print current_block_utility
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
			#print 'up', current_block_utility
			current_block_utility = calculate(empty, count_x, count_o)
			#print 'down', current_block_utility
			win_in_previous_check = True
		elif count_o == 3:
			current_block_utility = calculate(empty, count_x, count_o)
			win_in_previous_check = True
		else:
			current_block_utility += calculate(empty, count_x, count_o)
	#print 'about to return', current_block_utility
	# will have all the effect, if win at some time then only that part's contribution, else addition of all other values
	return current_block_utility	# final gain


def getCellUtility(board, cell_row, cell_col):
	
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

	# if checkOpponentWinning(board, cell_row, cell_col, block_status, player_flag):
	# 	utility += 0 # here -10000
	# if checkOpponentFreeMove(board, cell_row, cell_col, block_status, player_flag):
	# 	utility += 0 # here -100
	return utility

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
				print "diagnol 1", normalized_block[j][j]
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
		print row_sum, col_sum, d1_sum, d2_sum
		factor_row = calculateFactor(row_sum)
		factor_col = calculateFactor(col_sum)
		factor_d1 = calculateFactor(d1_sum)
		factor_d2 = calculateFactor(d2_sum)
		print factor_row, factor_col, factor_d1, factor_d2
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
			print "row ", index, utility_array[index]
		if flag_col == 1 or flag_next_col == 1:
			utility_array[index + 3] = 0
		else:
			utility_array[index + 3] = getUtilityValue(col_sum, factor_col)
			print "col ", index, utility_array[index + 3]
		if flag_d1 == 1 or flag_next_d1 == 1:
			utility_array[6] = 0
		else:
			utility_array[6] = getUtilityValue(d1_sum, factor_d1)
			print "diagnol1 ", 6, utility_array[6]
		if flag_d2 == 1 or flag_next_d2 == 1:
			utility_array[7] = 0
		else:
			utility_array[7] = getUtilityValue(d2_sum, factor_d2)
			print "diagnol2 ", 7, utility_array[7]
		# move to next element
		index += 1
	#print "outside whole loop"	
	return (utility_array, normalized_block, count_us, count_opponent, ultimate_win_flag)

# done
def getUtilityValue(hsum, factor):
	value = int(pow(10, abs(int(hsum)) - 1)) + (hsum - int(hsum)) * factor
	if hsum < 0:
		return -value
	return value

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
def finalGlobalUtility(global_utility, count_us, count_opponent, count_us_corners, count_opponent_corners, ultimate_win_flag):
	print global_utility, count_us, count_opponent, count_us_corners, count_opponent_corners, ultimate_win_flag
	utility_board = 0
	for k in range(0, 8):
		if ultimate_win_flag == 3 or ultimate_win_flag == -3:	# clear win/lose
			utility_board = 100 * (ultimate_win_flag) / 3
			break
		utility_board += global_utility[k]
		print utility_board		# else need to calculate
        if ultimate_win_flag != 3 and ultimate_win_flag != -3:
        	utility_board += (count_us - count_opponent) * 10
        	utility_board += (abs(count_us_corners) - abs(count_opponent_corners)) * 5
        print "after count", utility_board
	return utility_board

def checkCurrentPosition(board, current_row, current_col):
	
	# if corners
	if current_row in [0, 2, 3, 5, 6, 8] and current_col in [0, 2, 3, 5, 6, 8]:
		return 4
	return 0

def createboard1():
	board = [[ '-' for x in range(0, 9)] for x in range(0, 9)]
	# 0 block
	board[0][0] = 'x'
	board[0][1] = 'o'
	board[1][0] = 'o'
	board[2][0] = 'x'

	# 1 block
	board[0][4] = board[1][4] = 'x'
	board[0][3] = board[2][3] = board[0][5] = board[1][5] = board[2][5] = 'o'

	# 2 block
	board[0][6] = board[0][8] = board[2][6] = 'x'
	board[1][8] = 'o'

	# 3 block
	board[3][0] = 'x'	# wrong
	board[5][1] = 'x'
	board[3][1] = board[4][1] = board[5][2] = 'o'
	
	# 4 block
	board[3][5] = board[4][5] = 'x'
	board[3][3] = board[5][4] = board[5][5] = 'o'

	# 5 block
	board[3][8] = board[5][8] = board[5][7] = 'x'
	board[4][8] = 'o'

	# 6 block
	board[6][0] = board[7][1] = 'x'
	board[8][0] = 'o'

	# 7 block
	board[7][3] = board[7][4] = board[7][5] = 'x'

	# 8 block
	board[8][6] = 'o'
	board[6][6] = 'o'
	return board

def createboard():
	board = [[ '-' for x in range(0, 9)] for x in range(0, 9)]

	board[5][5] = 'x'
	board[0][5] = 'x' # wrong
	board[3][6] = 'o'
	return board
board = createboard()
block_utility = [0 for x in range(0, 9)]
for i in range(0, 9):
	block_utility[i] = getEachBlockUtility(board, i)
	print i, block_utility[i]
specific = checkCurrentPosition(board, 0, 5)
print 'specific', specific
block_utility[3] += specific

block_status = ['-' for x in range(0, 9)]
block_status[1] = 'o'
block_status[7] = 'x'

print
output1 = getBlockGlobalUtility(block_status, block_utility)
print output1
output2 = checkCorners(output1[1])
print output2
print finalGlobalUtility(output1[0], output1[2], output1[3], output2[0], output2[1], output1[4])
print getCellUtility(board, 0, 5)

