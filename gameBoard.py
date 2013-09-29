class gameBoard:
	def __init__(self,row,col):
		#Represents the lines of the grid.
		self.gridRepr = [0]*(row*2+1)
		for i in range(len(self.gridRepr)):
			if i%2==0:
				self.gridRepr[i]=[0]*(col)
			else:
				self.gridRepr[i]=[0]*(col+1)
		#Represents the squares of the grid.
		self.spaceRepr=[0]*row
		for i in range(len(self.spaceRepr)):
			self.spaceRepr[i]=[0]*col
	
	#Checks to see if a square has been made and fills in spaceRepr appropriately.
	def checkForSquares(self,grid,spaces,turn):
		for i in range(len(grid)-1):
			if i%2==0:
				for j in range(len(grid[i])):
					if grid[i][j]==1 and grid[i+1][j]==1 and grid[i+1][j+1]==1 and grid[i+2][j]==1 and spaces[i//2][j]==0:
						if turn == 0:
							spaces[i//2][j]=1
						if turn == 1:
							spaces[i//2][j]=2
		return spaces
	
	#Returns a list of the lines that complete a three-sided square.
	def threeSides(self,grid):
		closeableSpaces=[]
		for i in range(len(grid)-1):
			if i%2==0:
				for j in range(len(grid[i])):
					count=0
					for g in [[i,j],[i+1,j],[i+1,j+1],[i+2,j]]:
						if grid[g[0]][g[1]]==1:
							count+=1
						else:
							lineSpace=g
					if count==3:
						closeableSpaces.append(lineSpace)
		return closeableSpaces
	
	#Returns a list of all the lines that complete the third side of a square.
	def twoSides(self,grid):
		twoSideSpaces=[]
		for i in range(len(grid)-1):
			if i%2==0:
				for j in range(len(grid[i])):
					count=0
					lineSpaces=[]
					for g in [[i,j],[i+1,j],[i+1,j+1],[i+2,j]]:
						if grid[g[0]][g[1]]==1:
							count+=1
						else:
							lineSpaces.append(g)
					if count==2:
						for s in lineSpaces:
							if s not in twoSideSpaces:
								twoSideSpaces.append(s)
		return twoSideSpaces
		

if __name__ == '__main__':
	X=gameBoard(3,3)	
	
	#How to define a tempSpaceRepr and a tempGridRepr so that the two are distinguishable.
	tempSpaces=[]
	for r in range(len(X.spaceRepr)):
		tempSpaces.append([])
		tempSpaces[r]=X.spaceRepr[r][:]
			
	tempGrid=[]
	for r in range(len(X.gridRepr)):
		tempGrid.append([])
		tempGrid[r]=X.gridRepr[r][:]
	
	tempGrid[0][1]=1
	tempGrid[1][1]=1
	tempGrid[2][1]=1
	tempGrid[1][2]=1
	tempGrid[4][1]=1
	tempGrid[5][1]=1
	tempGrid[5][2]=1
	
	X.checkForSquares(tempGrid,tempSpaces,1)
	printed = X.twoSides(tempGrid)
	print(printed)
	printed = X.threeSides(tempGrid)
	print(printed)
	print('')
	
	for x in tempGrid:
		print(x)
	print('')
		
	for y in tempSpaces:
		print(y)