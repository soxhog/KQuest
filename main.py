import pygame
from pygame.locals import *
import sys

SCREEN_RECT = Rect(0, 0, 640, 480)
CS = 32 #画像のサイズ
SCREEN_NCOL = SCREEN_RECT.width//CS #スクリーンの列の個数
SCREEN_NROW = SCREEN_RECT.height//CS #スクリーンの行の個数
SCREEN_CENTER_X = SCREEN_RECT.width//2//CS
SCREEN_CENTER_Y = SCREEN_RECT.height//2//CS

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
	# image = pygame.transform.scale(image, (32*3, 32*3))
	return image

DIR_DOWN = 0
DIR_LEFT = 1
DIR_RIGHT = 2
DIR_UP = 3
ANIM_WAIT_COUNT = 24
MOVE_VELOCITY = 4
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
		self.rect.x = SCREEN_CENTER_X * CS
		self.rect.y = SCREEN_CENTER_Y * CS
		self.frame = 0
		self.anim_count = 0
		self.dir = DIR_DOWN
		self.wx, self.wy = 1, 1 #ワールドマップのデフォルト位置
		self.map = None
		self.moving = False
		self.vx, self.vy = 0, 0
		self.px, self.py = 0, 0
	def set_map(self, map_):
		self.map = map_
	def handle_keys(self):
		if self.moving:
			self.px += self.vx
			self.py += self.vy
			if self.px % CS == 0 and self.py % CS == 0:
				self.moving = False
				self.wx += self.px // CS
				self.wy += self.py // CS
				self.vx, self.vy = 0, 0
				self.px, self.py = 0, 0
		else:
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[K_DOWN]:
				self.dir = DIR_DOWN
				if self.map.can_move_at(self.wx, self.wy + 1):
					# self.wy += 1
					self.moving = True
					self.vy = MOVE_VELOCITY
			elif pressed_keys[K_UP]:
				self.dir = DIR_UP
				if self.map.can_move_at(self.wx, self.wy - 1):
					# self.wy -= 1
					self.moving = True
					self.vy = -MOVE_VELOCITY
			elif pressed_keys[K_LEFT]:
				self.dir = DIR_LEFT
				if self.map.can_move_at(self.wx - 1, self.wy):
					# self.wx -= 1
					self.moving = True
					self.vx = -MOVE_VELOCITY
			elif pressed_keys[K_RIGHT]:
				self.dir = DIR_RIGHT
				if self.map.can_move_at(self.wx + 1, self.wy):
					# self.wx += 1
					self.moving = True
					self.vx = MOVE_VELOCITY
	def update(self):
		self.anim_count += 1
		self.handle_keys()
		if self.anim_count >= ANIM_WAIT_COUNT:
			self.anim_count = 0
			self.frame += 1
			if self.frame > 3:
				self.frame = 0
		self.image = self.images[self.dir][self.frame]

class Map:
	def __init__(self, screen, filename, player):
		self.ncol = 20
		self.nrow = 15
		self.screen = screen
		self.player = player
		self.mapData = []
		self.readMap(filename)
		self.sheet0 = load_image("pipo-map001.png")
		self.sheet1 = load_image("pipo-map001_at-umi.png")
		self.images = []
		self.images.append([self.sheet1, 0, 4]) # 海(0)
		self.images.append([self.sheet0, 0, 0]) # 芝a(1)
		self.images.append([self.sheet0, 0, 1]) # 芝b(2)
		self.images.append([self.sheet0, 1, 1]) # 芝c(3)
		self.images.append([self.sheet0, 2, 1]) # 木(4)
	def readMap(self, filename):
		with open("field01.map") as fi:
			line = fi.readline()
			self.ncol, self.nrow = [int(tok) for tok in line.split(",")]
			for row in range(self.nrow):
				line = fi.readline()
				self.mapData.append([int(tok) for tok in line.split(",")])
	def drawImage(self, idx, sx, sy, px, py):
		sheet, x, y = self.images[idx]
		self.screen.blit(sheet, (sx*32 + px, sy*32 + py), (x*32, y*32, 32, 32))
	def draw(self):
		px, py = -self.player.px, -self.player.py
		screen_wx = self.player.wx - SCREEN_CENTER_X
		screen_wy = self.player.wy - SCREEN_CENTER_Y
		for sy in range(-1, SCREEN_NROW+1):
			for sx in range(-1, SCREEN_NCOL+1):
				wx = screen_wx + sx
				wy = screen_wy + sy
				if not (0 <= wx < self.ncol) or not (0 <= wy < self.nrow):
					self.drawImage(0, sx, sy, px, py) # 海
				else:
					idx = self.mapData[wy][wx]
					self.drawImage(1, sx, sy, px, py) # 芝
					self.drawImage(idx, sx, sy, px, py)

	def can_move_at(self, wx, wy): #マップで移動可能かどうか確認する関数
		if not (0 <= wx < self.ncol) or not (0 <= wy < self.nrow):
			return False
		idx = self.mapData[wy][wx]
		if idx == 0 or idx == 4: #　海と木
			return False
		else:
			return True
def main():
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_RECT.size)
	pygame.display.set_caption("KQuest") # タイトル
	player = Player("pipo-charachip021.png")
	group = pygame.sprite.RenderUpdates()
	group.add(player)
	fieldMap = Map(screen, "field01.map", player)
	player.set_map(fieldMap)
	clock = pygame.time.Clock()

	while True:
		clock.tick(60)
		# 画面に背景色
		screen.fill((0, 255, 0))
		fieldMap.draw()
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
