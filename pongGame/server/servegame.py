from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import socket
import json
import pickle
import threading
import time

ballpos_x = 0
ballpos_y = 0
Player_1 = 0
Player_2 = 0
Score_1 = 0
Score_2 = 0
On = True

def sending(con,player):
	while(On):
		time.sleep(10/1000)
		if player == 1:
			data = {
				"ball_x": ballpos_x,
				"ball_y": ballpos_y,
				"Player_O": Player_2,
				"Player_id": player,
				"Score_1": Score_1,
				"Score_2": Score_2
			}
		else:
			data = {
				"ball_x": ballpos_x,
				"ball_y": ballpos_y,
				"Player_O": Player_1,
				"Player_id": player,
				"Score_1": Score_1,
				"Score_2": Score_2
			}
		
		data = pickle.dumps(data)
		#print(data)
		con.sendall(data)
		

def getting(con,player):
	#print("hey")
	#global On
	global Player_1
	global Player_2
	while(On):
			data = con.recv(1024)
			data = pickle.loads(data)
			#print(data)
			if player == 1:
				#print(data)
				#data = pickle.loads(data)
				Player_1 = data["Player_O"]
				#print(Player_1)
			else:
				#print(data)
				#data = pickle.loads(data)
				Player_2 = data["Player_O"]


class Connection:
	def __init__(self,player):
		self.con= ''
		self.player = player
	def connect_to_client(self,s):
		self.con,addr = s.accept()
		print(addr," connected to server")
		
	def SendGetPos(self):
		sending_ = threading.Thread(target = sending, args = (self.con,self.player))
		getting_ = threading.Thread(target = getting, args = (self.con,self.player))
		sending_.start()
		getting_.start()
 
 
class PongPaddle(Widget):
	score = NumericProperty(0)
	def bounce_ball(self, ball):
		if self.collide_widget(ball):
			vx, vy = ball.velocity
			offset = (ball.center_y - self.center_y) / (self.height / 2)
			bounced = Vector(-1 * vx, vy)
			vel = bounced * 1.1
			ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
	velocity_x = NumericProperty(0)
	velocity_y = NumericProperty(0)
	velocity = ReferenceListProperty(velocity_x, velocity_y)

	def move(self):
		self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
	#global Player_1
	#global Player_2
	
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def serve_ball(self, vel=(4, 0)):
		global ballpos_x
		global ballpos_y
		ballpos_x,ballpos_y = self.center
		self.ball.center = self.center
		self.ball.velocity = vel

	def update(self, dt):
		global ballpos_x
		global ballpos_y
		global Score_1
		global Score_2
		self.player1.center_y = Player_1
		self.player2.center_y = Player_2
		self.ball.move()

        # bounce of paddles
		self.player1.bounce_ball(self.ball)
		self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
		if (self.ball.y < self.y) or (self.ball.top > self.top):
			self.ball.velocity_y *= -1

		ballpos_x = self.ball.x
		ballpos_y = self.ball.y
        # went of to a side to score point?
		if self.ball.x < self.x:
			self.player2.score += 1
			Score_2 = self.player2.score
			self.serve_ball(vel=(4, 0))
		if self.ball.x > self.width:
			self.player1.score += 1
			Score_1 = self.player1.score
			self.serve_ball(vel=(-4, 0))

class PongApp(App):
	def build(self):
		host = socket.gethostbyname('0.0.0.0')
		port = 8006
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.bind((host,port))
		s.listen(5)
		con1 = Connection(1)
		con2 = Connection(2)
		con1.connect_to_client(s)
		con1.SendGetPos()
		#print("Hello")
		
		con2.connect_to_client(s)
		con2.SendGetPos()
		#con1.SendGetPos()
		game = PongGame()
		game.serve_ball()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	#global On
	PongApp().run()
	On = False




