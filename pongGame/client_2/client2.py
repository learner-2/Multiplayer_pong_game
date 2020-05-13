from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import socket
import json
import threading
import time
import pickle

ready = False
ball_x = 0
ball_y = 0
Player_O = 0
Player_id = 0
Score_1 = 0
Score_2 = 0 
Player_My = 0
On = True

def sending(s):
	#while (not ready):
	#	pass
	#print("hello")
	#global On
	#global Player_My
	while(On):
		time.sleep(10/1000)
		data = {
		"Player_O": Player_My
		}
		data = pickle.dumps(data)
		s.send(data)
	s.close()

def getting(s):
	#print("hello")
	#global On
	global ball_x
	global ball_y
	global Player_O
	global Score_1
	global Score_2
	global Player_id
	global ready
	while(On):
		#print("hello1")
		data = s.recv(1024)
		#print(data)
		#print("hello2")
		data = pickle.loads(data)
		#print("ehll")
		#print(data)
		ball_x = data["ball_x"]
		ball_y = data["ball_y"]
		Player_O = data["Player_O"]
		Player_id = data["Player_id"]
		Score_1 = data["Score_1"]
		Score_2 = data["Score_2"]
		#ready = True
	s.close()
class Connection:
	#global Player_id
	host = '127.0.0.1'
	port = 8006
	s = socket.socket()
	def __init__(self):
		self.player = Player_id

	def connect_to_server(self):
		self.s.connect((self.host, self.port))
		print("Connected to server")
	
	def SendGetPos(self):
		sending_ = threading.Thread(target = sending, args = (self.s,))
		getting_ = threading.Thread(target = getting, args = (self.s,))
		sending_.start()
		getting_.start()
 
class PongPaddle(Widget):
	score = NumericProperty(0)



class PongBall(Widget):
	pass


class PongGame(Widget):
	ball = ObjectProperty(None)
	player1 = ObjectProperty(None)
	player2 = ObjectProperty(None)

	def update(self, dt):
		self.ball.x = ball_x
		self.ball.y = ball_y
		self.player1.score = Score_1
		self.player2.score = Score_2
		if Player_id == 1:
			self.player2.center_y = Player_O
		else:
			self.player1.center_y = Player_O

	def on_touch_move(self, touch):
		global Player_My
		if touch.x < self.width / 3 and Player_id == 1:
			self.player1.center_y = touch.y
			Player_My = touch.y
			#print(Player_My)
		elif touch.x > self.width - self.width / 3 and Player_id == 2:
			self.player2.center_y = touch.y
			Player_My = touch.y
			#print(Player_My)


class PongApp(App):
	def build(self):
		con = Connection()
		con.connect_to_server()
		con.SendGetPos()
		game = PongGame()
		Clock.schedule_interval(game.update, 1.0 / 60.0)
		return game

if __name__ == '__main__':
	#global On
	PongApp().run()
	On = False