import json
from math import pi, cos, sin

try:
	from scene import Texture, Vector2
except ImportError:
	class Texture:
		def __init__(self, tex):
			self.tex = tex

		def __repr__(self):
			return 'Texture(\'{}\')'.format(self.tex)
		
		def __str__(self):
			return self.__repr__()

def cmp(a, b):
	return (a>b) - (a<b)
	
def lerp(A, B, t):
	return Vector2(*A)*t + Vector2(*B)*(1.0-t)
	
def rotation_vector(rotation):
	return Vector2(cos(rotation+pi/2), sin(rotation+pi/2))

def _extract(load, *args):
	for arg in args:
		if hasattr(load, 'get'):
			load = load.get(arg)
	return load

try:
	with open('settings.json', 'r') as fp:
		loaded = json.loads(fp.read())
except FileNotFoundError:
	import os
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(dir_path)
	with open('settings.json', 'r') as fp:
		loaded = json.loads(fp.read())
	
PLAYER = _extract(loaded, 'player')
PLAYER_TEXTURE = Texture(_extract(PLAYER, 'texture'))
PLAYER_SPEED = _extract(PLAYER, 'speed')
PLAYER_TURN_SPEED = _extract(PLAYER, 'turn_speed')
PLAYER_SLOWDOWN_RATE = _extract(PLAYER, 'slowdown_rate')

PLAYER_LASER = _extract(PLAYER, 'laser')
PLAYER_LASER_TEXTURE = Texture(_extract(PLAYER_LASER, 'texture'))
PLAYER_LASER_EXPLOSION = Texture(_extract(PLAYER_LASER, 'explosion'))
PLAYER_LASER_DAMAGE = _extract(PLAYER_LASER, 'damage')
PLAYER_LASER_TIME = _extract(PLAYER_LASER, 'time')
PLAYER_LASER_SPEED = _extract(PLAYER_LASER, 'speed')
PLAYER_LASER_RADIUS = _extract(PLAYER_LASER, 'radius')

CONTROLLER = _extract(loaded, 'controller')
CONTROLLER_TEXTURE = Texture(_extract(CONTROLLER, 'texture'))
CONTROLLER_ALPHA = _extract(CONTROLLER, 'alpha')

CONTROLLER_JOYSTICK = _extract(CONTROLLER, 'joystick')
CONTROLLER_JOYSTICK_TEXTURE = Texture(_extract(CONTROLLER_JOYSTICK, 'texture'))
CONTROLLER_JOYSTICK_RESET_SPEED = _extract(CONTROLLER_JOYSTICK, 'reset_speed')

COMET = _extract(loaded, 'comet')
COMET_SIZES_BIG = [(Texture(x[0]), x[1]) for x in _extract(COMET, 'sizes', 'big')]
COMET_SIZES_MED = [(Texture(x[0]), x[1]) for x in _extract(COMET, 'sizes', 'med')]
COMET_SIZES_SMALL = [(Texture(x[0]), x[1]) for x in _extract(COMET, 'sizes', 'small')]
COMET_SIZES_TINY = [(Texture(x[0]), x[1]) for x in _extract(COMET, 'sizes', 'tiny')]
COMET_MAX_SPEED = _extract(COMET, 'max_speed')
COMET_HEALTH = _extract(COMET, 'health')
COMET_MAX_COMETS = _extract(COMET, 'max_comets')
COMET_NO_COLLIDE = _extract(COMET, 'no_collide')