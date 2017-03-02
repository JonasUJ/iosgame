from scene import *
from utils import *
from random import choice, random,randrange
from math import pi, cos, sin


class Comet(SpriteNode):
	def __init__(self, size='big', **kwargs):
		if isinstance(size, str):
			 size = {
				'big': 4,
				'med': 3,
				'small': 2,
				'tiny': 1}[size]
		self.looks = {
			4: COMET_TEXTURES_BIG,
			3: COMET_TEXTURES_MED,
			2: COMET_TEXTURES_SMALL,
			1: COMET_TEXTURES_TINY}[size]
		SpriteNode.__init__(self, choice(self.looks), **kwargs)
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
