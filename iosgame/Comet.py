from scene import *
from utils import *
from random import random, randrange
from math import pi, cos, sin, sqrt


class Comet(SpriteNode):
	def __init__(self, comet_size='big', **kwargs):
		self.comet_size = comet_size

		if isinstance(self.comet_size, str):
			 self.comet_size = {
				'big': 4,
				'med': 3,
				'small': 2,
				'tiny': 1}[self.comet_size]

		self.looks = {
			4: COMET_SIZES_BIG,
			3: COMET_SIZES_MED,
			2: COMET_SIZES_SMALL,
			1: COMET_SIZES_TINY}[self.comet_size]

		tex, self.diameter = self.looks[randrange(0, len(self.looks))]

		SpriteNode.__init__(self, tex, **kwargs)

		self.diameter *= self.scale
		self.radius = self.diameter/2
		self.mass = self.scale * self.radius
		self.speed /= self.scale
		self.pos = self.position
		self.rotation = random()*2*pi
		self.direction = self.rotation
		self.label = LabelNode('', parent=self)
		self.label.rotation = 0-self.rotation
		self.health = (COMET_HEALTH*self.comet_size)**self.scale
		self.no_collide = COMET_NO_COLLIDE

	def collides_with_other(self, other):
		distance = sqrt(((self.position.x - other.position.x) * (self.position.x - other.position.x)) + ((self.position.y - other.position.y) * (self.position.y - other.position.y)))
		if distance < 0: 
			distance *= -1

		return distance <= self.radius + other.radius
		
	@classmethod
	def spawn_in(self, parent, area, outside_area, origin_pos, collidables, **kwargs):
		comet = Comet(position=outside_area.size/2, parent=parent, **kwargs)
		
		while (comet.frame.intersects(outside_area)) and \
		(True in [obj.frame.intersects(comet.frame) for obj in collidables]):
			comet.position = (randrange(area.x, area.size.w), randrange(area.y, area.size.h))
			#print(comet.frame.intersects(outside_area), comet.scale)
		#print(comet.frame.intersects(outside_area), comet.scale)
		
		comet.pos = comet.position + origin_pos
		return comet
