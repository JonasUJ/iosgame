from scene import *
from utils import *
from random import random, randrange
from math import pi, cos, sin, sqrt


class Comet(SpriteNode):
	'''
	Represents a comet in the game
	Comets are assigned a random texture, depending on *comet_size*, during __init__ 

	Parameters:
	----------
	comet_size : str, int
		The size of the comet
	'''

	def __init__(self, comet_size='big', **kwargs):
		self.comet_size = comet_size

		if isinstance(self.comet_size, str):
			 self.comet_size = {
				'big': 3,
				'med': 2,
				'small': 1,
				'tiny': 0}[self.comet_size]

		self.looks = {
			3: COMET_SIZES_BIG,
			2: COMET_SIZES_MED,
			1: COMET_SIZES_SMALL,
			0: COMET_SIZES_TINY}[self.comet_size]

		tex, self.diameter = self.looks[randrange(0, len(self.looks))]
		
		SpriteNode.__init__(self, tex,  **kwargs)

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
		self.no_collide = 0.0

	def collides_with_other(self, other):
		'''
		True if self is colliding with `other` otherwise False
		Collision is determined using the distance between self and `other` and their radii
		Raises AttributeError if `other` does not have a radius
		'''
		distance = sqrt(((self.position.x - other.position.x) * (self.position.x - other.position.x)) + ((self.position.y - other.position.y) * (self.position.y - other.position.y)))		
		distance *= cmp(distance, 0)
		return distance <= self.radius + other.radius
		
	def check_health(self):
		'''
		Checks is self.health <= 0
		If True, spawns new, smaller, comets
		'''
		if self.health <= 0 and self.parent:
			new_comets = list()
			for i in range(self.comet_size if self.comet_size else 0):
				ncomet = Comet(
					parent=self.parent,
					comet_size=self.comet_size-1,
					scale=self.scale,
					speed=self.speed)
				ncomet.pos = self.pos
				ncomet.rotation = self.rotation+(0.5-random())
				self.parent.objects.append(ncomet)
				self.parent.comets.append(ncomet)
				new_comets.append(ncomet)
			
			for comet in new_comets:
				for other in new_comets:
					if comet == other:
						continue
					while comet.collides_with_other(other):
						comet.position += rotation_vector(comet.direction) * 10
					comet.pos = comet.position + self.pos
			
			self.parent.objects.remove(self)
			self.parent.comets.remove(self)
			self.remove_from_parent()
		
	@classmethod
	def spawn_in(self, parent, area, outside_area, origin_pos, collidables, **kwargs):
		'''
		Returns a Comet(parent=`parent`, **kwargs)
		The comet is not intersecting `outside_area` and is contained in `area`
		The comet is also not intersectin any SpriteNode in `collidables`
		'''
		comet = Comet(position=outside_area.size/2, parent=parent, **kwargs)
		
		while (comet.frame.intersects(outside_area)) or \
		(True in [obj.frame.intersects(comet.frame) for obj in collidables]):
			comet.position = (randrange(area.x, area.size.w), randrange(area.y, area.size.h))
		
		comet.pos = comet.position + origin_pos
		return comet
