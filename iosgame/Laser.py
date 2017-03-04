from scene import *
from math import pi, cos, sin
from utils import *
from ui import Path

class Laser(SpriteNode):
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
		
	def move(self):
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

	def __init__(self, *args, delay=0.4, parent=None, origin=None):
		self.t = 0.0
		self.delay = delay
		self.parent = parent
		self.origin = origin
		self.sequence = args
		self.progress = 0
	
	def shoot(self):
		if self.t + self.delay <= self.parent.t:
			for shot in self.sequence[self.progress]:
				laser = Laser(self.origin, x_offset=shot.x_offset, y_offset=shot.y_offset, angle_offset=shot.angle_offset, parent=self.parent)
				self.parent.objects.append(laser)
				self.parent.lasers.append(laser)

			self.progress = (self.progress + 1) if self.progress != len(self.sequence) else 0
			self.t = self.parent.t	


class Shot:

	def __init__(self, x_offset=0, y_offset=0, angle_offset=0):
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.angle_offset = angle_offset
