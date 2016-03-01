

class Player72:
	
	def __init__(self):
		
		pass

	def move(self,temp_board,temp_block,old_move,flag1):
		if old_move == (-1, -1):
			return (3,3)
		if(flag1 == 'x'):
			flag2 = 'o'
		else:
			flag2 = 'x'
		p_board = temp_board[:]
		p_block = temp_block[:]
		node = old_move
		limit = 4	
		#flag2 corresponds to player2's alphabet
		next_move = minimax(node,limit,-1000,1000,True,p_board[:],p_block[:],flag1,flag2,-1,-1)
		#next_move = alphabeta(node, depth, limit, a, b, True, flag1, flag2, p_board, temp_block)
		#print next_move
                
		return (next_move[1], next_move[2])



def minimax(node, depth, alpha, beta, maxnode, p_board, p_block, flag1, flag2, best_row, best_col):
	
	if depth==0 or len(compute_cells(p_board,p_block,node))==0:
		utility = check(p_board,p_block)
		if flag1 == 'o':
			return (-utility,best_row,best_col)
		
		return (utility,best_row,best_col)
	else:
		children_list = compute_cells(p_board,p_block,node)
		for child in children_list:
			if maxnode:
				p_board[child[0]][child[1]] = flag1
			else:
				p_board[child[0]][child[1]] = flag2
			if maxnode:
				score = minimax (child,depth-1,alpha,beta,False,p_board,p_block,flag1,flag2,best_row,best_col)
				if (score[0] > alpha):
	        	          alpha = score[0]
	        	          best_row = child[0]
	        	          best_col = child[1]
			else:
				score = minimax (child,depth-1,alpha,beta,True,p_board,p_block,flag1,flag2,best_row,best_col)
				if (score[0] < beta):
	        	          beta = score[0]
	        	          best_row = child[0]
	        	          best_col = child[1]
			p_board[child[0]][child[1]] = '-'
			if (alpha >= beta):
				 break
		if maxnode:
			return (alpha, best_row, best_col)
		else:
			return(beta, best_row, best_col)	               
	

def compute_cells(board,block_status,old_move):
		
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

		cells = get_empty_out_of(board, block_status, allowed_blocks)
		return cells


def get_empty_out_of(gameb,block_stat, blal):
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
	gain = 0;  #each bloack utility value
	start_x = x*3; 
	start_y = y*3;
	flag=1
	flags=0
	#countx = [0, 0, 0];
	#counto = [0, 0, 0];
	position_space_in_row = [[0 for x in range(2)] for x in range(3)] 
	position_space_in_column = [[0 for x in range(2)] for x in range(3)] 
	position_space_in_diagonal = [[0 for x in range(2)] for x in range(2)] 
	position_space_in_diagonal2 = [[0 for x in range(2)] for x in range(2)] 
	
	#
	#print block_no
	if flag == 1:
		for j in range(0,3):
			cx = 0;
			co = 0;
			cd = 0;
			for i in range(0,3):
				if board[start_x+i][start_y+j] == '-':
					cd += 1;
					position_space_in_row[j][0] = (start_x + i);
					position_space_in_row[j][1] = (start_y + j);
				if board[start_x+i][start_y+j] == 'x':
					cx += 1;
				if board[start_x+i][start_y+j] == 'o':
					co += 1;
			if cx == 3:
				gain = 100
				flag=0
				break

			elif co == 3:
				gain = -100
				flag=0
				break
			else: 
				gain = calculate(cx,cd,co,gain); #0,countx,counto);
				#print gain,'column'

	if flag == 1:
		for i in range(0,3):
			cx = 0;
			co = 0;
			cd = 0;
			for j in range(0,3):
				if board[start_x+i][start_y+j] == '-':
					cd += 1;
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
				gain = calculate(cx,cd,co,gain);#countx,counto);
				#print gain,'row'

	cx = 0;
	co = 0;
	cd = 0;
	if flag == 1:
		for i in range(0, 3):
			if board[start_x+i][start_y+i] == '-':
				cd += 1;
				position_space_in_diagonal[0][0] = (start_x + i);
				position_space_in_diagonal[0][1] = (start_y + i);
			if board[start_x+i][start_y+i] == 'o':
				co += 1;
			if board[start_x+i][start_y+i] == 'x':
				cx += 1;
		if cx == 3:
			gain = 100
		#break
		elif co == 3:
			gain = -100
	#	break
		else: 
			gain = calculate(cx,cd,co,gain); #2,countx,counto);
	#	print gain,'diagonal1'

	cx = 0;
	co = 0;
	cd = 0;
	if flag == 1:
		for i in range(0, 3):
			if board[start_x+2-i][start_y+i] == '-':
				cd += 1;
				position_space_in_diagonal2[0][0] = (start_x + i);
				position_space_in_diagonal2[0][1] = (start_y + i);
			if board[start_x+2-i][start_y+i] == 'o':
				co += 1;
			if board[start_x+2-i][start_y+i] == 'x':
				cx += 1;
		if cx == 3:
			gain = 100
	#	break
		elif co == 3:
			gain = -100
	#	break
	Final_gain = calculate(cx,cd,co,gain); #2,countx,counto);
	cx = 0;
	co = 0;
	cd = 0;
	#Utility = (countx[0]+countx[1]+countx[2])*10 + (counto[0]+counto[1]+counto[2])*-10 
	#print Final_gain#,'1234'	, start_y,start_x
	if Final_gain == 0:
		for j in range(0,3):
			
			for i in range(0,3):
				if board[start_x+i][start_y+j] == '-':
					cd += 1;
					hx = (start_x + i);
					hy = (start_y + j);
				if board[start_x+i][start_y+j] == 'x':
					cx += 1;
				if board[start_x+i][start_y+j] == 'o':
					co += 1;
		#print cx, cd, co, '!@#$%^&'
		
		vaishu = 0
		if cd == 0:
			Final_gain = -200
		#print Final_gain,'if draw == -200 or 0'
		
		if cd == 1:
			vaishu = 0
			flags = 0
			#print 'k'
			if hx%3==0 and hy%3==0:
				vaishu = new(hx, hy,Final_gain,board)
			elif hx%3 == 1 and hy % 3 == 1:
				vaishu = same(hx, hy,Final_gain,board)
			elif hx%3 == 2 and hy %3 == 2:
				vaishu = new(hx, hy,Final_gain,board)
			elif hx%3==2 and hy%3 == 0:
				vaishu=hnew(hx, hy,Final_gain,board)
			elif hx%3 == 0 and hy %3 == 2:
				vaishu = hnew(hx, hy,Final_gain,board)
			elif hx%3 == 0 and hy%3==1:
				vaishu =edge(hx, hy, Final_gain,board)

			elif hx%3==1 and hy % 3 == 0:
				vaishu = edge(hx, hy, Final_gain,board)
			elif hx%3 == 2 and hy%3 == 1:
				vaishu =edge(hx, hy, Final_gain,board)
			elif hx%3==1 and hy%3 == 2:
				vaishu = edge(hx, hy, Final_gain,board)
			#print vaishu
			
			if vaishu == 0:
				Final_gain = -200

	#print Final_gain
	if flags==1:
		Final_gain = 0
	
	return Final_gain;

def edge(hx, hy,Final_gain, board):
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
		#print 'edge',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
		#print next
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
		#print 'edge',calculate(cx, cd, co, Final_gain)
		
		next=calculate(cx, cd, co, Final_gain)
		#print next
		if next > 0:
			return next
	return 0


def same(hx, hy,Final_gain,board):
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
		#print 'same',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
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
		#print 'same',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
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
		#print 'same',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
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
		#print 'same',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next
	return 0


def new(hx, hy,Final_gain,board):
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


def hnew(hx, hy, Final_gain,board):
	cx =0
	co=0
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
		#print 'hnew', calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
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
		#print 'hnew',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
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
		#print 'hnew',calculate(cx, cd, co, Final_gain)
		next=calculate(cx, cd, co, Final_gain)
		if next > 0:
			return next
	return 0


def calculate(cx, cd, co, gain):
	
	if(cx == 2 and co == 0 and cd == 1):
		#countx[no] += 1;
		gain += 10;
	if(cx == 0 and co == 2 and cd == 1):
		#counto[no] += 1;
		gain += -10;
	if(cx == 1 and co == 0 and cd == 2):
		gain += 1;
	if(cx == 0 and co == 1 and cd == 2):
		gain -= 1;

	return gain; #(countx, counto, block_status);

def check(b,p_block):
	a = [0,0,0,0,0,0,0,0,0]

	for i in range(0, 9):
		c = check_utility(b, i);
		a[i] =  c
		
	dummy = position_space_in_row = [[0 for x in range(3)] for x in range(3)] 
	for i in range(0,9):
		x = i/3;
		y = i %3;
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
	utility=[0,0,0,0,0,0,0,0]
	cnt_n=cnt_p=dia_pos_sum=dia_neg_sum=0
	for i in range(0,3):
		sumr=0
		sumc=0
		sumd1=0
		sumd2=0
		flag_r = flag_rr=0
		flag_c = flag_cc=0
		flag_d1 = flag_dd1=0
		flag_d2= flag_dd2=0
		ultimate_flag=0
		for j in range(0,3):
	    		if dummy[i][j]=='alpha':
	    			flag_r=1        
	    		else:
	    			sumr=dummy[i][j]+sumr
	    		if dummy[j][i]=='alpha':
	    			flag_c=1
	    		else:
	    			sumc=dummy[j][i]+sumc
	    		if dummy[j][j]=='alpha':	
	    			flag_d1=1
	    		else:
	    			sumd1=dummy[j][j]+sumd1
	    			
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

	elif i == 7:
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


