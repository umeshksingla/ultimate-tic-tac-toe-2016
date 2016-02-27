class Player66:
	
	def __init__(self):
		pass

	def move(self, temp_board, temp_block, old_move, flag1):
		
		if old_move == (-1, -1):	# Initial Move
			return (3,3)
		if(flag1 == 'x'):
			flag2 = 'o'
		else:
			flag2 = 'x'
		p_board = temp_board[:]
		p_block = temp_block[:]
		node = old_move
		limit = 4	
		
		# flag2 corresponds to player2's alphabet
		# Initial alpha beta are kept to be -1000 and 1000
		# limit is the depth to which the code will search
		next_move = minimax(node, limit, -1000, 1000, True, p_board[:], p_block[:], flag1, flag2, -1, -1)
                
		return (next_move[1], next_move[2])


def minimax(node, depth, alpha, beta, maxnode, p_board, p_block, flag1, flag2, best_row, best_col):
	
	if depth==0 or len(compute_cells(p_board, p_block,node))==0:
		utility = check(p_board, p_block)
		if flag1 == 'o':
			return (-utility, best_row, best_col)
		
		return (utility, best_row, best_col)
	else:
		children_list = compute_cells(p_board,p_block,node)
		for child in children_list:
			# we'll make the move already to check utility
			if maxnode:
				p_board[child[0]][child[1]] = flag1
			else:
				p_board[child[0]][child[1]] = flag2
			if maxnode:
				score = minimax (child,depth-1,alpha,beta,False,p_board,p_block,flag1,flag2,best_row,best_col)
				if (score[0] > alpha):	# score[0] is basically utility
	        	          alpha = score[0]
	        	          best_row = child[0]
	        	          best_col = child[1]
			else:
				score = minimax (child,depth-1,alpha,beta,True,p_board,p_block,flag1,flag2,best_row,best_col)
				if (score[0] < beta):
	        	          beta = score[0]
	        	          best_row = child[0]
	        	          best_col = child[1]

	        # undo the move which was done above, since that is not the actual move
			p_board[child[0]][child[1]] = '-'
			if (alpha >= beta):
				 break
		if maxnode:
			return (alpha, best_row, best_col)
		else:
			return(beta, best_row, best_col)	               


def compute_cells(p_board,p_block,old_move):
		
		
		for_corner = [0,2,3,5,6,8]
		if(old_move == (-1,-1)):
			blocks_allowed = [0,1,2,3,4,5,6,7,8]
		#List of permitted blocks, based on old move.
		else:
			blocks_allowed  = []

			if old_move[0] in for_corner and old_move[1] in for_corner:
				## we will have 3 representative blocks, to choose from

				if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
					## top left 3 blocks are allowed
					blocks_allowed = [0, 1, 3]
				elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
					## top right 3 blocks are allowed
					blocks_allowed = [1,2,5]
				elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
					## bottom left 3 blocks are allowed
					blocks_allowed  = [3,6,7]
				elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
					### bottom right 3 blocks are allowed
					blocks_allowed = [5,7,8]
				else:
					print "SOMETHING REALLY WEIRD HAPPENED!"
					sys.exit(1)
			else:
			#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
				if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
					## upper-center block
					blocks_allowed = [1]
	
				elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
					## middle-left block
					blocks_allowed = [3]
		
				elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
					## lower-center block
					blocks_allowed = [7]

				elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
					## middle-right block
					blocks_allowed = [5]
				elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
					blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if p_block[i] != '-':
                        blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(p_board, blocks_allowed,p_block)
		return cells

def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
	        if(block_stat[idb] == '-'):
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
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

#a =minimax((0,3),4,-1000,1000,True,b[:],p_block,'x','o',-1,-1)
#print

def check_utility(board, block_no):
	
	x = block_no/3;
	y = block_no%3;
	
	gain = 0;  #each block utility value, initially zero
	start_x = x*3; 
	start_y = y*3;
	
	flag = 1 	#	used to determine whether we get any complete row/column/diagnol or not for coming cases
	flags = 0

	position_space_in_row = [[0 for x in range(2)] for x in range(3)] 
	position_space_in_column = [[0 for x in range(2)] for x in range(3)] 
	position_space_in_diagonal = [[0 for x in range(2)] for x in range(2)] 
	position_space_in_diagonal2 = [[0 for x in range(2)] for x in range(2)] 
	
	## cx, cd, co are count of x, count of -, count of o basically

	#	going over columns first
	if flag == 1:
		# iterating on 0, 1, 2
		# moving over a certain block, we are calling this function for every block separately so we're worried about only this cell
		for j in range(0,3):
			# some variables initialized here
			cx = 0;
			co = 0;
			cd = 0;
			# iterating on 0, 1, 2
			for i in range(0,3):
				# if no one is there
				if board[start_x+i][start_y+j] == '-':
					cd += 1;
					# I didn't get the next two lines
					position_space_in_row[j][0] = (start_x + i);
					position_space_in_row[j][1] = (start_y + j);
				# if x is there, increase cx value
				if board[start_x+i][start_y+j] == 'x':
					cx += 1;
				# if o is there, increase co value
				if board[start_x+i][start_y+j] == 'o':
					co += 1;

			if cx == 3:	# x will win, therefore increase the gain and break the loop
				gain = 100
				flag = 0
				break

			elif co == 3:	# o will win, therefore gain drastically decreased since it's bad for us and break the loop
				gain = -100
				flag = 0
				break
			else: 
				gain = calculate(cx, cd, co, gain); #	otherwise we need to calculate according to the given block scenario


	# only if no one was having columns [x, x, x] or [o, o, o] in the previuos if condition 
	# i.e. we needed to calculate gain using calculate() func
	#	going over rows
	if flag == 1:
		for i in range(0,3):
			cx = 0;
			co = 0;
			cd = 0;
			for j in range(0,3):
				if board[start_x+i][start_y+j] == '-':
					cd += 1;
					# I didn't get the next two lines
					position_space_in_column[i][0] = (start_x + i);
					position_space_in_column[i][1] = (start_y + j);
				if board[start_x+i][start_y+j] == 'x':
					cx += 1;
				if board[start_x+i][start_y+j] == 'o':
					co += 1;
			if cx == 3:
				gain = 100
				flag = 0
				break
			elif co == 3:
				gain = -100
				flag = 0
				break
			else: 
				gain = calculate(cx, cd, co, gain);

	# only if no one was having rows [x, x, x] or [o, o, o] in the previuos if condition 
	# i.e. we needed to calculate gain using calculate() func
	#	going over diagnol 1
	cx = 0;
	co = 0;
	cd = 0;
	if flag == 1:
		for i in range(0, 3):
			if board[start_x+i][start_y+i] == '-':
				cd += 1;
				# I didn't get the next two lines
				position_space_in_diagonal[0][0] = (start_x + i);
				position_space_in_diagonal[0][1] = (start_y + i);
			if board[start_x+i][start_y+i] == 'o':
				co += 1;
			if board[start_x+i][start_y+i] == 'x':
				cx += 1;
		if cx == 3:
			gain = 100
			# DOUBT: NEED TO CHANGE FLAG VALUE HERE and below
		elif co == 3:
			gain = -100
		else: 
			gain = calculate(cx, cd, co, gain);

	#	going over diagnol 2, only if we didn't get any cx, cd or co to be 3 in upper cases
	cx = 0;
	co = 0;
	cd = 0;
	if flag == 1:
		for i in range(0, 3):
			if board[start_x+2-i][start_y+i] == '-':
				cd += 1;
				# I didn't get the next two lines
				position_space_in_diagonal2[0][0] = (start_x + i);
				position_space_in_diagonal2[0][1] = (start_y + i);
			if board[start_x+2-i][start_y+i] == 'o':
				co += 1;
			if board[start_x+2-i][start_y+i] == 'x':
				cx += 1;
		if cx == 3:
			gain = 100
			# DOUBT: NEED TO CHANGE FLAG VALUE HERE and below
		elif co == 3:
			gain = -100
			# DOUBT: ELSE CONDITION TO BE THERE WITH calculate(..) as in above cases
			# you don't need actually since we are doing final_gain afterwards anyways

	# DOUBT: this cx, cd and co are only taking the effect of diagnol 2
	Final_gain = calculate(cx, cd, co, gain); 
	
	cx = 0
	co = 0
	cd = 0
	#	if final gain is still zero
	if Final_gain == 0:
		for j in range(0,3):
			for i in range(0,3):
				if board[start_x+i][start_y+j] == '-':
					cd += 1;
					hx = (start_x + i);		# denotes row
					hy = (start_y + j);		# denotes column
				if board[start_x+i][start_y+j] == 'x':
					cx += 1;
				if board[start_x+i][start_y+j] == 'o':
					co += 1;
		
		vaishu = 0
		if cd == 0:
			Final_gain = -200	# no point of going there, large loss
		
		if cd == 1:		# if cd == 1, it means only when one - is there 
			vaishu = 0
			flags = 0	# initially also flags was 0 though
			
			if hx%3==0 and hy%3==0:			# top left corner of a block
				vaishu = new(hx, hy, Final_gain, board)
			elif hx%3 == 1 and hy % 3 == 1: # center 
				vaishu = same(hx, hy,Final_gain,board)
			elif hx%3 == 2 and hy %3 == 2:	# bottom right corner
				vaishu = new(hx, hy,Final_gain,board)
			elif hx%3 == 2 and hy%3 == 0:	# bottom left corner
				vaishu= hnew(hx, hy,Final_gain,board)
			elif hx%3 == 0 and hy %3 == 2:	# top right corner
				vaishu = hnew(hx, hy,Final_gain,board)
			elif hx%3 == 0 and hy%3==1:		# top center
				vaishu = edge(hx, hy, Final_gain,board)
			elif hx%3==1 and hy %3 == 0:	# left center
				vaishu = edge(hx, hy, Final_gain,board)
			elif hx%3 == 2 and hy%3 == 1:	# bottom center
				vaishu = edge(hx, hy, Final_gain,board)
			elif hx%3==1 and hy%3 == 2:		# right center
				vaishu = edge(hx, hy, Final_gain,board)

			if vaishu == 0:
				Final_gain = -200


	#print Final_gain
	if flags == 1:	# It is never 1 actually
		Final_gain = 0
	
	return Final_gain;

def edge(hx, hy, Final_gain, board):
	# same as new() but only row and column of that cell are checked here
	cx=0
	co=0
	cd=0
	for i in range(0,3):
		# going over columns
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# going over row
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1		
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next
	return 0

def same(hx, hy, Final_gain, board):
	# same as new() but everyhtin gis being checked here
	cx=0
	co=0
	cd=0
	for i in range(0,3):
		# going over column
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# going over row
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# going over diagnol 1
		gx = hx - hx%3
		gy = hy - hy%3
		if board[gx+i][gy+i] == '-':
			cd += 1;
		if board[gx+i][gy+i] == 'x':
			cx += 1;
		if board[gx+i][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# going over diagnol 2
		gx = gx - gx%3
		gy = gy + gy%3
		if board[gx+i][gy-i] == '-':
			cd += 1;
		if board[gx+i][gy-i] == 'x':
			cx += 1;
		if board[gx+i][gy-i] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next
	return 0

def new(hx, hy, Final_gain, board):
	# will be only called if final gain was zero and cd was 1 somewhere: DOUBT
	cx=0
	co=0
	cd=0
	
	for i in range(0,3):
		# checking one column of a cell, the column of (gx, gy)
		# trying to get cell in (gx, gy)
		gx = hx - hx%3 		# will always be divisible by 3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		next = calculate(cx, cd, co, Final_gain)
		if next > 0:	# if some positive gain, return else need to check others
			return next

	for i in range(0,3):
		# checking one row of a cell, the row of (gx, gy)
		# trying to get cell in (gx, gy)
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# diagnol 1
		gx = hx - hx%3
		gy = hy - hy%3
		if board[gx+i][gy+i] == '-':
			cd += 1;
		if board[gx+i][gy+i] == 'x':
			cx += 1;
		if board[gx+i][gy+i] == 'o':
			co += 1
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next
	return 0

def hnew(hx, hy, Final_gain, board):
	# similar to new(), except the last for loop where unlike new, it checks for diagnol 2
	cx = 0
	co = 0
	cd = 0
	for i in range(0,3):
		# going over column
		gx = hx - hx%3
		gy = hy
		if board[gx+i][gy] == '-':
			cd += 1;
		if board[gx+i][gy] == 'x':
			cx += 1;
		if board[gx+i][gy] == 'o':
			co += 1
		
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# going over row
		gy = hy - hy%3
		gx = hx
		if board[gx][gy+i] == '-':
			cd += 1;
		if board[gx][gy+i] == 'x':
			cx += 1;
		if board[gx][gy+i] == 'o':
			co += 1
		
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next

	for i in range(0,3):
		# diagnol 2
		gx = gx - gx%3
		gy = gy + gy%3
		if board[gx+i][gy-i] == '-':
			cd += 1;
		if board[gx+i][gy-i] == 'x':
			cx += 1;
		if board[gx+i][gy-i] == 'o':
			co += 1
		
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next
	return 0

def calculate(cx, cd, co, gain):
	#	simple to understand, just some of more heuristics but not so simple
	if(cx == 2 and co == 0 and cd == 1):
		gain += 10
	elif(cx == 0 and co == 2 and cd == 1):
		gain += -10
	elif(cx == 1 and co == 0 and cd == 2):
		gain += 1
	elif(cx == 0 and co == 1 and cd == 2):
		gain -= 1
	return gain

def check(b, p_block):
	# b is current board
	a = [0, 0, 0, 0, 0, 0, 0, 0, 0]

	for i in range(0, 9):
		c = check_utility(b, i);
		a[i] =  c 	# assigning ulility of each block in order
		
	dummy = position_space_in_row = [[0 for x in range(3)] for x in range(3)]

	# dummy is kind of 3x3 block, representing whole board using utility values of each of the 9 blocks
	for i in range(0,9):
		# 
		x = i/3;
		y = i%3;
		if a[i] == 100:
			dummy[x][y] = 1
		elif a[i] == -100:
			dummy[x][y] = -1
		elif a[i] == -200:
			dummy[x][y] = 'alpha'
		else:
			dummy[x][y] = float(a[i]) / 100;

	#print dummy
	index=0
	utility=[0, 0, 0, 0, 0, 0, 0, 0]

	cnt_n = cnt_p = dia_pos_sum = dia_neg_sum = 0

	for i in range(0,3):
		sumr=0	# row
		sumc=0	# column
		sumd1=0	# diagnol 1
		sumd2=0	# diagnol 2
		flag_r = flag_rr = 0	
		flag_c = flag_cc = 0
		flag_d1 = flag_dd1 = 0
		flag_d2 = flag_dd2 = 0
		ultimate_flag = 0

		for j in range(0,3):
				# rows
	    		if dummy[i][j]=='alpha':
	    			flag_r=1        
	    		else:
	    			sumr=dummy[i][j]+sumr
	    		# columns
	    		if dummy[j][i]=='alpha':
	    			flag_c=1
	    		else:
	    			sumc=dummy[j][i]+sumc
	    		# diagnol 1	
	    		if dummy[j][j]=='alpha':	
	    			flag_d1=1
	    		else:
	    			sumd1=dummy[j][j]+sumd1
	    		# diagnol 2	
	    		if dummy[j][2-j]=='alpha':	
	    			flag_d2=1
	    		else:
	    			sumd2=dummy[j][2-j]+sumd2

	    	        if dummy[i][j]==1:
	    	        	cnt_p=cnt_p+1
	    	        if dummy[i][j]==-1:
	    	        	cnt_n=cnt_n+1

	    		factor_r=cal_factor(sumr)
	    		factor_c=cal_factor(sumc)
	    		factor_d1=cal_factor(sumd1)
	    		factor_d2=cal_factor(sumd2)
	  	 	
            
        	if sumr == -1 or sumr == 1:
        		flag_rr=change_utility(index,dummy)
        		#print "kkkkkkkkkk",flag_rr,index
		elif sumc == -1 or sumc == 1:
			flag_cc=change_utility(index+3,dummy)
		elif sumd1 == -1 or sumd1 == 1:
			flag_dd1=change_utility(6,dummy)
		elif sumd2 == -1 or sumd2 == +1:
			flag_dd2=change_utility(7,dummy)
			
		if sumr == -3 or sumr == 3:
			ultimate_flag=sumr
        		break
		elif sumc == -3 or sumc == 3:
			ultimate_flag=sumc
			break
		elif sumd1 == -3 or sumd1 == 3:
			ultimate_flag=sumd1
			break
		elif sumd2 == -3 or sumd2 == +3:
			ultimate_flag=sumd2
			break	
			

		if flag_r==1 or flag_rr==1:
			utility[index]=0
		else:	
			utility[index] = int(pow(10,abs(int(sumr))-1))+ (sumr-int(sumr))*factor_r
			if(sumr < 0 ):
				utility[index]=-utility[index]
		if flag_c==1 or flag_cc==1:
			utility[index+3]=0
		else:		
			utility[index+3] = int(pow(10,abs(int(sumc))-1)) + (sumc-int(sumc))*factor_c
			if sumc < 0:
				utility[index+3]=-utility[index+3]
		if flag_d1==1 or flag_dd1==1:
			utility[6]=0

		else:	
			utility[6] = int(pow(10,abs(int(sumd1))-1)) + (sumd1-int(sumd1))*factor_d1 
        		if sumd1 < 0:
	    			utility[6]=-utility[6]
		if flag_d2==1 or flag_dd2==1:
			utility[7]=0
		else:
			utility[7] = int(pow(10,abs(int(sumd2))-1)) + (sumd2-int(sumd2))*factor_d2
			if sumd2 < 0:
				utility[7]=-utility[7] 
		index+=1
	if dummy[0][0]!='alpha':
		if dummy[0][0]>0:
			dia_pos_sum=dia_pos_sum+dummy[0][0]
		else:
			dia_neg_sum=dia_neg_sum+dummy[0][0]
	if dummy[0][2]!='alpha':
		if dummy[0][2]>0:
			dia_pos_sum=dia_pos_sum+dummy[0][2]
		else:
			dia_neg_sum=dia_neg_sum+dummy[0][2]
	if dummy[2][0]!='alpha':	
		if dummy[2][0]>0:
			dia_pos_sum=dia_pos_sum+dummy[2][0]
		else:
			dia_neg_sum=dia_neg_sum+dummy[2][0]
	if dummy[2][2]!='alpha':	
		if dummy[2][2]>0:
			dia_pos_sum=dia_pos_sum+dummy[2][2]
		else:
			dia_neg_sum=dia_neg_sum+dummy[2][2]
						
	#print utility
	utility_board = 0
	for k in range(0,8):
		if ultimate_flag==3 or ultimate_flag==-3:
			utility_board=(100*ultimate_flag)/3
			break
		utility_board=utility[k]+utility_board
        if ultimate_flag!=3 and ultimate_flag!=-3:
        	utility_board=utility_board+(cnt_p - cnt_n)*10
        	utility_board=utility_board+(abs(dia_pos_sum)-abs(dia_neg_sum))*5
       
	return utility_board	


def change_utility(index,dummy):
	i=index;
	flag=0
	in_flag=0
	
	if i < 3:
		#print "yay",i
		for j in range(0,3):
			if dummy[i][j]==-1 or dummy[i][j]==1:
			 	value=dummy[i][j]
			 	ind=j
				#print "yayy",j
				in_flag=1
				break
				
		if in_flag==1:
			for k in range(ind+1,3):
		    		if dummy[i][k]==-value:
		    			#print "yayyyy",k
		    			flag=1
		    			break
		    			
	elif i > 2 and i < 6:
		for j in range(0,3):
			if dummy[j][i-3]==-1 or dummy[j][i-3]==1:
				value=dummy[j][i-3]
				in_flag=1
				break
		if in_flag==1:		
			for k in range(j,3):
		    		if dummy[k][i-3]==-value:
		    			flag=1
		    			break
	elif i==6:
		for k in range(0,3):
			if dummy[k][k]==-1 or dummy[k][k]==1:
				value=dummy[k][k]
				in_flag=1
				break
		if in_flag==1: 		
			for k1 in range(k,3):
				if dummy[k1][k1]==-value:
					flag=1
					break

	elif i==7:
		for k in range(0,3):
			if dummy[k][2-k]==-1 or dummy[k][2-k]==1:
				value=dummy[k][2-k]
				in_flag=1
				break
		if in_flag==1:		
			for k1 in range(k,3):
				if dummy[k1][2-k1]==-value:
					flag=1
					break
    
	return flag             

def cal_factor(sum):
	factor_f=0
	if -3 < sum and sum < -2:
		factor_f=-90
	elif -2 < sum and sum < -1:
		factor_f=-9
	elif 0 < sum and sum < 1:
		factor_f=1
        elif -1 < sum and sum < 0:
		factor_f=-1
	elif 1<sum and sum < 2:
		factor_f=9
	elif 2<sum and sum< 3:
		factor_f=90
	return factor_f

#print "HIIIIII",utility_board

