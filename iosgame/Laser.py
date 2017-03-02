from scene import *
from math import pi, cos, sin, atan2
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
		'''
		self.move_by = (
			self.distance*cos(self.rotation+pi/2),
			self.distance*sin(self.rotation+pi/2))
		self.run_action(
			Action.sequence([
				Action.move_by(*self.move_by),
				Action.call(lambda: setattr(self, 'alpha', 0)),
				Action.call(lambda: setattr(self, 'pos', (self.origin.pos[0] + self.pos[0] + self.move_by[0], self.origin.pos[1] + self.pos[1] + self.move_by[1]))),
				Action.call(self._explode),
				Action.wait(.2),
				Action.call(lambda: setattr(self, 'dead', True)),
				Action.remove()]))
		
				
	def _explode(self):
		self.texture = PLAYER_LASER_EXPLOSION
		self.alpha = 1
		
			'''
