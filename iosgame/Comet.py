from scene import *
from utils import *
from random import random, randrange
from math import pi, cos, sin


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
			4: COMET_SIZES_BIG[0],
			3: COMET_SIZES_MED[0},
			2: COMET_SIZES_SMALL[0],
			1: COMET_SIZES_TINY[0]}[self.comet_size]

		tex, self.radius = randrange(0, len(self.looks)-1)

		SpriteNode.__init__(self, tex, **kwargs)

		self.pos = self.position
		self.rotation = random()*2*pi
		self.label = LabelNode(str(self.position), parent=self)
		self.label.rotation = 0-self.rotation
		self.health = (COMET_HEALTH*size)**self.scale
		self.no_collide = COMET_NO_COLLIDE
		
	@classmethod
	def spawn_in(self, parent, area, outside_area, origin_pos, **kwargs):
		pos = Point(*(outside_area.size/2))
		while outside_area.contains_point(pos):
			pos = (randrange(area.x, area.size.w), randrange(area.y, area.size.h))

		comet = Comet(position=pos, parent=parent, **kwargs)
		comet.pos = pos + origin_pos
		return comet
