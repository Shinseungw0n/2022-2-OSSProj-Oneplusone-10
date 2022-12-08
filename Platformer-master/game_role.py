#font, fontcolor
#player lava, enemy

import pygame
from pygame.locals import *
from game_value import *
import pickle
from os import path
from game_image_sound import *
from game_setting import *

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)


#define font
font = pygame.font.Font('Puradak Gentle Gothic OTF.otf', 50)
font_score = pygame.font.Font('Puradak Gentle Gothic OTF.otf', 20)

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0

	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1

