from scene import *
from Player import Player
from Controls import Controller, FireBtn
from Comet import Comet
from math import pi, cos, sin, atan2
from utils import *
from random import random, randrange
from ui import Path
from Laser import *

class Game(Scene):
	'''
	The Scene object where the gameplay is handled
	'''
	
	def setup(self):
		'''Called to initialize the game'''

		self.center = (self.size.w/2, self.size.h/2)
		self.player = Player(parent=self, speed=PLAYER_SPEED)
		self.controller = Controller(padding=40, scale=1.2, parent=self)
		self.firebtn = FireBtn(70, parent=self)
		self.background_color = '#003f68'
		self.objects = list()
		self.lasers = list()
		self.comets = list()
		self.pos = (.0, .0)
		self.firing = False
		
		self.player_sequence = Sequence(
			[Shot(x_offset=40, y_offset=20), Shot(x_offset=-40, y_offset=20)], 
			origin=self.player, delay=0.2)

		self.spawn_area = ShapeNode(
			Path.rect(*self.bounds),
			alpha=0,
			parent=self, 
			scale=2, 
			position=self.size/2)
		
	def update(self):
		'''Called, preferably, 60 times a second'''

		if len(self.comets) <= COMET_MAX_COMETS and round(self.t) % 0.25 == 0: 
			new_comet = Comet.spawn_in(
				self,
				self.spawn_area.frame, 
				self.bounds, 
				self.player.pos,
				self.comets,
				comet_size='big',
				scale=max(1, random()*2),
				speed=randrange(0, COMET_MAX_SPEED))
			self.objects.append(new_comet)
			self.comets.append(new_comet)
			
		if self.firing:
			self.player_sequence.shoot()
		
		self.controller.joystick.update_movement()
		joystick_vector = Vector2(*self.controller.joystick.movement[:2])
		if self.player.velocity != joystick_vector:
			self.player.update_vel(self.controller.joystick.movement[2]/self.controller.radius)
			self.player.rotate(((self.controller.joystick.movement[3]-self.player.rotation)%(2*pi)-pi)*.05)
			
		self.player.move()
		self.pos = (self.center[0] - self.player.pos[0], self.center[1] - self.player.pos[1])
		self.check_comet_collisions()
		self.check_laser_collisions()
		self.move_objects()

	def move_objects(self):
		'''Moves every Node in self.objects to give the impression self.player moved'''

		for obj in list(self.objects):
			obj.position = (obj.pos[0] - self.player.pos[0], obj.pos[1] - self.player.pos[1])
			if isinstance(obj, Comet): 
				if max([abs(x+self.size.w/2) for x in obj.position]) > self.size.w*2:
					self.objects.remove(obj)
					self.comets.remove(obj)
					obj.remove_from_parent()
				obj.pos += rotation_vector(obj.direction) * obj.speed
				
	def check_comet_collisions(self):
		'''Checks and handles Comet to Comet collisions'''

		for comet in list(self.comets):
			for other in list(self.comets):
				if other == comet:
					continue
				if comet.frame.intersects(other.frame) and comet.collides_with_other(other):
					x1, y1 = comet.position
					x2, y2 = other.position
					r1 = comet.radius
					r2 = other.radius
					
					collisionPoint = Point( (x1 * r2 + x2 * r1) / (r1 + r2), (y1 * r2 + y2 * r1) / (r1 + r2) )
			
					mass1 = comet.mass
					mass2 = other.mass
					velX1, velY1 = rotation_vector(comet.direction) * comet.speed
					velX2, velY2 = rotation_vector(other.direction) * other.speed
					
					newVelX1 = (velX1 * (mass1 - mass2) + (2 * mass2 * velX2)) / (mass1 + mass2)
					newVelX2 = (velX2 * (mass2 - mass1) + (2 * mass1 * velX1)) / (mass1 + mass2)
					newVelY1 = (velY1 * (mass1 - mass2) + (2 * mass2 * velY2)) / (mass1 + mass2)
					newVelY2 = (velY2 * (mass2 - mass1) + (2 * mass1 * velY1)) / (mass1 + mass2)

					comet.health -= other.mass * other.speed / 100
					other.health -= comet.mass * comet.speed / 100
					
					comet.position += Vector2(-velX1, -velY1) 
					comet.pos += Vector2(-velX1, -velY1) 
					comet.direction = -atan2(newVelX1, newVelY1)
					comet.speed = abs(Vector2(newVelX1, newVelY1))
					
					other.position += Vector2(-velX2, -velY2)
					other.pos += Vector2(-velX2, -velY2)
					other.direction = -atan2(newVelX2, newVelY2)
					other.speed = abs(Vector2(newVelX1, newVelY1))	
					
					comet.check_health()
					other.check_health()
					
	def check_laser_collisions(self):
		'''Moves, checks and handles Laser to Comet collisions '''

		for laser in list(self.lasers):
			laser.move()
			if laser.dead:
				continue
			for comet in self.comets:
				if laser.frame.intersects(comet.frame) and comet.collides_with_other(laser):
					laser.counter = 0
					laser.z_position = comet.z_position+.1
					comet.health -= laser.damage
					comet.check_health()
	
	def touch_began(self, touch):
		'''Called when a touch is initiated'''

		if touch.location in self.controller.frame:
			self.controller.touch_id = touch.touch_id
			self.controller.run_action(Action.fade_to(1, .2))
			self.controller.joystick.remove_all_actions()
			self.controller.joystick.touch_loc = self.controller.point_from_scene(touch.location)
			self.controller.joystick.move_to(touch.location)
		
		elif touch.location in self.firebtn.frame:
			self.firebtn.touch_id = touch.touch_id
			self.firebtn.start()
			
		
	def touch_moved(self, touch):
		'''Called when a touch moved'''

		if touch.touch_id == self.controller.touch_id:
			self.controller.joystick.move_to(touch.location)
		
	def touch_ended(self, touch):
		'''Called when a touch ended'''

		if touch.touch_id == self.controller.touch_id:
			self.controller.joystick.reset()
			self.controller.run_action(Action.fade_to(.4, .2))
			
		elif touch.touch_id ==self.firebtn.touch_id:
			self.firebtn.stop()
		
		
if __name__ == '__main__':
	 
	# Run the game
	run(Game(), LANDSCAPE, show_fps=True)
