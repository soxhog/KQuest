import pygame
from pygame.locals import *
import sys

SCREEN_RECT = Rect(0, 0, 640, 480)

def load_image(filename):
	image = pygame.image.load(filename)
	# image = image.convert_alpha()
	return image

def get_image(sheet, x, y, width, height, useColorKey=False):
	image = pygame.Surface([width, height])
	image.blit(sheet, (0, 0), (x, y, width, height))
	image = image.convert_alpha()
	if useColorKey:
		colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, RLEACCEL)
	image = pygame.transform.scale(image, (32*3, 32*3))
	return image

DIR_DOWN = 0
DIR_LEFT = 1
DIR_RIGHT = 2
DIR_UP = 3
ANIM_WAIT_COUNT = 24

class Player(pygame.sprite.Sprite):
	def __init__(self, filename):
		pygame.sprite.Sprite.__init__(self)
		sheet = load_image(filename)
		self.images = [[], [], [], []]
		for row in range(0, 4):
			for col in [0, 1, 2 ,1]:
				self.images[row].append(get_image(sheet, 0+32*col, 0+32*row, 32, 32, True)) #画像をplayerに入れる
		self.image = self.images[DIR_DOWN][0]
		self.rect = self.image.get_rect()
		self.rect.center = (SCREEN_RECT.width//2, SCREEN_RECT.height//2)
		self.frame = 0
		self.anim_count = 0
		self.dir = DIR_DOWN

	def update(self):
		self.anim_count += 1
		if self.anim_count >= ANIM_WAIT_COUNT:
			self.anim_count = 0
			self.frame += 1
			if self.frame > 3:
				self.frame = 0
		self.image = self.images[self.dir][self.frame]

def main():
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_RECT.size)
	pygame.display.set_caption("KQuest") # タイトル
	player = Player("pipo-charachip021.png")
	group = pygame.sprite.RenderUpdates()
	group.add(player)
	clock = pygame.time.Clock()

	while True:
		clock.tick(60)
		# 画面に背景色
		screen.fill((0, 255, 0))
		group.update() #groupをupdate
		group.draw(screen) #groupをscreenに
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == QUIT: # バツボタン押したとき画面終了
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE: # エスケープボタン押したとき画面終了
					pygame.quit()
					sys.exit()

if __name__ == "__main__":
	main()



# -----------------------------------------------------------------------------
# import pygame
# from pygame.locals import *
# import sys

# SCREEN_RECT = Rect(0, 0, 640, 480)

# def load_image(filename):
# 	image = pygame.image.load(filename)
# 	# image = image.convert_alpha()
# 	return image

# def main():
# 	pygame.init()
# 	screen = pygame.display.set_mode(SCREEN_RECT.size)
# 	pygame.display.set_caption("KQuest")
# 	player = load_image("pipo-charachip021.png")
# 	while True:
# 		screen.fill((0, 255, 0))
# 		screen.blit(player, (0, 0))
# 		pygame.display.update()

# 		for event in pygame.event.get():
# 			if event.type == QUIT: # バツボタン押したとき画面終了
# 				pygame.quit()
# 				sys.exit()
# 			elif event.type == KEYDOWN:
# 				if event.key == K_ESCAPE: # エスケープボタン押したとき画面終了
# 					pygame.quit()
# 					sys.exit()

# if __name__ == "__main__":
# 	main()
