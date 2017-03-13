from scene import *
from math import pi, cos, sin
from utils import *
from ui import Path
from Laser import Laser
		

class Player(SpriteNode):
	'''
	Represents the controllable spaceship.
	There is only one instance og Player at any time
	'''

	def __init__(self, **kwargs):
		SpriteNode.__init__(self, PLAYER_TEXTURE, **kwargs)
		self.position = self.parent.center
		self.pos = Vector2(.0, .0)
		self.anchor_point = (.5, .5)
		self.velocity = Vector2(.0, .0)
		self.label = LabelNode('', parent=self, position=(0, 60))
		
	def move(self):
		'''Add self.velocity to self.pos'''
		self.pos = self.pos + self.velocity
		
	def update_vel(self, dist):
		'''Update self.velocity with `dist` towards self.rotation'''
		self.velocity = lerp(
			self.velocity,
			rotation_vector(self.rotation)*dist*self.speed,
			PLAYER_SLOWDOWN_RATE)
	
	def rotate(self, radians):
		'''Adds `radians` to self.rotaion if `radians` < PLAYER_TURN_SPEED'''
		self.rotation += min(PLAYER_TURN_SPEED, abs(radians)) * cmp(radians, 0) 