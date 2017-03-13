from scene import *
from math import pi, cos, sin
from utils import *
from ui import Path

class Laser(SpriteNode):
	'''
	Represents a laser fired by a spaceship

	Parameters:
	----------
	origin : Node
		The objects the Laser originates from
	x_offset : int, float
		How far off `origins.position.x` the laser is created
	y_offset : int, float
		How far off `origins.position.y` the laser is created
	angle_offset : int, float
		The angle, in radians, the Laser is rotated when the laser is created
	'''

	def __init__(self, origin, x_offset=0, y_offset=0, angle_offset=0, **kwargs):
		self.origin = origin
		y_offset *= -1
		SpriteNode.__init__(self, PLAYER_LASER_TEXTURE, **kwargs)
		self.parent.objects.append(self)
		self.rotation = self.origin.rotation + angle_offset
		self.position = origin.position + (
			x_offset*cos(self.rotation) + y_offset*sin(self.rotation),
			x_offset*sin(self.rotation) - y_offset*cos(self.rotation))
		self.pos = self.position + origin.pos + origin.velocity
		self.z_position = -1
		self.distance = self.size.h * 5
		self.damage = PLAYER_LASER_DAMAGE
		self.dead = False
		self.velocity = rotation_vector(self.rotation)*16+origin.velocity
		self.counter = PLAYER_LASER_TIME
		self.radius = PLAYER_LASER_RADIUS
		
	def move(self):
		'''
		Called once per frame
		Moves and destroys the laser depnding on how many times `move` have been called
		'''

		if self.dead:
			if self.counter <= -8:
				self.parent.objects.remove(self)
				self.parent.lasers.remove(self)
				self.remove_from_parent()
		elif self.counter <= 0:
			self.dead = True
			self.texture = PLAYER_LASER_EXPLOSION
		else:
			self.pos = self.pos + self.velocity
		self.counter -= 1


class Sequence:
	'''
	Represents a sequence of `Shot`s

	Parameters:
	----------
	*args : list
		Bursts of shots
	delay : int, float
		The time, in seconds, between a shot
	origin : Node
		The Node which shots originate from
	'''

	def __init__(self, *args, delay=0.4, origin=None):
		self.t = 0.0
		self.delay = delay
		self.origin = origin
		self.parent = origin.parent
		self.sequence = args
		self.progress = 0
	
	def shoot(self):
		'''
		Called to check if at least self.delay seconds have passed since last shot
		If True, fire the next volley of shots
		'''
		if self.t + self.delay <= self.parent.t:

			for shot in self.sequence[self.progress]:
				laser = Laser(self.origin, x_offset=shot.x_offset, y_offset=shot.y_offset, angle_offset=shot.angle_offset, parent=self.parent)
				self.parent.objects.append(laser)
				self.parent.lasers.append(laser)

			self.progress = (self.progress + 1) if self.progress != len(self.sequence)-1 else 0
			self.t = self.parent.t	


class Shot:
	'''
	Simple class that holds the nessecary variables to __init__ a Laser object
	
	Parameters:
	----------
	x_offset : int, float
	y_offset : int, float
	angle_offset : int, float
	'''

	def __init__(self, x_offset=0, y_offset=0, angle_offset=0):
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.angle_offset = angle_offset
