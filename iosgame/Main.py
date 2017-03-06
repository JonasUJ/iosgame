from scene import *
from Player import Player
from Controller import Controller
from Comet import Comet
from math import pi, cos, sin, atan2
from utils import *
from random import random, randrange
from ui import Path
from Laser import *

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
		
		self.player_sequence = Sequence(
			[Shot(x_offset=40), Shot(x_offset=-40), Shot(y_offset=80)], 
			origin=self.player, parent=self, delay=0.1)

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
			self.player_sequence.shoot()
			if len(self.comets) <= COMET_MAX_COMETS:
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
				obj.pos += rotation_vector(obj.direction) * obj.speed
				#obj.label.text = str(obj.health)
				
	def move_lasers(self):
		for laser in self.lasers:
			laser.move()
				
	def check_comet_collisions(self):
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
					
					comet.position += Vector2(newVelX1, newVelY1) 
					comet.pos += Vector2(newVelX1, newVelY1) 
					comet.direction = -atan2(newVelX1, newVelY1)
					comet.speed = abs(Vector2(newVelX1, newVelY1))
					
					other.position += Vector2(newVelX2, newVelY2)
					other.pos += Vector2(newVelX2, newVelY2)
					other.direction = -atan2(newVelX2, newVelY2)
					other.speed = abs(Vector2(newVelX1, newVelY1))	
					
	def check_laser_collisions(self):
		for laser in list(self.lasers):
			if laser.dead:
				continue
			for comet in self.comets:
				if laser.frame.intersects(comet.frame) and comet.collides_with_other(laser):
					laser.counter = 0
					laser.z_position = comet.z_position+.1
					comet.health -= laser.damage
	
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
