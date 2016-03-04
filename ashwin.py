''' 

This is the engine for the Ultimate TicTacToe Tournament. The code in this file is not for reproduction.
@author: Devansh Shah

The structure of the code is as below:
1. Header Files
2. Sample implementations of your class (Player and ManualPlayer)
3. Game Logic
4. Game simulator

In case of any queries, please post on moodle.iiit.ac.in

'''

import sys
import random
import signal
import time

import team72

def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    raise TimedOutExc()


class ManualPlayer:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
		print 'Enter your move: <format:row column> (you\'re playing with', flag + ")"	
		mvp = raw_input()
		mvp = mvp.split()
		return (int(mvp[0]), int(mvp[1]))

class Player1:
	
	def __init__(self):
		self.number=0
		self.ply=0
		self.n_inf=-1000000
		self.inf=1000000
		self.count=0
		# You may initialize your object here and use any variables for storing throughout the game
		pass
	
	def move(self,board,block,old_move,flag):

		##start=time.clock()
		
		self.number=self.number+1

		blocks_allowed = self.find_legal_blocks(old_move,block)

		cells = self.cells_allowed(blocks_allowed, board, block)

		ply_cells = self.cells_allowed([0,1,2,3,4,5,6,7,8], board, block)

		if flag=='o':
			player=0
		elif flag=='x':
			player=1

		# if self.number > 10:
		# 	self.ply=5
		# else:
		# 	self.ply=4

		self.ply=4

		#if len(ply_cells) < 40:
		#	print "\t\t\t\t\t\tNitrox\t"
#			self.ply=6

		self.count=0
		val_bchild=self.minimax(board,self.ply,player,cells,block,self.n_inf,self.inf)

		#elapsed=(time.clock() - start)
		#f.write("%s ->  %s (%s) %s\n\n" %(str(self.number), str(elapsed), str(len(cells)), str(self.count)))
		#print "%s ->  %s (%s)\n\n" %(str(self.number), str(elapsed), str(len(cells)))
		#print "real deal"
		#print val_bchild[0]
		return val_bchild[1]

	def show_board(self,board):
		for i in range(0,9):
			print board[i]
			if i%3==2:
				print "\n"

	def find_legal_blocks(self,old_move,block_val):
		temp_blocks_allowed=[]
		if old_move[0]%3==1 and old_move[1]%3==1:
			temp_blocks_allowed=[4]
		elif old_move[0]%3==0 and old_move[1]%3==0:
			temp_blocks_allowed=[1,3]
		elif old_move[0]%3==0 and old_move[1]%3==1:
			temp_blocks_allowed=[0,2]	
		elif old_move[0]%3==0 and old_move[1]%3==2:
			temp_blocks_allowed=[1,5]
		elif old_move[0]%3==1 and old_move[1]%3==0:
			temp_blocks_allowed=[0,6]
		elif old_move[0]%3==1 and old_move[1]%3==2:
			temp_blocks_allowed=[2,8]
		elif old_move[0]%3==2 and old_move[1]%3==0:
			temp_blocks_allowed=[3,7]
		elif old_move[0]%3==2 and old_move[1]%3==1:
			temp_blocks_allowed=[6,8]
		elif old_move[0]%3==2 and old_move[1]%3==2:
			temp_blocks_allowed=[7,5]

		blocks_allowed=[]

		for i in temp_blocks_allowed:
			if block_val[i]=='-':
				blocks_allowed.append(i)
		if old_move[0]==-1 and old_move[1]==-1:
			blocks_allowed=[4]
			print "poop"
		return blocks_allowed
		
	def cells_allowed(self, blocks_allowed, board, block):
		cells=[]

		for b in blocks_allowed:
			if block[b]=='-':
				#print "qwertt\n"
				Q=int(b/3)
				
				r=3*Q
				c=3*(b%3)
				i=r
				j=c

				while (i<r+3):
					j=c
					while (j<c+3):
						if board[i][j]=='-':
							cells.append((i,j))
						j=j+1
					i=i+1
#		print block

	
		
		if not cells:
			# print " prepottyyyyyy\n"
			Cells = self.cells_allowed([0,1,2,3,4,5,6,7,8], board, block)
			#print "\n potty"
			return Cells
		else:
			return cells

	def multiplier(self,i,j):
		old_block=int(i/3)*3+int(j/3)
		if old_block in [0,2,6,8]:
			return 5
		elif old_block==4:
			return 9
		else:
			return 1

	def multiplier2(self,i,j):
		old_block=int(i/3)*3+int(j/3)
		if old_block in [0,2,6,8]:
			return 5
		elif old_block==4:
			return 9
		else:
			return 1

	def single_block(self,board):
		score=0
		score_list=[]
		for q in range(0,9):
			rs=int(q/3)*3
			cs=(q%3)*3

			for i in range(rs,rs+3):
				for j in range(cs,cs+3):
					if board[i][j]=='x':
						score=score+0.25
					elif board[i][j]=='o':
						score=score-0.25

		
			# rows
			for l in range(0,3):
				if board[rs+l][cs]==board[rs+l][cs+1] and board[rs+l][cs+2]=='-':
					if board[rs+l][cs]=='x':
						score=score+10
					elif board[rs+l][cs]=='o':
						score=score-10

				if board[rs+l][cs]==board[rs+l][cs+2] and board[rs+l][cs+1]=='-':
					if board[rs+l][cs]=='x':
						score=score+10
					elif board[rs+l][cs]=='o':
						score=score-10

				if board[rs+l][cs+1]==board[rs+l][cs+2] and board[rs+l][cs]=='-':
					if board[rs+l][cs+1]=='x':
						score=score+10
					elif board[rs+l][cs+1]=='o':
						score=score-10

				##coloms

				if board[rs][cs+l]==board[rs+2][cs+l] and board[rs+1][cs+l]=='-':
					if board[rs][cs+l]=='x':
						score=score+10
					elif board[rs][cs+l]=='o':
						#print "reche"
						score=score-10

				if board[rs][cs+l]==board[rs+1][cs+l] and board[rs+2][cs+l]=='-':
					if board[rs][cs+l]=='x':
						score=score+10
					elif board[rs][cs+l]=='o':
						score=score-10

				if board[rs+1][cs+l]==board[rs+2][cs+l] and board[rs][cs+l]=='-':
					if board[rs+1][cs+l]=='x':
						score=score+10
					elif board[rs+1][cs+l]=='o':
						score=score-10

			## DIAGONALS

			if board[rs][cs]==board[rs+1][cs+1] and board[rs+2][cs+2]=='-':
				if board[rs][cs]=='x':
					score=score+10
				elif board[rs][cs]=='o':
					score=score-10

			if board[rs][cs]==board[rs+2][cs+2] and board[rs+1][cs+1]=='-':
				if board[rs][cs]=='x':
					score=score+10
				elif board[rs][cs]=='o':
					score=score-10

			if board[rs+1][cs+1]==board[rs+2][cs+2] and board[rs][cs]=='-':
				if board[rs+1][cs+1]=='x':
					score=score+10
				elif board[rs+1][cs+1]=='o':
					score=score-10


			if board[rs][cs+2]==board[rs+1][cs+1] and board[rs+2][cs]=='-':
				if board[rs][cs+2]=='x':
					score=score+10
				elif board[rs][cs+2]=='o':
					score=score-10

			if board[rs][cs+2]==board[rs+2][cs] and board[rs+1][cs+1]=='-':
				if board[rs][cs+2]=='x':
					score=score+10
				elif board[rs][cs+2]=='o':
					score=score-10

			if board[rs+1][cs+1]==board[rs+2][cs] and board[rs][cs+2]=='-':
				if board[rs+1][cs+1]=='x':
					score=score+10
					#print "nega\n\n\n\n\n"
				elif board[rs+1][cs+1]=='o':
					score=score-10

			score_list.append(score)
		return score_list


	def block_val(self,block,board,score_list):
		score=0
		
		#score_list=self.cells_val(board,block)
		for i in range(0,9):
			score_list[i]=score_list[i]*9
		## Single blocks
		for q in [0,3,6]:
			if block[q]=='x' and block[q+1]=='-' and block[q+2]=='-':
				score=score+1000+(1*(score_list[q+1]))+(1*(score_list[q+2]))
			elif  block[q]=='o' and block[q+1]=='-' and block[q+2]=='-':
				score=score-1000+(1*(score_list[q+1]))+(1*(score_list[q+2]))

			if block[q]=='-' and block[q+1]=='x' and block[q+2]=='-':
				score=score+1000+(1*(score_list[q]))+(1*(score_list[q+2]))
			elif  block[q]=='-' and block[q+1]=='o' and block[q+2]=='-':
				score=score-1000+(1*(score_list[q]))+(1*(score_list[q+2]))

			if block[q]=='-' and block[q+1]=='-' and block[q+2]=='x':
				
				score=score+1000+(1*(score_list[q]))+(1*(score_list[q+1]))
			elif  block[q]=='-' and block[q+1]=='-' and block[q+2]=='o':
				score=score-1000+(1*(score_list[q]))+(1*(score_list[q+1]))

		for q in [0,1,2]:
			if block[q]=='x' and block[q+1]=='-' and block[q+2]=='-':
				score=score+1000+(1*(score_list[q+1]))+(1*(score_list[q+2]))
			elif  block[q]=='o' and block[q+1]=='-' and block[q+2]=='-':
				score=score-1000+(1*(score_list[q+1]))+(1*(score_list[q+2]))

			if block[q]=='-' and block[q+1]=='x' and block[q+2]=='-':
				score=score+1000+(1*(score_list[q]))+(1*(score_list[q+2]))
			elif  block[q]=='-' and block[q+1]=='o' and block[q+2]=='-':
				score=score-1000+(1*(score_list[q]))+(1*(score_list[q+2]))

			if block[q]=='-' and block[q+1]=='-' and block[q+2]=='x':
				score=score+1000+(1*(score_list[q]))+(1*(score_list[q+1]))
			elif  block[q]=='-' and block[q+1]=='-' and block[q+2]=='o':
				score=score-1000+(1*(score_list[q]))+(1*(score_list[q+1]))

		# two blocks in a row
		for q in [0,3,6]:
			if block[q]==block[q+1] and block[q+2]=='-':
				if block[q]=='x':
					score=score+100000+(1*(score_list[q+2]))
				elif block[q]=='o':
					score=score-100000+(1*(score_list[q+2]))
			if block[q]==block[q+2] and block[q+1]=='-':
				if block[q]=='x':
					score=score+100000+(1*(score_list[q+1]))
				elif block[q]=='o':
					score=score-100000+(1*(score_list[q+1]))
			if block[q+1]==block[q+2] and block[q]=='-':
				if block[q+1]=='x':
					score=score+100000+(1*(score_list[q]))
				elif block[q+1]=='o':
					score=score-100000+(1*(score_list[q]))
		## two blocks in a colomn
		for q in [0,1,2]:
			if block[q]==block[q+3] and block[q+6]=='-':
				if block[q]=='x':
					score=score+100000+(1*(score_list[q+6]))
				elif block[q]=='o':
					score=score-100000+(1*(score_list[q+6]))
			if block[q]==block[q+6] and block[q+3]=='-':
				if block[q]=='x':
					score=score+100000+(1*(score_list[q+3]))
				elif block[q]=='o':
					score=score-100000+(1*(score_list[q+3]))
			if block[q+3]==block[q+6] and block[q]=='-':
				if block[q+3]=='x':
					score=score+100000+(1*(score_list[q]))
				elif block[q+3]=='o':
					score=score-100000+(1*(score_list[q]))

	## Checking diagonal doubles
		if block[0]==block[4] and block[8]=='-':
			if block[0]=='x':
				score=score+100000+(1*(score_list[8]))
			elif block[0]=='o':
				score=score-100000+(1*(score_list[8]))
		if block[0]==block[8] and block[4]=='-':
			if block[0]=='x':
				score=score+100000+(1*(score_list[4]))
			elif block[0]=='o':
				score=score-100000+(1*(score_list[4]))
		if block[4]==block[8] and block[0]=='-':
			if block[4]=='x':
				score=score+100000+(1*(score_list[0]))
			elif block[4]=='o':
				score=score-100000+(1*(score_list[0]))


		if block[2]==block[4] and block[6]=='-':
			if block[2]=='x':
				score=score+100000+(1*(score_list[6]))
			elif block[2]=='o':
				score=score-100000+(1*(score_list[6]))
		if block[2]==block[6] and block[4]=='-':
			if block[2]=='x':
				score=score+100000+(1*(score_list[4]))
			elif block[2]=='o':
				score=score-100000+(1*(score_list[4]))
		if block[4]==block[6] and block[2]=='-':
			if block[4]=='x':
				score=score+100000+(1*(score_list[2]))
			elif block[4]=='o':
				score=score-100000+(1*(score_list[2]))

		##Checking diagonal singles

		if block[0]=='x' and block[4]=='-' and block[8]=='-':
			score=score+1000+(1*(score_list[4]))+(1*(score_list[8]))
		elif block[0]=='o' and block[4]=='-' and block[8]=='-':
			score=score-1000+(1*(score_list[4]))+(1*(score_list[8]))

		if block[0]=='-' and block[4]=='x' and block[8]=='-':
			score=score+1000+(1*(score_list[0]))+(1*(score_list[8]))
		elif block[0]=='-' and block[4]=='o' and block[8]=='-':
			score=score-1000+(1*(score_list[0]))+(1*(score_list[8]))

		if block[0]=='-' and block[4]=='-' and block[8]=='x':
			score=score+1000+(1*(score_list[0]))+(1*(score_list[4]))
		elif block[0]=='-' and block[4]=='-' and block[8]=='o':
			score=score-1000+(1*(score_list[0]))+(1*(score_list[4]))

			##Other diagonal
		if block[2]=='x' and block[4]=='-' and block[6]=='-':
			score=score+1000+(1*(score_list[6]))+(1*(score_list[4]))
		elif block[2]=='o' and block[4]=='-' and block[6]=='-':
			score=score-1000+(1*(score_list[6]))+(1*(score_list[4]))

		if block[2]=='-' and block[4]=='x' and block[6]=='-':
			score=score+1000+(1*(score_list[2]))+(1*(score_list[6]))
		elif block[2]=='-' and block[4]=='o' and block[6]=='-':
			score=score-1000+(1*(score_list[2]))+(1*(score_list[6]))

		if block[2]=='-' and block[4]=='-' and block[6]=='x':
			score=score+1000+(1*(score_list[2]))+(1*(score_list[4]))
		elif block[2]=='-' and block[4]=='-' and block[6]=='o':
			score=score-1000+(1*(score_list[2]))+(1*(score_list[4]))

		return score

	

	def cells_val(self,board,block):
		score=0
		siscore=0
		score_list=[]
		for q in range(0,9):
			rs=int(q/3)*3
			cs=(q%3)*3
			siscore=0


			for i in range(rs,rs+3):
				for j in range(cs,cs+3):
					if board[i][j]=='x':
						score=score+(0.01*self.multiplier(i,j))
						siscore=siscore+0.25
					elif board[i][j]=='o':
						score=score-(0.01*self.multiplier(i,j))
						siscore=siscore-0.25

			 # if board[rs][cs]=='x' :
			 # 	score=score+3
			 # 	#print score
			 # if board[rs+1][cs+1]=='o':
			 # 	score=score-3

			# rows
			for l in range(0,3):
				if board[rs+l][cs]==board[rs+l][cs+1] and board[rs+l][cs+2]=='-':
					if board[rs+l][cs]=='x':
						score=score+(0.5*self.multiplier(rs+l,cs))
						siscore=siscore+10
					elif board[rs+l][cs]=='o':
						score=score-(0.5*self.multiplier(rs+l,cs))
						siscore=siscore-10
				if board[rs+l][cs]==board[rs+l][cs+2] and board[rs+l][cs+1]=='-':
					if board[rs+l][cs]=='x':
						score=score+(0.5*self.multiplier(rs+l,cs))
						siscore=siscore+10
					elif board[rs+l][cs]=='o':
						score=score-(0.5*self.multiplier(rs+l,cs))
						siscore=siscore-10

				if board[rs+l][cs+1]==board[rs+l][cs+2] and board[rs+l][cs]=='-':
					if board[rs+l][cs+1]=='x':
						score=score+(0.5*self.multiplier(rs+l,cs+1))
						siscore=siscore+10
					elif board[rs+l][cs+1]=='o':
						score=score-(0.5*self.multiplier(rs+l,cs+1))
						siscore=siscore-10

				##coloms

				if board[rs][cs+l]==board[rs+2][cs+l] and board[rs+1][cs+l]=='-':
					if board[rs][cs+l]=='x':
						score=score+(0.5*self.multiplier(rs,cs+l))
						siscore=siscore+10
					elif board[rs][cs+l]=='o':
						#print "reche"
						score=score-(0.5*self.multiplier(rs,cs+l))
						siscore=siscore-10

				if board[rs][cs+l]==board[rs+1][cs+l] and board[rs+2][cs+l]=='-':
					if board[rs][cs+l]=='x':
						score=score+(0.5*self.multiplier(rs,cs+l))
						siscore=siscore+10
					elif board[rs][cs+l]=='o':
						score=score-(0.5*self.multiplier(rs,cs+l))
						siscore=siscore-10

				if board[rs+1][cs+l]==board[rs+2][cs+l] and board[rs][cs+l]=='-':
					if board[rs+1][cs+l]=='x':
						score=score+(0.5*self.multiplier(rs+1,cs+l))
						siscore=siscore+10
					elif board[rs+1][cs+l]=='o':
						score=score-(0.5*self.multiplier(rs+1,cs+l))
						siscore=siscore-10

			## DIAGONALS

			if board[rs][cs]==board[rs+1][cs+1] and board[rs+2][cs+2]=='-':
				if board[rs][cs]=='x':
					score=score+(0.5*self.multiplier(rs,cs))
					siscore=siscore+10
				elif board[rs][cs]=='o':
					score=score-(0.5*self.multiplier(rs,cs))
					siscore=siscore-10

			if board[rs][cs]==board[rs+2][cs+2] and board[rs+1][cs+1]=='-':
				if board[rs][cs]=='x':
					score=score+(0.5*self.multiplier(rs,cs))
					siscore=siscore+10
				elif board[rs][cs]=='o':
					score=score-(0.5*self.multiplier(rs,cs))
					siscore=siscore-10

			if board[rs+1][cs+1]==board[rs+2][cs+2] and board[rs][cs]=='-':
				if board[rs+1][cs+1]=='x':
					score=score+(0.5*self.multiplier(rs+1,cs+1))
					siscore=siscore+10
				elif board[rs+1][cs+1]=='o':
					score=score-(0.5*self.multiplier(rs+1,cs+1))
					siscore=siscore-10


			if board[rs][cs+2]==board[rs+1][cs+1] and board[rs+2][cs]=='-':
				if board[rs][cs+2]=='x':
					score=score+(0.5*self.multiplier(rs,cs+2))
					siscore=siscore+10
				elif board[rs][cs+2]=='o':
					score=score-(0.5*self.multiplier(rs,cs+2))
					siscore=siscore-10

			if board[rs][cs+2]==board[rs+2][cs] and board[rs+1][cs+1]=='-':
				if board[rs][cs+2]=='x':
					score=score+(0.5*self.multiplier(rs,cs+2))
					siscore=siscore+10
				elif board[rs][cs+2]=='o':
					score=score-(0.5*self.multiplier(rs,cs+2))
					siscore=siscore-10

			if board[rs+1][cs+1]==board[rs+2][cs] and board[rs][cs+2]=='-':
				if board[rs+1][cs+1]=='x':
					score=score+(0.5*self.multiplier(rs+1,cs+1))
					siscore=siscore+10
					#print "nega\n\n\n\n\n"
				elif board[rs+1][cs+1]=='o':
					score=score-(0.5*self.multiplier(rs+1,cs+1))
					siscore=siscore-10


			score_list.append(siscore)

		#print score 
		#print "cells"
		
		milist=[score,score_list]
		return milist

	def eval(self,board,maxiplayer,block):
		##Check individual blocks
		score=0
		tscore=[]
		tscore=self.cells_val(board,block)
		score=score+tscore[0]				
		score=score+self.block_val(block,board,tscore[1])
		#print score
		
				
		#self.show_board(board)
		return score
		
	def end_game(self,block,board):
		flag=0
		tflag=-1
		for i in range(0,3):
			if i < 3:
				if block[i]==block[i+3] and block[i]==block[i+6] and block[i]!='-' and block[i]!='D':
					flag=1
					break
		if flag!=1:
			for i in [0,3,6]:
				if block[i]==block[i+1] and block[i]==block[i+2] and block[i]!='-' and block[i]!='D':
					flag=1
					break

		i=4
		if block[i]==block[i+4] and block[i]==block[i-4] and block[i]!='-' and block[i]!='D' and flag!=1:
			flag=1

		if block[i]==block[i+2] and block[i]==block[i-2] and block[i]!='-' and block[i]!='D' and flag!=1:
			flag=1

		for i in range(0,9):
			if block[i]=='-':
				tflag=0
		if tflag==-1 and flag==0:
			xcount=0
			ocount=0
			for i in range(0,9):
				if block[i]=='x':
					xcount=xcount+1
				elif block[i]=='o':
					ocount=ocount+1

			if xcount>ocount:
				return 10000000
			elif ocount>xcount:
				return -10000000
			else:
				xcount=0
				ocount=0
				for q in range(0,9):
					rs=int(q/3)*3
					cs=(q%3)*3
					if board[rs+1][cs+1]=='x':
						xcount=xcount+1
					elif board[rs+1][cs+1]=='o':
						ocount=ocount+1
				if xcount>ocount:
					return 10000000
				elif xcount<ocount:
					return -10000000
				else:
					return 2
		else:
			return flag

	def update_block(self,board,block,maxiplayer,old_move):

		old_block=int(old_move[0]/3)*3+int(old_move[1]/3)
		t1=int(old_block/3)*3
		t2=(old_block%3)*3

		flag=0
		tflag=0

		if board[t1][t2]==board[t1+1][t2+1] and board[t1][t2]==board[t1+2][t2+2] and board[t1][t2]!='-':
			#print 1
			flag=1

		if board[t1][t2+2]==board[t1+1][t2+1] and board[t1][t2+2]==board[t1+2][t2] and board[t1+2][t2]!='-':
			flag=1
			#print 2


		if flag!=1:
			for i in range(t1,t1+3):
				if board[i][t2]==board[i][t2+1] and board[i][t2]==board[i][t2+2] and board[i][t2]!='-':
					flag=1
					#print 3


		if flag!=1:
			for i in range(t2,t2+3):
				if board[t1][i]==board[t1+1][i] and board[t1][i]==board[t1+2][i] and board[t1][i]!='-':
					flag=1
					#print 4

		if flag==1:
			block[old_block]=maxiplayer
			return old_block

		else:
			for i in range(t1,t1+3):
				for j in range(t2,t2+3):
					if board[i][j]=='-':
						tflag=1
			if tflag==0:
				block[old_block]='D'
			return old_block

		####print block

#	def win_check():

	def minimax(self,board,depth,maxiplayer,cells_allowed,block,alpha,beta):
		#check for terminal node

		if depth == 0:
			return [self.eval(board,maxiplayer,block),[-2,-2]]

		#children=genchildren(board,cells_allowed)
		temp=[]
		if maxiplayer==1:
			bestval=-100000000
			best_child=cells_allowed[0]
			for child in cells_allowed:
				board[child[0]][child[1]]='x'
				old_move=child
				#self.show_board(board)
				#block update
				revert_old=self.update_block(board,block,'x',old_move)

				check_game=self.end_game(block,board)
				if check_game==1:
					#print "kaka"
					temp=[10000000,child]
				elif check_game!=0:
					#print "kaka"

					temp=[check_game,child]
				elif check_game==0:
					blocks_allowed = self.find_legal_blocks(old_move,block)
					new_allow = self.cells_allowed(blocks_allowed, board, block)
					#if alpha<beta:
					temp=self.minimax(board,depth-1,0,new_allow,block,alpha,beta)
									
				board[child[0]][child[1]]='-'
				block[revert_old]='-'
				
				if temp[0] > bestval:
					best_child=child
					bestval=temp[0]
				#if child==cells_allowed[-1]:
					#print "max"
					#print bestval
				alpha = bestval
			#print "poop"
			#print bestval
			#print best_child

			return (bestval,best_child)

		else:
			bestval=100000000
			best_child=cells_allowed[0]
			for child in cells_allowed:
				
				board[child[0]][child[1]]='o'
				old_move=child
				
				#self.show_board(board)
				#block update
				revert_old=self.update_block(board,block,'o',old_move)
				#print block
				check_game=self.end_game(block,board)
				if check_game==1:
					#print "kaka"
					temp=[-10000000,child]
				elif check_game!=0:
					#print "kaka"
					temp= [check_game,child]
				elif check_game==0:
					blocks_allowed = self.find_legal_blocks(old_move,block)
					new_allow = self.cells_allowed(blocks_allowed, board, block)
					#if alpha<beta:
					temp=self.minimax(board,depth-1,1,new_allow,block,alpha,beta)

						# print self.count
				board[child[0]][child[1]]='-'
				block[revert_old]='-'

				if temp[0] < bestval:
					best_child=child
					bestval=temp[0]

				#if child==cells_allowed[-1]:
					#print "min"

					#print bestval

				beta = bestval
				#print "This is max"
				#print bestval


			return (bestval,best_child)

class Player2:
	
	def __init__(self):
		self.number=0
		self.ply=0
		self.n_inf=-1000000
		self.inf=1000000
		self.count=0
		# You may initialize your object here and use any variables for storing throughout the game
		pass
	
	def move(self,board,block,old_move,flag):

		#start=time.clock()
		
		self.number=self.number+1

		blocks_allowed = self.find_legal_blocks(old_move,block)

		cells = self.cells_allowed(blocks_allowed, board, block)

		ply_cells = self.cells_allowed([0,1,2,3,4,5,6,7,8], board, block)

		if flag=='o':
			player=0
		elif flag=='x':
			player=1

		# if self.number > 10:
		# 	self.ply=5
		# else:
		# 	self.ply=4

		self.ply=4

		#if len(ply_cells) < 40:
		#	print "\t\t\t\t\t\tNitrox\t"
#			self.ply=6

		self.count=0
		val_bchild=self.minimax(board,self.ply,player,cells,block,self.n_inf,self.inf)

		#elapsed=(time.clock() - start)
		#f.write("%s ->  %s (%s) %s\n\n" %(str(self.number), str(elapsed), str(len(cells)), str(self.count)))
		#print "%s ->  %s (%s)\n\n" %(str(self.number), str(elapsed), str(len(cells)))
		#print "real deal"
		#print val_bchild[0]
		return val_bchild[1]

	def show_board(self,board):
		for i in range(0,9):
			print board[i]
			if i%3==2:
				print "\n"

	def find_legal_blocks(self,old_move,block_val):
		temp_blocks_allowed=[]
		if old_move[0]%3==1 and old_move[1]%3==1:
			temp_blocks_allowed=[4]
		elif old_move[0]%3==0 and old_move[1]%3==0:
			temp_blocks_allowed=[1,3]
		elif old_move[0]%3==0 and old_move[1]%3==1:
			temp_blocks_allowed=[0,2]	
		elif old_move[0]%3==0 and old_move[1]%3==2:
			temp_blocks_allowed=[1,5]
		elif old_move[0]%3==1 and old_move[1]%3==0:
			temp_blocks_allowed=[0,6]
		elif old_move[0]%3==1 and old_move[1]%3==2:
			temp_blocks_allowed=[2,8]
		elif old_move[0]%3==2 and old_move[1]%3==0:
			temp_blocks_allowed=[3,7]
		elif old_move[0]%3==2 and old_move[1]%3==1:
			temp_blocks_allowed=[6,8]
		elif old_move[0]%3==2 and old_move[1]%3==2:
			temp_blocks_allowed=[7,5]

		blocks_allowed=[]

		for i in temp_blocks_allowed:
			if block_val[i]=='-':
				blocks_allowed.append(i)
		if old_move[0]==-1 and old_move[1]==-1:
			blocks_allowed=[4]
			print "poop"
		return blocks_allowed
		
	def cells_allowed(self, blocks_allowed, board, block):
		cells=[]

		for b in blocks_allowed:
			if block[b]=='-':
				#print "qwertt\n"
				Q=int(b/3)
				
				r=3*Q
				c=3*(b%3)
				i=r
				j=c

				while (i<r+3):
					j=c
					while (j<c+3):
						if board[i][j]=='-':
							cells.append((i,j))
						j=j+1
					i=i+1
#		print block

	
		
		if not cells:
			# print " prepottyyyyyy\n"
			Cells = self.cells_allowed([0,1,2,3,4,5,6,7,8], board, block)
			#print "\n potty"
			return Cells
		else:
			return cells

	def block_val(self,block):
		score=0
		## Single blocks
		for q in [0,3,6]:
			if block[q]=='x' and block[q+1]=='-' and block[q+2]=='-':
				score=score+100
			elif  block[q]=='o' and block[q+1]=='-' and block[q+2]=='-':
				score=score-100

			if block[q]=='-' and block[q+1]=='x' and block[q+2]=='-':
				score=score+100
			elif  block[q]=='-' and block[q+1]=='o' and block[q+2]=='-':
				score=score-100

			if block[q]=='-' and block[q+1]=='-' and block[q+2]=='x':
				
				score=score+100
			elif  block[q]=='-' and block[q+1]=='-' and block[q+2]=='o':
				score=score-100

		for q in [0,1,2]:
			if block[q]=='x' and block[q+1]=='-' and block[q+2]=='-':
				score=score+100
			elif  block[q]=='o' and block[q+1]=='-' and block[q+2]=='-':
				score=score-100

			if block[q]=='-' and block[q+1]=='x' and block[q+2]=='-':
				score=score+100
			elif  block[q]=='-' and block[q+1]=='o' and block[q+2]=='-':
				score=score-100

			if block[q]=='-' and block[q+1]=='-' and block[q+2]=='x':
				score=score+100
			elif  block[q]=='-' and block[q+1]=='-' and block[q+2]=='o':
				score=score-100

		# two blocks in a row
		for q in [0,3,6]:
			if block[q]==block[q+1] and block[q+2]=='-':
				if block[q]=='x':
					score=score+10000
				elif block[q]=='o':
					score=score-10000
			if block[q]==block[q+2] and block[q+1]=='-':
				if block[q]=='x':
					score=score+10000
				elif block[q]=='o':
					score=score-10000
			if block[q+1]==block[q+2] and block[q]=='-':
				if block[q+1]=='x':
					score=score+10000
				elif block[q+1]=='o':
					score=score-10000
		## two blocks in a colomn
		for q in [0,1,2]:
			if block[q]==block[q+3] and block[q+6]=='-':
				if block[q]=='x':
					score=score+10000
				elif block[q]=='o':
					score=score-10000
			if block[q]==block[q+6] and block[q+3]=='-':
				if block[q]=='x':
					score=score+10000
				elif block[q]=='o':
					score=score-10000
			if block[q+3]==block[q+6] and block[q]=='-':
				if block[q+3]=='x':
					score=score+10000
				elif block[q+3]=='o':
					score=score-10000

	## Checking diagonal doubles
		if block[0]==block[4] and block[8]=='-':
			if block[0]=='x':
				score=score+10000
			elif block[0]=='o':
				score=score-10000
		if block[0]==block[8] and block[4]=='-':
			if block[0]=='x':
				score=score+10000
			elif block[0]=='o':
				score=score-10000
		if block[4]==block[8] and block[0]=='-':
			if block[4]=='x':
				score=score+10000
			elif block[4]=='o':
				score=score-10000


		if block[2]==block[4] and block[6]=='-':
			if block[2]=='x':
				score=score+10000
			elif block[2]=='o':
				score=score-10000
		if block[2]==block[6] and block[4]=='-':
			if block[2]=='x':
				score=score+10000
			elif block[2]=='o':
				score=score-10000
		if block[4]==block[6] and block[2]=='-':
			if block[4]=='x':
				score=score+10000
			elif block[4]=='o':
				score=score-10000

		##Checking diagonal singles

		if block[0]=='x' and block[4]=='-' and block[8]=='-':
			score=score+100
		elif block[0]=='o' and block[4]=='-' and block[8]=='-':
			score=score-100

		if block[0]=='-' and block[4]=='x' and block[8]=='-':
			score=score+100
		elif block[0]=='-' and block[4]=='o' and block[8]=='-':
			score=score-100

		if block[0]=='-' and block[4]=='-' and block[8]=='x':
			score=score+100
		elif block[0]=='-' and block[4]=='-' and block[8]=='o':
			score=score-100

			##Other diagonal
		if block[2]=='x' and block[4]=='-' and block[6]=='-':
			score=score+100
		elif block[2]=='o' and block[4]=='-' and block[6]=='-':
			score=score-100

		if block[2]=='-' and block[4]=='x' and block[6]=='-':
			score=score+100
		elif block[2]=='-' and block[4]=='o' and block[6]=='-':
			score=score-100

		if block[2]=='-' and block[4]=='-' and block[6]=='x':
			score=score+100
		elif block[2]=='-' and block[4]=='-' and block[6]=='o':
			score=score-100

		return score

	def multiplier(self,i,j):
		old_block=int(i/3)*3+int(j/3)
		if old_block in [0,2,6,8]:
			return 5
		elif old_block==4:
			return 9
		else:
			return 1

	def cells_val(self,board,block):
		score=0
		for q in range(0,9):
			rs=int(q/3)*3
			cs=(q%3)*3

			for i in range(rs,rs+3):
				for j in range(cs,cs+3):
					if board[i][j]=='x':
						score=score+(0.25*self.multiplier(i,j))
					elif board[i][j]=='o':
						score=score-(0.25*self.multiplier(i,j))

			 # if board[rs][cs]=='x' :
			 # 	score=score+3
			 # 	#print score
			 # if board[rs+1][cs+1]=='o':
			 # 	score=score-3

			# rows
			for l in range(0,3):
				if board[rs+l][cs]==board[rs+l][cs+1] and board[rs+l][cs+2]=='-':
					if board[rs+l][cs]=='x':
						score=score+(10*self.multiplier(rs+l,cs))
					elif board[rs+l][cs]=='o':
						score=score-(10*self.multiplier(rs+l,cs))

				if board[rs+l][cs]==board[rs+l][cs+2] and board[rs+l][cs+1]=='-':
					if board[rs+l][cs]=='x':
						score=score+(10*self.multiplier(rs+l,cs))
					elif board[rs+l][cs]=='o':
						score=score-(10*self.multiplier(rs+l,cs))

				if board[rs+l][cs+1]==board[rs+l][cs+2] and board[rs+l][cs]=='-':
					if board[rs+l][cs+1]=='x':
						score=score+(10*self.multiplier(rs+l,cs+1))
					elif board[rs+l][cs+1]=='o':
						score=score-(10*self.multiplier(rs+l,cs+1))

				##coloms

				if board[rs][cs+l]==board[rs+2][cs+l] and board[rs+1][cs+l]=='-':
					if board[rs][cs+l]=='x':
						score=score+(10*self.multiplier(rs,cs+l))
					elif board[rs][cs+l]=='o':
						#print "reche"
						score=score-(10*self.multiplier(rs,cs+l))

				if board[rs][cs+l]==board[rs+1][cs+l] and board[rs+2][cs+l]=='-':
					if board[rs][cs+l]=='x':
						score=score+(10*self.multiplier(rs,cs+l))
					elif board[rs][cs+l]=='o':
						score=score-(10*self.multiplier(rs,cs+l))

				if board[rs+1][cs+l]==board[rs+2][cs+l] and board[rs][cs+l]=='-':
					if board[rs+1][cs+l]=='x':
						score=score+(10*self.multiplier(rs+1,cs+l))
					elif board[rs+1][cs+l]=='o':
						score=score-(10*self.multiplier(rs+1,cs+l))

			## DIAGONALS

			if board[rs][cs]==board[rs+1][cs+1] and board[rs+2][cs+2]=='-':
				if board[rs][cs]=='x':
					score=score+(10*self.multiplier(rs,cs))
				elif board[rs][cs]=='o':
					score=score-(10*self.multiplier(rs,cs))

			if board[rs][cs]==board[rs+2][cs+2] and board[rs+1][cs+1]=='-':
				if board[rs][cs]=='x':
					score=score+(10*self.multiplier(rs,cs))
				elif board[rs][cs]=='o':
					score=score-(10*self.multiplier(rs,cs))

			if board[rs+1][cs+1]==board[rs+2][cs+2] and board[rs][cs]=='-':
				if board[rs+1][cs+1]=='x':
					score=score+(10*self.multiplier(rs+1,cs+1))
				elif board[rs+1][cs+1]=='o':
					score=score-(10*self.multiplier(rs+1,cs+1))


			if board[rs][cs+2]==board[rs+1][cs+1] and board[rs+2][cs]=='-':
				if board[rs][cs+2]=='x':
					score=score+(10*self.multiplier(rs,cs+2))
				elif board[rs][cs+2]=='o':
					score=score-(10*self.multiplier(rs,cs+2))

			if board[rs][cs+2]==board[rs+2][cs] and board[rs+1][cs+1]=='-':
				if board[rs][cs+2]=='x':
					score=score+(10*self.multiplier(rs,cs+2))
				elif board[rs][cs+2]=='o':
					score=score-(10*self.multiplier(rs,cs+2))

			if board[rs+1][cs+1]==board[rs+2][cs] and board[rs][cs+2]=='-':
				if board[rs+1][cs+1]=='x':
					score=score+(10*self.multiplier(rs+1,cs+1))
					#print "nega\n\n\n\n\n"
				elif board[rs+1][cs+1]=='o':
					score=score-(10*self.multiplier(rs+1,cs+1))

		#print score 
		#print "cells"
		return score

	def eval(self,board,maxiplayer,block):
		##Check individual blocks
		score=0
		
		score=score+self.block_val(block)+self.cells_val(board,block)
				
		#print score
		
				
		#self.show_board(board)
		return score
		
	def end_game(self,block,board):
		flag=0
		tflag=-1
		for i in range(0,3):
			if i < 3:
				if block[i]==block[i+3] and block[i]==block[i+6] and block[i]!='-' and block[i]!='D':
					flag=1
					break
		if flag!=1:
			for i in [0,3,6]:
				if block[i]==block[i+1] and block[i]==block[i+2] and block[i]!='-' and block[i]!='D':
					flag=1
					break

		i=4
		if block[i]==block[i+4] and block[i]==block[i-4] and block[i]!='-' and block[i]!='D' and flag!=1:
			flag=1

		if block[i]==block[i+2] and block[i]==block[i-2] and block[i]!='-' and block[i]!='D' and flag!=1:
			flag=1

		for i in range(0,9):
			if block[i]=='-':
				tflag=0
		if tflag==-1 and flag==0:
			xcount=0
			ocount=0
			for i in range(0,9):
				if block[i]=='x':
					xcount=xcount+1
				elif block[i]=='o':
					ocount=ocount+1

			if xcount>ocount:
				return 10000000
			elif ocount>xcount:
				return -10000000
			else:
				xcount=0
				ocount=0
				for q in range(0,9):
					rs=int(q/3)*3
					cs=(q%3)*3
					if board[rs+1][cs+1]=='x':
						xcount=xcount+1
					elif board[rs+1][cs+1]=='o':
						ocount=ocount+1
				if xcount>ocount:
					return 10000000
				elif xcount<ocount:
					return -10000000
				else:
					return 2
		else:
			return flag

	def update_block(self,board,block,maxiplayer,old_move):

		old_block=int(old_move[0]/3)*3+int(old_move[1]/3)
		t1=int(old_block/3)*3
		t2=(old_block%3)*3

		flag=0
		tflag=0

		if board[t1][t2]==board[t1+1][t2+1] and board[t1][t2]==board[t1+2][t2+2] and board[t1][t2]!='-':
			#print 1
			flag=1

		if board[t1][t2+2]==board[t1+1][t2+1] and board[t1][t2+2]==board[t1+2][t2] and board[t1+2][t2]!='-':
			flag=1
			#print 2


		if flag!=1:
			for i in range(t1,t1+3):
				if board[i][t2]==board[i][t2+1] and board[i][t2]==board[i][t2+2] and board[i][t2]!='-':
					flag=1
					#print 3


		if flag!=1:
			for i in range(t2,t2+3):
				if board[t1][i]==board[t1+1][i] and board[t1][i]==board[t1+2][i] and board[t1][i]!='-':
					flag=1
					#print 4

		if flag==1:
			block[old_block]=maxiplayer
			return old_block

		else:
			for i in range(t1,t1+3):
				for j in range(t2,t2+3):
					if board[i][j]=='-':
						tflag=1
			if tflag==0:
				block[old_block]='D'
			return old_block

		####print block

#	def win_check():

	def minimax(self,board,depth,maxiplayer,cells_allowed,block,alpha,beta):
		#check for terminal node

		if depth == 0:
			return [self.eval(board,maxiplayer,block),[-2,-2]]

		#children=genchildren(board,cells_allowed)
		temp=[]
		if maxiplayer==1:
			bestval=-100000000
			best_child=cells_allowed[0]
			for child in cells_allowed:
				board[child[0]][child[1]]='x'
				old_move=child
				#self.show_board(board)
				#block update
				revert_old=self.update_block(board,block,'x',old_move)

				check_game=self.end_game(block,board)
				if check_game==1:
					#print "kaka"
					temp=[10000000,child]
				elif check_game!=0:
					#print "kaka"

					temp=[check_game,child]
				elif check_game==0:
					blocks_allowed = self.find_legal_blocks(old_move,block)
					new_allow = self.cells_allowed(blocks_allowed, board, block)
					#if alpha<beta:
					temp=self.minimax(board,depth-1,0,new_allow,block,alpha,beta)
									
				board[child[0]][child[1]]='-'
				block[revert_old]='-'
				
				if temp[0] > bestval:
					best_child=child
					bestval=temp[0]
				#if child==cells_allowed[-1]:
					#print "max"
					#print bestval
				alpha = bestval
			#print "poop"
			#print bestval
			#print best_child

			return (bestval,best_child)

		else:
			bestval=100000000
			best_child=cells_allowed[0]
			for child in cells_allowed:
				
				board[child[0]][child[1]]='o'
				old_move=child
				
				#self.show_board(board)
				#block update
				revert_old=self.update_block(board,block,'o',old_move)
				#print block
				check_game=self.end_game(block,board)
				if check_game==1:
					#print "kaka"

					temp=[-10000000,child]
				elif check_game!=0:
					#print "kaka"

					temp= [check_game,child]
				elif check_game==0:
					blocks_allowed = self.find_legal_blocks(old_move,block)
					new_allow = self.cells_allowed(blocks_allowed, board, block)
					#if alpha<beta:
					temp=self.minimax(board,depth-1,1,new_allow,block,alpha,beta)

						# print self.count
				board[child[0]][child[1]]='-'
				block[revert_old]='-'

				if temp[0] < bestval:
					best_child=child
					bestval=temp[0]

				#if child==cells_allowed[-1]:
					#print "min"

					#print bestval

				beta = bestval
				#print "This is max"
				#print bestval


			return (bestval,best_child)


def determine_blocks_allowed(old_move, block_stat):
	blocks_allowed = []
	if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
		blocks_allowed = [1,3]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
		blocks_allowed = [1,5]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
		blocks_allowed = [3,7]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
		blocks_allowed = [5,7]
	elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
		blocks_allowed = [0,2]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
		blocks_allowed = [0,6]
	elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
		blocks_allowed = [6,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
		blocks_allowed = [2,8]
	elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
		blocks_allowed = [4]
	else:
		sys.exit(1)
	final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	return final_blocks_allowed

#Initializes the game
def get_init_board_and_blockstatus():
	board = []
	for i in range(9):
		row = ['-']*9
		board.append(row)
	
	block_stat = ['-']*9
	return board, block_stat

# Checks if player has messed with the board. Don't mess with the board that is passed to your move function. 
def verification_fails_board(board_game, temp_board_state):
	return board_game == temp_board_state	

# Checks if player has messed with the block. Don't mess with the block array that is passed to your move function. 
def verification_fails_block(block_stat, temp_block_stat):
	return block_stat == temp_block_stat	

#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
def get_empty_out_of(gameb, blal,block_stat):
	cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in blal:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if gameb[i][j] == '-':
					cells.append((i,j))

	# If all the possible blocks are full, you can move anywhere
	if cells == []:
		new_blal = []
		all_blal = [0,1,2,3,4,5,6,7,8]
		for i in all_blal:
			if block_stat[i]=='-':
				new_blal.append(i)

		for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))
	return cells
		
# Returns True if move is valid
def check_valid_move(game_board, block_stat, current_move, old_move):

	# first we need to check whether current_move is tuple of not
	# old_move is guaranteed to be correct
	if type(current_move) is not tuple:
		return False
	
	if len(current_move) != 2:
		return False

	a = current_move[0]
	b = current_move[1]	

	if type(a) is not int or type(b) is not int:
		return False
	if a < 0 or a > 8 or b < 0 or b > 8:
		return False

	#Special case at start of game, any move is okay!
	if old_move[0] == -1 and old_move[1] == -1:
		return True

	#List of permitted blocks, based on old move.
	blocks_allowed  = determine_blocks_allowed(old_move, block_stat)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
	cells = get_empty_out_of(game_board, blocks_allowed, block_stat)
	#Checks if you made a valid move. 
	if current_move in cells:
		return True
	else:
		return False

def update_lists(game_board, block_stat, move_ret, fl):

	game_board[move_ret[0]][move_ret[1]] = fl

	block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0

	flag = 0
	for i in range(id1*3,id1*3+3):
		for j in range(id2*3,id2*3+3):
			if game_board[i][j] == '-':
				flag = 1


	if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if flag == 0:
		block_stat[block_no] = 'D'
	if mflg == 1:
		block_stat[block_no] = fl
	
	return mflg

#Check win
def terminal_state_reached(game_board, block_stat,point1,point2):
	### we are now concerned only with block_stat
	bs = block_stat
	## Row win
	if (bs[0] == bs[1] and bs[1] == bs[2] and bs[1]!='-' and bs[1]!='D') or (bs[3]!='-' and bs[3]!='D' and bs[3] == bs[4] and bs[4] == bs[5]) or (bs[6]!='D' and bs[6]!='-' and bs[6] == bs[7] and bs[7] == bs[8]):
		return True, 'W'
	## Col win
	elif (bs[0] == bs[3] and bs[3] == bs[6] and bs[0]!='-' and bs[0]!='D') or (bs[1] == bs[4] and bs[4] == bs[7] and bs[4]!='-' and bs[4]!='D') or (bs[2] == bs[5] and bs[5] == bs[8] and bs[5]!='-' and bs[5]!='D'):
		return True, 'W'
	## Diag win
	elif (bs[0] == bs[4] and bs[4] == bs[8] and bs[0]!='-' and bs[0]!='D') or (bs[2] == bs[4] and bs[4] == bs[6] and bs[2]!='-' and bs[2]!='D'):
		return True, 'W'
	else:
		smfl = 0
		for i in range(9):
			if block_stat[i] == '-':
				smfl = 1
				break
		if smfl == 1:
			return False, 'Continue'
		
		else:
			if point1>point2:
				return True, 'P1'
			elif point2>point1:
				return True, 'P2'
			else:
				return True, 'D'	


def decide_winner_and_get_message(player,status, message):
	if status == 'P1':
		return ('P1', 'MORE BLOCKS')
	elif status == 'P2':
		return ('P2', 'MORE BLOCKS')
	elif player == 'P1' and status == 'L':
		return ('P2',message)
	elif player == 'P1' and status == 'W':
		return ('P1',message)
	elif player == 'P2' and status == 'L':
		return ('P1',message)
	elif player == 'P2' and status == 'W':
		return ('P2',message)
	else:
		return ('NONE','DRAW')
	return


def print_lists(gb, bs):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

	print "=========== Block Status ========="
	for i in range(0, 9, 3):
		print bs[i] + " " + bs[i+1] + " " + bs[i+2] 
	print "=================================="
	print
	

def simulate(obj1,obj2):
	
	# Game board is a 9x9 list of lists & block_stat is a list of 9 elements indicating if a block has been won.
	game_board, block_stat = get_init_board_and_blockstatus()

	pl1 = obj1 
	pl2 = obj2

	# Player with flag 'x' will start the game
	pl1_fl = 'x'
	pl2_fl = 'o'

	old_move = (-1, -1) # For the first move

	WINNER = ''
	MESSAGE = ''
	TIMEALLOWED = 1200
	p1_pts=0
	p2_pts=0

	print_lists(game_board, block_stat)

	while(1): # Main game loop
		
		temp_board_state = game_board[:]
		temp_block_stat = block_stat[:]
	
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(TIMEALLOWED)
		ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)

#		try:
#			ret_move_pl1 = pl1.move(temp_board_state, temp_block_stat, old_move, pl1_fl)
#		except:
#			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'TIMED OUT')
#			print MESSAGE
#			break
		signal.alarm(0)
	
		# Check if list is tampered.
		if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
		
		# Check if the returned move is valid
		if not check_valid_move(game_board, block_stat, ret_move_pl1, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P1', 'L',   'MADE AN INVALID MOVE')
			break
			

		print "Player 1 made the move:", ret_move_pl1, 'with', pl1_fl
		# Update the 'game_board' and 'block_stat' move
		p1_pts += update_lists(game_board, block_stat, ret_move_pl1, pl1_fl)

		gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
		if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P1', mesg,  'COMPLETE')	
			break

		
		old_move = ret_move_pl1
		print_lists(game_board, block_stat)

        	temp_board_state = game_board[:]
        	temp_block_stat = block_stat[:]

        	signal.signal(signal.SIGALRM, handler)
        	signal.alarm(TIMEALLOWED)

        	try:
           		ret_move_pl2 = pl2.move(temp_board_state, temp_block_stat, old_move, pl2_fl)
        	except:
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'TIMED OUT')
			break
        	signal.alarm(0)

        	if not (verification_fails_board(game_board, temp_board_state) and verification_fails_block(block_stat, temp_block_stat)):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MODIFIED CONTENTS OF LISTS')
			break
			
        	if not check_valid_move(game_board, block_stat, ret_move_pl2, old_move):
			WINNER, MESSAGE = decide_winner_and_get_message('P2', 'L',   'MADE AN INVALID MOVE')
			break

        	print "Player 2 made the move:", ret_move_pl2, 'with', pl2_fl
        
        	p2_pts += update_lists(game_board, block_stat, ret_move_pl2, pl2_fl)

        	# Now check if the last move resulted in a terminal state
        	gamestatus, mesg =  terminal_state_reached(game_board, block_stat,p1_pts,p2_pts)
        	if gamestatus == True:
			print_lists(game_board, block_stat)
			WINNER, MESSAGE = decide_winner_and_get_message('P2', mesg,  'COMPLETE' )
			break
        	else:
			old_move = ret_move_pl2
			print_lists(game_board, block_stat)
	
	print WINNER
	print MESSAGE

if __name__ == '__main__':
	## get game playing objects

	f = open("log.txt", "w+")

	if len(sys.argv) != 2:
		print 'Usage: python simulator.py <option>'
		print '<option> can be 1 => Random player vs. Random player'
		print '                2 => Human vs. Random Player'
		print '                3 => Human vs. Human'
		sys.exit(1)
 
	obj1 = ''
	obj2 = ''
	option = sys.argv[1]	
	if option == '1':
		obj1 = Player1()
		obj2 = team72.Player72()

	elif option == '2':
		obj1 = Player1()
		obj2 = ManualPlayer()
	elif option == '3':
		obj1 = ManualPlayer()
		obj2 = ManualPlayer()
	else:
		print 'Invalid option'
		sys.exit(1)

	#num = random.uniform(0,1)
	simulate(obj1, obj2)
	print "Umesh - P2"
	f.close()

		
	
