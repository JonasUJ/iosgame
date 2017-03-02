from scene import *
from Player import Player
from Controller import Controller
from Comet import Comet
from math import pi, atan2, cos, sin
from utils import *
from random import randrange
from ui import Path
from Laser import Laser

class Game(Scene):
	
	def setup(self):
		self.center = (self.size.w/2, self.size.h/2)
		self.player = Player(parent=self, speed=PLAYER_SPEED)
		self.controller = Controller(padding=40, scale=1.2, parent=self)
		self.frameno = 1
		self.background_color = '#003f68'
		self.objects = list()
		self.lasers = list()
		self.comets = list()
		self.pos = (.0, .0)

		self.spawn_area = ShapeNode(
			Path.rect(*self.bounds),
			alpha=0,
			parent=self, 
			scale=2, 
			position=self.size/2)
		
	def update(self):
		self.controller.joystick.update_movement()
		self.frameno = (self.frameno + 1) if self.frameno != 60 else 1
		if not self.frameno % 15 and self.frameno:
			self.player.shoot()
			if len(self.comets) <= COMET_MAX_COMETS:
				new_comet = Comet.spawn_in(
					self,
					self.spawn_area.frame, 
					self.bounds, 
					self.player.pos,
					speed=randrange(0, COMET_MAX_SPEED))
				self.objects.append(new_comet)
				self.comets.append(new_comet)
			
		joystick_vector = Vector2(*self.controller.joystick.movement[:2])
		if self.player.velocity != joystick_vector:
			self.player.update_vel(self.controller.joystick.movement[2]/self.controller.radius)
			self.player.rotate(((self.controller.joystick.movement[3]-self.player.rotation)%(2*pi)-pi)*.05)
			
		self.player.move()
		self.pos = (self.center[0] - self.player.pos[0], self.center[1] - self.player.pos[1])
		self.check_comet_collisions()
		self.check_laser_collisions()
		self.move_objects()
		self.move_lasers()
		self.player.label.text = str(self.player.velocity)
		self.player.label.rotation = 0-self.player.rotation
		
	def move_objects(self):
		for obj in list(self.objects):
			obj.position = (obj.pos[0] - self.player.pos[0], obj.pos[1] - self.player.pos[1])
			if isinstance(obj, Comet):
				if max([abs(x+self.size.w/2) for x in obj.position]) > self.size.w*2:
					self.objects.remove(obj)
					self.comets.remove(obj)
					obj.remove_from_parent()
				obj.pos += rotation_vector(obj.rotation) * obj.speed
				obj.label.text = str(obj.health)
				
	def move_lasers(self):
		for laser in self.lasers:
			laser.move()
				
	def check_comet_collisions(self):
		print(self.comets)
		for comet in list(self.comets):
			if comet.no_collide > self.t:
				continue
			else:
				comet.no_collide = self.t + COMET_NO_COLLIDE
			for other in list(self.comets):
				if other == comet:
					continue
				if comet.frame.intersects(other.frame):
					comet.rotation *= -1
					comet.no_collide = COMET_NO_COLLIDE
					other.rotaion *= -1
					other.no_collide = COMET_NO_COLLIDE		
					
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if laser.dead:
				continue
			for obj in self.objects:
				if isinstance(obj, Laser):
					continue
				elif isinstance(obj, Comet) and laser.frame.intersects(obj.frame):
					laser.counter = 0
					laser.z_position = obj.z_position+.1
					obj.health -= laser.damage
	
	def touch_began(self, touch):
		if touch.location in self.controller.frame:
			self.controller.touch_id = touch.touch_id
			self.controller.run_action(Action.fade_to(1, .2))
			self.controller.joystick.remove_all_actions()
			self.controller.joystick.touch_loc = self.controller.point_from_scene(touch.location)
			self.controller.joystick.move_to(touch.location)
		
	def touch_moved(self, touch):
		if touch.touch_id == self.controller.touch_id:
			self.controller.joystick.move_to(touch.location)
		
	def touch_ended(self, touch):
		if touch.touch_id == self.controller.touch_id:
			self.controller.joystick.reset()
			self.controller.run_action(Action.fade_to(.4, .2))
		
		
if __name__ == '__main__':
	run(Game(), LANDSCAPE, show_fps=True)
