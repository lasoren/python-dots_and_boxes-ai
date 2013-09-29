#!/usr/bin/env python
try:
	import tkinter as tk
	from tkinter import *
except:
	import Tkinter as tk
	from Tkinter import *
import gameBoard as gB
import DandBCom as DBC
import time
import os

class App:
	#Begins the app, and allows the user to enter a grid size for the game.
	def __init__(self,master):
		try:
			self.frame.destroy()
			self.t=0
		except:
			pass
		self.Master=master
		master.title("Dots and Boxes")
		self.canvas = Canvas(self.Master)
		self.frame = Frame(master); self.frame.grid()
		self.welcomePhoto = tk.PhotoImage(file='Welcome.gif'); self.welcome = Label(self.frame, image=self.welcomePhoto)
		self.welcome.grid(row=0,columnspan=6)
		self.cmdPhoto = tk.PhotoImage(file='Enter.gif'); self.enter = Label(self.frame, image=self.cmdPhoto)
		self.enter.grid(row=1,columnspan=6)
		self.rowPhoto = tk.PhotoImage(file='Rows.gif'); self.rows = Label(self.frame, image = self.rowPhoto)
		self.rows.grid(row=2)
		self.colPhoto = tk.PhotoImage(file='Cols.gif'); self.cols = Label(self.frame, image = self.colPhoto)
		self.cols.grid(row=3)
		self.rowEntry = Entry(self.frame)
		self.rowEntry.grid(row=2,column=1)
		self.colEntry = Entry(self.frame)
		self.colEntry.grid(row=3,column=1)
		self.enterPhoto = tk.PhotoImage(file='EnterButton.gif')
		self.Enter = Label(self.frame,image = self.enterPhoto)
		self.Enter.bind("<Button-1>",lambda e,comOption=self.comOption: self.comOption())
		self.Master.bind('<Return>', (lambda e, Enter=self.Enter: self.comOption()))
		self.Enter.grid(row=4,column=1)
	
	#Prompts the user to choose if they would like to play against the computer.
	def comOption(self):
		self.Master.unbind('<Return>')
		try:
			self.rows=int(self.rowEntry.get())
			self.cols=int(self.colEntry.get())
			if self.rows < 3:
				self.rows =3
			elif self.rows > 10:
				self.rows = 10
			if self.cols < 3:
				self.cols =3
			elif self.cols > 10:
				self.cols = 10
		except:
			self.rows=3
			self.cols=3
		self.frame.destroy()
		self.frame = Frame(self.Master); self.frame.grid()
		self.comQues = tk.PhotoImage(file='ComQuestion.gif'); self.question = Label(self.frame, image=self.comQues)
		self.question.grid(row=0,columnspan=6)
		self.yesHard = tk.PhotoImage(file='YesHard.gif'); self.YesHard = Label(self.frame, image=self.yesHard)
		self.YesHard.bind("<Button-1>",lambda e,createWindow=self.createWindow: self.createWindow(1,self.rows,self.cols))
		self.YesHard.grid(row=1,column=0)
		self.yesPhoto = tk.PhotoImage(file='Yes.gif'); self.Yes = Label(self.frame, image=self.yesPhoto)
		self.Yes.bind("<Button-1>",lambda e,createWindow=self.createWindow: self.createWindow(2,self.rows,self.cols))
		self.Yes.grid(row=1,column=1)
		self.noPhoto = tk.PhotoImage(file='No.gif'); self.No = Label(self.frame, image = self.noPhoto)
		self.No.bind("<Button-1>",lambda e,createWindow=self.createWindow: self.createWindow(0,self.rows,self.cols))
		self.No.grid(row=1,column=2)
	
	#Sets the window size, based on the grid.
	def createWindow(self,comOp,rows,cols):
		self.h=rows*50 + (rows+1)*20 + 60
		self.w=cols*50 + (cols+1)*20 + 60
		self.frame.destroy()
		self.canvas.config(height=self.h,width=self.w)
		self.canvas.pack()
		self.Master.minsize(self.w,self.h)
		self.comOp=comOp
		if self.comOp:
			self.com = DBC.DandBCom(self.comOp)
		self.startGame()
	
	#Reads in the photos and begins the game.
	def startGame(self):
		self.colors=['blue','red']
		self.Lines =[tk.PhotoImage(file='DottedLine.gif'),tk.PhotoImage(file='Line.gif'),
						tk.PhotoImage(file='HorizDottedLine.gif'),tk.PhotoImage(file='HorizLine.gif')]
		self.Dot =tk.PhotoImage(file='Dot.gif')
		self.Squares =[tk.PhotoImage(file='EmptySquare.gif'),tk.PhotoImage(file='BlueSquare.gif'),tk.PhotoImage(file='RedSquare.gif')]
		self.ActiveLines = [tk.PhotoImage(file='ActiveLine.gif'),tk.PhotoImage(file='ActiveHorizLine.gif')]
		self.ComLines = [tk.PhotoImage(file='ComLine.gif'),tk.PhotoImage(file='HorizComLine.gif')]
		self.t=0
		self.counter=0
		self.gb = gB.gameBoard(self.rows,self.cols)
		self.makeBoard()
	
	#Displays the board to the user.
	def makeBoard(self):
		if self.counter == 0:
			self.Master.config(bg='black')
			for r in range(self.rows+1):
				for c in range(self.cols+1):
					dH=31+70*(r)
					dW=31+70*(c)
					self.dot = self.canvas.create_image (dW,dH,image=self.Dot,anchor=NW)
		for r in range(len(self.gb.gridRepr)):
			for c in range(len(self.gb.gridRepr[r])):
				if r%2 ==0:
					lH=31+70*r//2
					lW=51+70*c
					if self.gb.gridRepr[r][c] == 1:
						line = self.canvas.create_image (lW,lH,image=self.Lines[self.gb.gridRepr[r][c]+2],anchor=NW)
					else:
						line = self.canvas.create_image (lW,lH,image=self.Lines[self.gb.gridRepr[r][c]+2],anchor=NW,activeimage=self.ActiveLines[1])
				else:	
					lH=51+70*(r-1)//2
					lW=31+70*(c)
					if self.gb.gridRepr[r][c] == 1:
						line = self.canvas.create_image (lW,lH,image=self.Lines[self.gb.gridRepr[r][c]],anchor=NW)
					else:
						line = self.canvas.create_image (lW,lH,image=self.Lines[self.gb.gridRepr[r][c]],anchor=NW,activeimage=self.ActiveLines[0])
		
		self.counter=1
	
	#Changes the board based on a user or computer's move.
	def changeBoard(self,r,c,t):
		try:
			self.canvas.delete(self.text)
		except:
			pass
		if r%2 ==0:
			lH=31+70*r//2
			lW=51+70*c
			if self.comOp and self.t%2 == 1:
				self.makeBoard()
				line = self.canvas.create_image (lW,lH,image=self.ComLines[1],anchor=NW)
			else:
				line = self.canvas.create_image (lW,lH,image=self.Lines[self.gb.gridRepr[r][c]+2],anchor=NW)
		else:	
			lH=51+70*(r-1)//2
			lW=31+70*(c)
			if self.comOp and self.t%2 == 1:
				self.makeBoard()
				line = self.canvas.create_image (lW,lH,image=self.ComLines[0],anchor=NW)
			else:
				line = self.canvas.create_image (lW,lH,image=self.Lines[self.gb.gridRepr[r][c]],anchor=NW)
		
		tempSpaces=[]
		for row in range(len(self.gb.spaceRepr)):
			tempSpaces.append([])
			tempSpaces[row]=self.gb.spaceRepr[row][:]
		tempGrid=[]
		for row in range(len(self.gb.gridRepr)):
			tempGrid.append([])
			tempGrid[row]=self.gb.gridRepr[row][:]
		self.gb.checkForSquares(tempGrid,tempSpaces,self.t%2)
		if self.gb.spaceRepr == tempSpaces:
			self.t+=1
		else:
			self.gb.checkForSquares(self.gb.gridRepr,self.gb.spaceRepr,self.t%2)
			for row in range(len(self.gb.spaceRepr)):
				for col in range(len(self.gb.spaceRepr[row])):
					sH=51+70*row
					sW=51+70*col
					square=self.canvas.create_image (sW,sH,image=self.Squares[self.gb.spaceRepr[row][col]],anchor=NW)
		if not self.comOp:
			self.text = self.canvas.create_text(self.w//2,self.h-25,anchor = N,text = 'Player ' + str(self.t%2+1) + "'s turn.",font = ("Lucida Console","20"),fill=self.colors[self.t%2])
		value=True
		for row in self.gb.gridRepr:
			if 0 in row:
				value = False
				
		if value:
			count1=0
			count2=0
			for row in self.gb.spaceRepr:
				for s in row:
					if s == 1:
						count1+=1
					if s == 2:
						count2+=1
			self.makeBoard()
			self.newGame(count1,count2)
		
		self.Master.update()

		if self.comOp and self.t%2 == 1 and not value:
			point = self.com.comPick(self.gb,r,c)
			self.gb.gridRepr[point[0]][point[1]]=1
			self.changeBoard(point[0],point[1],self.t%2)
	
	#Reads in the user's turn.
	def callback(self,event):
		if not self.comOp or (self.comOp and self.t%2 == 0):
			for r in range(len(self.gb.gridRepr)):
				for c in range(len(self.gb.gridRepr[r])):
					if r%2 ==0:
						lH=31+70*r//2
						lW=51+70*c
						if event.x in range(lW,lW+50) and event.y in range(lH,lH+20):
							if self.gb.gridRepr[r][c]!=1:
								self.gb.gridRepr[r][c]=1
								self.changeBoard(r,c,self.t%2)
					else:	
						lH=51+70*(r-1)//2
						lW=31+70*(c)
						if event.x in range(lW,lW+20) and event.y in range(lH,lH+50):
							if self.gb.gridRepr[r][c]!=1:
								self.gb.gridRepr[r][c]=1
								self.changeBoard(r,c,self.t%2)
	
	#Opens a window to allow a user to play a new game.
	def newGame(self,count1,count2):
		self.Master.update()
		time.sleep(.5)
		self.Master.config(bg='white')
		self.window = Toplevel(); self.window.title('Dots and Boxes')
		self.frame = Frame(self.window); self.frame.grid()
		self.player1score = Label(self.frame,text='Player 1 Boxes: '+ str(count1),font = ("Lucida Console", "22"), fg = 'blue')
		self.player1score.grid(row=0)
		self.player2score = Label(self.frame,text='Player 2 Boxes: '+ str(count2),font = ("Lucida Console", "22"), fg = 'red')
		self.player2score.grid(row=1)
		if count1 > count2:
			self.result = Label(self.frame,text='Player 1 is the winner!',font = ("Lucida Console", "22"))
			self.result.grid(row=2)
		elif count2 > count1:
			self.result = Label(self.frame,text='Player 2 is the winner!',font = ("Lucida Console", "22"))
			self.result.grid(row=2)	
		else:
			self.result = Label(self.frame,text="It's a tie.",font = ("Lucida Console", "22"))
			self.result.grid(row=2)
		self.space = Label(self.frame,image=self.Squares[0])
		self.space.grid(row=3)
		self.newPhoto = tk.PhotoImage(file='NewGame.gif'); self.newGame = Label(self.frame, image=self.newPhoto)
		self.newGame.bind("<Button-1>",lambda e,reroute=self.reroute: self.reroute())
		self.newGame.grid(row=4)
		self.quitPhoto = tk.PhotoImage(file='Quit.gif'); self.quit = Label(self.frame, image=self.quitPhoto)
		self.quit.bind("<Button-1>",lambda e,quit=self.quiter: self.quiter())
		self.quit.grid(row=5)
	
	#Starts the game over.
	def reroute(self):
		self.Master.destroy()
		root = tk.Tk()
		app = App(root)
		app.canvas.bind("<Button-1>", app.callback)
		root.mainloop()
	
	def quiter(self):
		self.Master.destroy()
		self.Master.quit()
		
root = tk.Tk()
app = App(root)
app.canvas.bind("<Button-1>", app.callback)
root.mainloop()