from scene import *
from math import pi, cos, sin
from utils import *
from ui import Path
from Laser import Laser
		

class Player(SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, PLAYER_TEXTURE, **kwargs)
		self.position = self.parent.center
		self.pos = Vector2(.0, .0)
		self.anchor_point = (.5, .5)
		self.laser_side = 1
		self.velocity = Vector2(.0, .0)
		self.label = LabelNode('', parent=self, position=(0, 60))
		
	def move(self):
		self.pos = self.pos + self.velocity
		
	def update_vel(self, dist):
		self.velocity = lerp(
			self.velocity,
			rotation_vector(self.rotation)*dist*self.speed,
			PLAYER_SLOWDOWN_RATE)
	
	def rotate(self, radians):
		self.rotation += min(PLAYER_TURN_SPEED, abs(radians)) * cmp(radians, 0) 
		
	def shoot(self):
		self.laser_side *= -1
		laser = Laser(origin=self, parent=self.parent, x_offset=(self.size.w/2-4)*self.laser_side, y_offset=10, speed=1)
		self.parent.lasers.append(laser)
		
	def bounds_collision(self):
		dx, dy = self.velocity
		awayDx, awayDy = moveRelative(other, -1)
		dx = dx + self.speed * awayDx
		dy = dy + self.speed * awayDy
		self.velocity = Vector2(dx, dy)
