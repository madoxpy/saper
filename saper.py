from pygame import *
import numpy as np
from random import *
from time import sleep


green=(0,255,0)
greengrass=(1,166,17)
black=(0,0,0)
white=(255,255,255)
bluesky=(135,206,235)
red=(255,5,5)
bloodred=(138,7,7)
blue=(0,0,255)
darkblue=(0,0,139)
colors = [(0,0,0),(255,0,0),(0,128,255),(255,128,0),(255,0,128),(128,255,0),(128,0,255),(0,255,0),(0,0,255)]


res=[800,640]

init()
window=display.set_mode(res)
clock = time.Clock()
Font=font.SysFont("arial",20)

def nei(i,j,tab):
	result=0
	if j>0 and i>0:
		if tab[i-1][j-1]==9:
			result=result+1
	if j>0:
		if tab[i][j-1]==9:
			result=result+1
	if j>0 and i<23:
		if tab[i+1][j-1]==9:
			result=result+1
	if i>0:
		if tab[i-1][j]==9:
			result=result+1		
	if i<23:
		if tab[i+1][j]==9:
			result=result+1	
	if j<23 and i>0:
		if tab[i-1][j+1]==9:
			result=result+1
	if j<23 and i<23:
		if tab[i+1][j+1]==9:
			result=result+1
	if j<23:
		if tab[i][j+1]==9:
			result=result+1
			
	if tab[i][j] != 9:
		return result
	else:
		return 9
	
def clear(i,j,tab,vis):
	if j>0 and i>0:
		if tab[i-1][j-1]==0 and vis[i-1][j-1]==False:
			vis[i-1][j-1]=True
			clear(i-1,j-1,tab,vis)
		vis[i-1][j-1]=True
	if j>0:
		if tab[i][j-1]==0 and vis[i][j-1]==False:
			vis[i][j-1]=True
			clear(i,j-1,tab,vis)
		vis[i][j-1]=True
	if j>0 and i<23:
		if tab[i+1][j-1]==0  and vis[i+1][j-1]==False:
			vis[i+1][j-1]=True
			clear(i+1,j-1,tab,vis)
		vis[i+1][j-1]=True
	if i>0:
		if tab[i-1][j]==0 and vis[i-1][j]==False:		
			vis[i-1][j]=True
			clear(i-1,j,tab,vis)
		vis[i-1][j]=True
	if i<23:
		if tab[i+1][j]==0 and vis[i+1][j]==False:
			vis[i+1][j]=True
			clear(i+1,j,tab,vis)
		vis[i+1][j]=True
	if j<23 and i>0:
		if tab[i-1][j+1]==0 and vis[i-1][j+1]==False:
			vis[i-1][j+1]=True
			clear(i-1,j+1,tab,vis)
		vis[i-1][j+1]=True
	if j<23 and i<23:
		if tab[i+1][j+1]==0 and vis[i+1][j+1]==False:
			vis[i+1][j+1]=True
			clear(i+1,j+1,tab,vis)
		vis[i+1][j+1]=True
	if j<23:
		if tab[i][j+1]==0 and vis[i][j+1]==False:
			vis[i][j+1]=True
			clear(i,j+1,tab,vis)
		vis[i][j+1]=True

			
class Game(object):
	def __init__(self):
		self.w = 24
		self.h = 24
		self.size = 25
		self.mines = 90
		self.tab = []
		self.vis = []
		self.marked=[]
		self.endgame=False
		self.wingame=False
		for i in range(self.w):
			tmp=[]
			tmp2=[]
			for j in range(self.h):
				tmp.append(0)
				tmp2.append(False)
			self.tab.append(tmp)
			self.vis.append(tmp2)
		for i in range(self.w):
			tmp2=[]
			for j in range(self.h):
				tmp2.append(False)			
			self.marked.append(tmp2)
			


		i=0
		while i<self.mines:
			x = randint(0,self.w-1)
			y = randint(0,self.h-1)	
			if self.tab[x][y]==0:
				self.tab[x][y]=9
				i = i+1
			#print i
				

		for i in range(self.w):
			for j in range(self.h):
				self.tab[i][j]=nei(i,j,self.tab)
				
		'''for i in range(self.w):
			for j in range(self.h):
				print str(self.tab[i][j]),
			print
		'''
	def draw(self):
		window.fill(black)
		for i in range(self.w):
			for j in range(self.h):
				if self.vis[i][j]:
					if self.tab[i][j]==0:
						draw.rect(window,white,Rect(i*self.size,j*self.size,self.size-1,self.size-1))
					elif self.tab[i][j]==9:
						draw.rect(window,bloodred,Rect(i*self.size,j*self.size,self.size-1,self.size-1))	
					else:
						draw.rect(window,white,Rect(i*self.size,j*self.size,self.size-1,self.size-1))	
						text = Font.render(str(self.tab[i][j]),True,colors[self.tab[i][j]])
						window.blit(text,(i*self.size+3,j*self.size))
				else:
					draw.rect(window,green,Rect(i*self.size,j*self.size,self.size-1,self.size-1))
				if self.marked[i][j]:
					draw.rect(window,black,Rect(i*self.size,j*self.size,self.size-1,self.size-1))

		if self.endgame:
				if not self.wingame:
					text = Font.render(str("Game Over"),True,white)
					window.blit(text,(650,100))
				else:
					text = Font.render(str("Win"),True,white)
					window.blit(text,(650,100))

					
	def check(self,x,y):
		for i in range(self.w):
			for j in range(self.h):
				if x>i*self.size and x<(i+1)*self.size and y>j*self.size and y<(j+1)*self.size and not self.marked[i][j]:
					if not self.vis[i][j]:	
						self.vis[i][j] = True
					if self.tab[i][j]==9:
						self.endgame=True
						mixer.music.load('exp.wav')
						mixer.music.play(1)
					if self.tab[i][j]==0:
						clear(i,j,self.tab,self.vis)
						
	def mark(self,x,y):					
		for i in range(self.w):
			for j in range(self.h):
				if x>i*self.size and x<(i+1)*self.size and y>j*self.size and y<(j+1)*self.size:
					if not self.vis[i][j] and not self.marked[i][j]:	
						self.marked[i][j] = True
					elif not self.vis[i][j] and self.marked[i][j]:	
						self.marked[i][j] = False
					sleep(0.5)
	def win(self):
		n = 0
		for i in range(self.w):
			for j in range(self.h):
				if self.vis[i][j]:
					n=n+1
					
		if self.w*self.h-self.mines==n:
			return True
		else:
			return False

class Button(object):
	def __init__(self,x,y,w,h,text=""):
		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.text=text
		self.Font=font.SysFont("arial",36)
		self.act=False
		
	def event(self):
		return Game()
		
	def click(self):
		if mouse.get_pressed()[0]:
			if mouse.get_pos()[0]>self.x and mouse.get_pos()[0]<self.x+self.w and mouse.get_pos()[1]>self.y and mouse.get_pos()[1]<self.y+self.h:
				return True

	def draw(self):

		if mouse.get_pos()[0]>self.x and mouse.get_pos()[0]<self.x+self.w and mouse.get_pos()[1]>self.y and mouse.get_pos()[1]<self.y+self.h:
			draw.rect(window,green,Rect(self.x,self.y,self.w,self.h),1)
		else:
			draw.rect(window,white,Rect(self.x,self.y,self.w,self.h),1)
		text = self.Font.render(self.text,True,white)
		window.blit(text,(self.x+5,self.y+5))
						
						
game=Game()
end=False
new=Button(600,300,200,50,"New Game")	

while not end:
	
	for zet in event.get():
		if zet.type ==QUIT:
			end=True
		
		
	if mouse.get_pressed()[0]:
		if not game.endgame:
			game.check(mouse.get_pos()[0],mouse.get_pos()[1])
			
	if mouse.get_pressed()[2]:
		if not game.endgame:
			game.mark(mouse.get_pos()[0],mouse.get_pos()[1])
	
	game.draw()
	new.draw()
	if new.click():
		game=new.event()
	if game.win():
		game.wingame=True
		game.endgame=True
	clock.tick(20)
	display.flip()