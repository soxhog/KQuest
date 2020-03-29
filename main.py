import pygame
from pygame.locals import *
import sys

SCREEN_RECT = Rect(0, 0, 640, 480)

def main():
	pygame.init()
	pygame.display.set_mode(SCREEN_RECT.size)
	# pygame.quit()
	while True:
		# 画面に背景色
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
