from scene import *
from math import pi, cos, sin, sqrt, atan2, acos, atan
from ui import Image
from utils import *

class Joystick(SpriteNode):
	def __init__(self, **kwargs):
		SpriteNode.__init__(self, CONTROLLER_JOYSTICK, **kwargs)
		self.alpha = self.parent.alpha
		self.movement = (0, 0, 0, 0)
		self.touch_loc = (0, 0)
		self.z_position = 1.0
		
	def move_to(self, location, from_scene=True):
		self.touch_loc = self.parent.point_from_scene(location) if from_scene else location
		distance = sqrt(self.touch_loc[0]**2 + self.touch_loc[1]**2)
		if distance <= self.parent.radius:
			self.position = self.touch_loc
		else:
			self.position = (
				cos(atan2(-self.touch_loc[0], -self.touch_loc[1])+pi/2) * self.parent.radius,
				sin(atan2(self.touch_loc[0], self.touch_loc[1])+pi/2) * self.parent.radius)
			
	def reset(self):
		self.run_action(Action.move_to(0, 0, .2))
		
	def update_movement(self):
		dist = sqrt(self.position[0]**2 + self.position[1]**2)
		self.movement = (
			(self.position[0]/self.parent.radius),
			(self.position[1]/self.parent.radius),
			dist if dist <= self.parent.radius else self.parent.radius,
			(-atan(-self.position[0] / -self.position[1] if self.position[1] else .000001)+pi) + pi*(self.position[1]<0) if self.position != (0, 0) else self.movement[3])
			

class Controller(SpriteNode):
	def __init__(self, padding, **kwargs):
		SpriteNode.__init__(self, CONTROLLER_TEXTURE, **kwargs)
		self.anchor_point = (.5, .5)
		self.position = (
			(self.size.w/2 + padding) * self.scale,
			(self.size.h/2 + padding) * self.scale)
		self.joystick = Joystick(parent=self)
		self.alpha = CONTROLLER_ALPHA
		self.radius = self.size.w/2-10
		self.touch_id = 0x0
		self.z_position = 1.0