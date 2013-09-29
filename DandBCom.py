import gameBoard as gb
import random
import math

class DandBCom:
	def __init__(self,diff):
		self.diff=diff #1 is hard, 2 is easy
	
	#The computer picks a location  of a line and returns a list of two integers.
	def comPick(self,gb,i,j):
		firstChoices=gb.threeSides(gb.gridRepr)
		if len(firstChoices) > 0:
			if self.diff == 1:
				possibleSquares,newGrid=self.completeTurn(gb)
				userSquares=self.userToMake(gb,newGrid)
				if (possibleSquares == 2 and userSquares > 2):
					tempGrid = []
					for r in range(len(gb.gridRepr)):
						tempGrid.append([])
						tempGrid[r]=gb.gridRepr[r][:]
					tempGrid[firstChoices[0][0]][firstChoices[0][1]]=1
					newChoices=gb.threeSides(tempGrid)
					if len(newChoices) > 0:
						return(newChoices[0])
					else:
						return(firstChoices[0])
				elif (possibleSquares == 4 and userSquares > 4):
					tempGrid = []
					for r in range(len(gb.gridRepr)):
						tempGrid.append([])
						tempGrid[r]=gb.gridRepr[r][:]
					dontChoose = gb.twoSides(tempGrid)
					tempGrid[firstChoices[0][0]][firstChoices[0][1]]=1
					newChoices=gb.threeSides(tempGrid)
					if len(newChoices) > 1:
							for f in firstChoices:
								while f in dontChoose:
									dontChoose.remove(f)
							for d in dontChoose:
								if d in newChoices:
									return d
					else:
						return(firstChoices[0])
				else:
					return(firstChoices[0])
			else:
				return(firstChoices[0])
			
		viableSpaces=[]
		for i in range(len(gb.gridRepr)):
			for j in range(len(gb.gridRepr[i])):
				if gb.gridRepr[i][j]==0:
					viableSpaces.append([i,j])
		dontChoose = gb.twoSides(gb.gridRepr)
		if len(viableSpaces) == len(dontChoose):
			num = 100000
			for x in viableSpaces:
				if self.squaresToMake(gb,x) < num:
					num = self.squaresToMake(gb,x)
			best = []
			for x in viableSpaces:
				if self.squaresToMake(gb,x) == num:
					best.append(x)
			if self.diff == 1:
				for b in best:
					tempGrid = []
					for r in range(len(gb.gridRepr)):
						tempGrid.append([])
						tempGrid[r]=gb.gridRepr[r][:]
					tempGrid[b[0]][b[1]]=1
					newChoices=gb.threeSides(tempGrid)
					if len(newChoices) > 1:
						return b
			random.shuffle(best)
			return best[0]
		else:
			for d in dontChoose:
				if len(viableSpaces)>1:
					if d in viableSpaces:
						viableSpaces.remove(d)
		random.shuffle(viableSpaces)
		return(viableSpaces[0])
	
	#Simulates the users turn. 
	def squaresToMake(self,gb,point):
		tempGrid=[]
		for r in range(len(gb.gridRepr)):
			tempGrid.append([])
			tempGrid[r]=gb.gridRepr[r][:]
		tempGrid[point[0]][point[1]]=1
		self.count=0
		self.recursiveSquares(gb,tempGrid)
		return self.count
	
	#Support function to determine number of squares that are possible to create on one turn.
	def recursiveSquares(self,gb,grid):
		if len(gb.threeSides(grid))==0:
			return grid
		else:
			choices=gb.threeSides(grid)
			choice = [choices[0][0],choices[0][1]]
			grid[choices[0][0]][choices[0][1]]=1
			self.count+=1
			choices.remove(choice)
			if choice in choices:
				self.count+=1
			self.recursiveSquares(gb,grid)
	
	#Simulates computer's whole turn.
	def completeTurn(self,gb):
		tempGrid=[]
		for r in range(len(gb.gridRepr)):
			tempGrid.append([])
			tempGrid[r]=gb.gridRepr[r][:]
		self.count=0
		self.recursiveSquares(gb,tempGrid)
		newGrid = self.recursiveSquares(gb,tempGrid)
		return self.count, newGrid
		
	#Simulates user's next turn.	
	def userToMake(self,gb,grid):
		userPick = self.modComPick(gb,grid)
		if userPick == [-1,-1]:
			return 0
		grid[userPick[0]][userPick[1]]=1
		self.count=0
		self.recursiveSquares(gb,grid)
		return self.count
	
	#Modified computer pick for after the computer's turn has been simulated.
	def modComPick(self,gb,grid):
		viableSpaces=[]
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				if grid[i][j]==0:
					viableSpaces.append([i,j])
		dontChoose = gb.twoSides(grid)
		if len(viableSpaces) != 0:
			if len(viableSpaces) == len(dontChoose):
				num = 100000
				for x in viableSpaces:
					if self.squaresToMake(gb,x) < num:
						num = self.squaresToMake(gb,x)
						best = x
				return best
			else:
				for d in dontChoose:
					if len(viableSpaces)>1:
						if d in viableSpaces:
							viableSpaces.remove(d)
			random.shuffle(viableSpaces)
			return(viableSpaces[0])
		return [-1,-1]
				
if __name__ == "__main__":
	X=gb.gameBoard(3,3)
	
	for r in range(len(X.gridRepr)):
		for c in range(len(X.gridRepr[r])):
			X.gridRepr[r][c]=1
	X.gridRepr[0][0]=0		
	X.gridRepr[0][1]=0		
	X.gridRepr[4][1]=0
	X.gridRepr[5][2]=0
	X.gridRepr[5][3]=0
	X.gridRepr[2][1]=0
	X.gridRepr[1][0]=0
	c=-1
	for x in X.gridRepr:
		c+=1
		if c%2 == 0:
			print(' '+str(x))
		else:
			print(x)
	print('')
	X.checkForSquares(X.gridRepr,X.spaceRepr,1)
	for y in X.spaceRepr:
		print(y)
	
	C=DandBCom(2)
	print('')
	print(C.comPick(X,0,0))
	
	