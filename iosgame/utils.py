import json
from scene import Texture, Vector2
from math import pi, cos, sin

def cmp(a, b):
	return (a>b) - (a<b)
	
def lerp(A, B, t):
	return Vector2(*A)*t + Vector2(*B)*(1.0-t)
	
def rotation_vector(rotation):
	return Vector2(cos(rotation+pi/2), sin(rotation+pi/2))

with open('settings.json', 'r') as fp:
	loaded = json.loads(fp.read())
	
PLAYER_TEXTURE = Texture(loaded.get('player').get('texture'))
PLAYER_LASER_TEXTURE = Texture(loaded.get('player').get('laser_texture'))
PLAYER_LASER_EXPLOSION = Texture(loaded.get('player').get('laser_explosion'))
PLAYER_LASER_DAMAGE = loaded.get('player').get('laser_damage')
PLAYER_SPEED = loaded.get('player').get('speed')
PLAYER_TURN_SPEED = loaded.get('player').get('turn_speed')
PLAYER_SLOWDOWN_RATE = loaded.get('player').get('slowdown_rate')

CONTROLLER_TEXTURE = Texture(loaded.get('controller').get('texture'))
CONTROLLER_ALPHA = loaded.get('controller').get('alpha')
CONTROLLER_JOYSTICK = Texture(loaded.get('controller').get('joystick'))

COMET_TEXTURES_BIG = [Texture(x) for x in loaded.get('comet').get('textures').get('big')]
COMET_TEXTURES_MED = [Texture(x) for x in loaded.get('comet').get('textures').get('med')]
COMET_TEXTURES_SMALL = [Texture(x) for x in loaded.get('comet').get('textures').get('small')]
COMET_TEXTURES_TINY = [Texture(x) for x in loaded.get('comet').get('textures').get('tiny')]
COMET_MAX_SPEED = loaded.get('comet').get('max_speed')
COMET_HEALTH = loaded.get('comet').get('health')


