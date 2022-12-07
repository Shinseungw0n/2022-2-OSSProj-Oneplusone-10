import pygame
from pygame.locals import *
from pygame import mixer
from game_value import *
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('Platformer')



#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)


#load images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_bt.png')
start_img = pygame.image.load('img/start_bt.png')
store_img = pygame.image.load('img/store_bt.png')
option_img = pygame.image.load('img/option_bt.png')
score_img = pygame.image.load('img/score_bt.png')
exit_img = pygame.image.load('img/exit_bt.png')
easy_mode_img = pygame.image.load('img/easy_mode_bt.png')
hard_mode_img = pygame.image.load('img/hard_mode_bt.png')
game_rule_img = pygame.image.load('img/game_rule_bt.png')
sound_on_img = pygame.image.load('img/sound_on_bt.png')
sound_off_img = pygame.image.load('img/sound_off_bt.png')
home_img = pygame.image.load('img/home_bt.png')
back_img = pygame.image.load('img/back_bt.png')
game_rule_page = pygame.image.load('img/game_rule_pg.jpg')
skin_img = pygame.image.load('img/skin_bt.png')
my_skin_img = pygame.image.load('img/my_skin_bt.png')
playing_home_img = pygame.image.load('img/playing_home_bt.png')
winter_ako_img = pygame.image.load('img/winter_ako1.png')
school_ako_img = pygame.image.load('img/school_ako1.png')
graduation_ako_img = pygame.image.load('img/graduation_ako1.png')
coin_img = pygame.image.load('img/coin.png')
buy_img = pygame.image.load('img/buy_bt.png')

#load sounds
pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound('img/coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('img/game_over.wav')
game_over_fx.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)  
	screen.blit(img, (x, y))  # screen.blit(이미지, 대상) -> 이미지 복사


#function to reset level
def reset_level(level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'level{level}_data'):  # 파일 또는 폴더 존재 여부 확인
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world 

def reset_hard_level(hard_level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	#load in level data and create world
	if path.exists(f'hard_level{hard_level}_data'):  # 파일 또는 폴더 존재 여부 확인
		pickle_in = open(f'hard_level{hard_level}_data', 'rb')
		hard_world_data = pickle.load(pickle_in)
	hard_world = World(hard_world_data)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return hard_world 


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()  # 마우스 위치

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action


class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
				jump_fx.play()
				self.vel_y = -15
				self.jumped = True
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 2 #하드모드의 경우 +=2, 이지모드의 경우 +=1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 2 #하드모드의 경우 +=2, 이지모드의 경우 +=1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1

			# x방향과 y방향 모두 충돌이 발생하도록 설정
			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1  # 캐릭터를 한 픽셀 위에 넣기 위해
						self.in_air = False
						dy = 0
					#move sideways with the platform  -> 캐릭터가 플랫폼과 함께 직접 좌우이동
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

        
		elif game_over == -1:   
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200:   # 죽으면 유령으로 바뀌고 설정한 범위만큼 위로 올라감
				self.rect.y -= 5   
            

            
            

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over


	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/ako{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True



class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1
			row_count += 1


	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])



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


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/platform.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y


	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1
   
   
class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



player = Player(100, screen_height - 130)

# 각 스프라이트 마다 group을 지정
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# 맵 로드해주는 코드를 이지모드와 하드모드로 구분하여 진행하므로 각각의 게임 모드안에 reset_level 함수를 호출하여 맵을 로드시킴 
# load in level data and create world 
# if path.exists(f'level{level}_data'):
# 	pickle_in = open(f'level{level}_data', 'rb')
# 	world_data = pickle.load(pickle_in)
# world_easy = World(world_data)

# if path.exists(f'hard_level{hard_level}_data'):
# 	pickle_in = open(f'hard_level{hard_level}_data', 'rb')
# 	hard_world_data = pickle.load(pickle_in)
# world_hard = World(hard_world_data)

 
#create buttons

start_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 - (screen_height*0.3), start_img)
store_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 - (screen_height*0.15), store_img)
option_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2, option_img)
exit_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 + (screen_height*0.15), exit_img)
easy_mode_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 - (screen_height*0.1), easy_mode_img)
hard_mode_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 + (screen_height*0.1), hard_mode_img)
game_rule_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 + (screen_height*0.1), game_rule_img)
sound_on_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 - (screen_height*0.1), sound_on_img)
back_img_button = Button(screen_width // 2 - (screen_width*0.47), screen_height // 2 - (screen_height*0.47), back_img)
sound_off_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 - (screen_height*0.1), sound_off_img)
restart_button = Button(screen_width // 2 - (screen_width*0.05), screen_height // 2 + (screen_height*0.1), restart_img)
home_button = Button(screen_width // 2 - (screen_width*0.05), screen_height // 2 - (screen_height*0.1), home_img)
skin_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 - (screen_height*0.1), skin_img)
my_skin_button = Button(screen_width // 2 - (screen_width*0.16), screen_height // 2 + (screen_height*0.1), my_skin_img)
playing_home_button = Button(screen_width // 2 + (screen_width*0.46) , screen_height // 2 - (screen_height*0.49), playing_home_img)
buy_button1 = Button(screen_width// 2 - (screen_width*0.32), screen_height// 2, buy_img)
buy_button2 = Button(screen_width// 2 - (screen_width*0.03), screen_height// 2, buy_img)
buy_button3 = Button(screen_width// 2 + (screen_width*0.27), screen_height// 2, buy_img)

run = True
while run:
	# print(main_menu)
	clock.tick(fps)

	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100))

	if main_menu == True:
		if exit_button.draw(): # exit 버튼 누르면 while 반복 루프에서 벗어남
			run = False     
		if start_button.draw(): # start 버튼 누르면 
			main_menu = "main_screen" #2
		if store_button.draw(): # store 버튼 누르면 
			main_menu = "skin" #3
		if option_button.draw(): # option 버튼 누르면 
			main_menu = "option" #4
   
	
	elif main_menu == "main_screen":  #2 start 버튼 눌렀을때 페이지 
		screen.blit(bg_img, (0,0))
		screen.blit(sun_img, (100,100))

		if back_img_button.draw():  # 뒤로가기 버튼 기능 구현 -> 메인 메뉴 페이지로
			main_menu = True
		if easy_mode_button.draw(): # easy mode 버튼 눌렀을때 게임 실행
			main_menu = "easy"
			start_ticks = pygame.time.get_ticks() #시작 시간 설정
			total_time = 6 #초안 그래도 10분, 600초로 설정(임시)
			flag = False
		if hard_mode_button.draw(): 
			main_menu = "hard"
			start_ticks = pygame.time.get_ticks() #시작 시간 설정
			total_time = 6 #초안 그래도 10분, 600초로 설정(임시)
			flag = False
   
	elif main_menu == "skin":  #3 start 버튼 눌렀을때 페이지 
		screen.blit(bg_img, (0,0))
		screen.blit(sun_img, (100,100))

		if back_img_button.draw():  # 뒤로가기 버튼 기능 구현 -> 메인 메뉴 페이지로
			main_menu = True 
		if skin_button.draw():
			main_menu = 3.5
		my_skin_button.draw()
	
	elif main_menu == 3.5: #skin 페이지
		screen.blit(bg_img, (0,0))
		screen.blit(sun_img, (100,100))

		coin_img = pygame.transform.scale(coin_img, (25,25)) #코인 이미지 리사이징 해서 불러오기

		black = (0,0,0) #검정

		#겨울 아코
		my_font = pygame.font.Font('DungGeunMo.ttf', 25)  #폰트 설정
		winter_ako_img = pygame.transform.scale(winter_ako_img, (200,200))
		screen.blit(winter_ako_img, (100,200))
		item1 = my_font.render("50",True,black)  #텍스트가 표시된 Surface 를 만듬
		screen.blit(coin_img, (200,450))
		screen.blit(item1,(240,450)) #텍스트를 화면에 출력
		buy_button1.draw()
  
		#과잠 아코
		school_ako_img = pygame.transform.scale(school_ako_img, (200,200))
		screen.blit(school_ako_img, (400,200))
		item2 = my_font.render("100",True,black)  #텍스트가 표시된 Surface 를 만듬
		screen.blit(coin_img, (470,450))
		screen.blit(item2,(510,450)) #텍스트를 화면에 출력
		buy_button2.draw()

		#졸업 아코
		graduation_ako_img = pygame.transform.scale(graduation_ako_img, (200,200))
		screen.blit(graduation_ako_img, (700,200))
		item3 = my_font.render("150",True,black)  #텍스트가 표시된 Surface 를 만듬
		screen.blit(coin_img, (770,450))
		screen.blit(item3,(810,450)) #텍스트를 화면에 출력
		buy_button3.draw()
  
		if back_img_button.draw():  # 뒤로가기 버튼 기능 구현 -> 메인 메뉴 페이지로
			main_menu = True
   
	elif main_menu == "option":  # 4 option 버튼 눌렀을때 페이지(디폴트 : 소리켜져있음)
		screen.blit(bg_img, (0,0))
		screen.blit(sun_img, (100,100))
		pygame.mixer.music.unpause() 
		if back_img_button.draw():
			main_menu = True
		if sound_off_button.draw(): #sound on 버튼 누르면 음악 임시멈춤
			main_menu="option_soundoff" #4.3
		if game_rule_button.draw() :
			main_menu = "game_role" #4.7

	elif main_menu == "option_soundoff": #4.3 옵션화면_소리 껐을때
		pygame.mixer.music.pause()
		if back_img_button.draw():
			main_menu = True
		if sound_on_button.draw(): #sound off 버튼 누르면 음악 다시 시작
			main_menu= "option" #4
		if game_rule_button.draw() :
			main_menu = "game_role" #4.7
		

	elif main_menu == "game_role": #게임 룰 페이지 4.7
		screen.blit(bg_img, (0,0))
		screen.blit(sun_img, (100,100))
		screen.blit(game_rule_page, (0,0))
		if back_img_button.draw():  # 뒤로가기 버튼 기능 구현 -> 옵션 페이지로
			if pygame.mixer.music. get_busy ( ) :
				main_menu = "option" #4
			elif not pygame.mixer.music. get_busy ( ) :
				main_menu = 4.3

	elif main_menu == 'easy' and not flag:
		flag = True
		world = reset_level(level)
		world.draw()


	elif main_menu == "easy" and flag:
		world.draw()
		if playing_home_button.draw():
			main_menu = True
			level = 1
   
		if game_over == 0:
			
			elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 타이머 시간을 1000으로 나누어 초단위로 표시 (default: ms 단위)
			game_font = pygame.font.Font(None, 40)
			timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255)) # 타이머 위치 지정
			screen.blit(timer, (900,10)) # 타이머 위치 지정
			if total_time - elapsed_time <= 0: 
				restart_button = Button(screen_width // 2 - 160, screen_height // 2 , restart_img)
				if restart_button.draw():
					main_menu = "main_screen"
				if exit_button.draw():
					main_menu = True

			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()  # 코인 먹을때 사운드 실행
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)  # 코인 스코어 왼쪽 상단에 가시화
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		#if player has died
		if game_over == -1:
				world_data = []
				world = reset_level(level)
				game_over = 0
				# score = 0   # 획득한 코인 리셋 안되게 이코드 주석

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= max_levels:
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				draw_text('Congratulations!! You broke the record :)', font, blue, 0, screen_height // 2)
				draw_text('(previous record:n /  current record: m)', font, white, 0, screen_height // 2+ (screen_height*0.05))
				#draw_text('an established record : nn, the current record : mm', font, white, (screen_width // 2), screen_height // 2)
				if home_button.draw():
					main_menu = True
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
     
				elif restart_button.draw():
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0
					
     
	elif main_menu == 'hard' and not flag:
		flag = True
		world = reset_hard_level(level)
		world.draw()
  
	elif main_menu == "hard" and flag:
		world.draw()
		if playing_home_button.draw():
			main_menu = True
			hard_level = 1
   
		if game_over == 0:
			elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # 타이머 시간을 1000으로 나누어 초단위로 표시 (default: ms 단위)
			game_font = pygame.font.Font(None, 40)
			timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255)) # 타이머 위치 지정
			screen.blit(timer, (900,10)) # 타이머 위치 지정
			
			if total_time - elapsed_time <= 0: 
				restart_button = Button(screen_width // 2 - 160, screen_height // 2 , restart_img)
				if restart_button.draw():
					main_menu = "main_screen"
				if exit_button.draw():
					main_menu = True
			blob_group.update()
			platform_group.update()
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				coin_fx.play()
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		#if player has died
		if game_over == -1:
				hard_world_data = []
				world = reset_hard_level(hard_level)
				game_over = 0
				# score = 0   # 획득한 코인 리셋 안되게 이코드 주석

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			hard_level += 1
			if hard_level <= hard_max_levels:
				#reset hard_level
				hard_world_data = []
				world = reset_hard_level(hard_level)
				game_over = 0
			else:
				draw_text('Congratulations!! You broke the record :)', font, blue, 0, screen_height // 2)
				draw_text('(previous record:n /  current record: m)', font, white, 0, screen_height // 2+ (screen_height*0.05))
				#draw_text('an established record : nn, the current record : mm', font, white, (screen_width // 2), screen_height // 2)
				if home_button.draw():
					main_menu = True
					hard_level = 1
					#reset hard_level
					hard_world_data = []
					world = reset_hard_level(hard_level)
					game_over = 0
     
				elif restart_button.draw():
					hard_level = 1
					#reset hard_level
					hard_world_data = []
					world = reset_hard_level(hard_level)
					game_over = 0
				

	for event in pygame.event.get():  # 어떤 이벤트가 발생하였는가?
		if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
			run = False  # 닫히는 이벤트가 발생하였으면 게임이 진행중이 아님

	pygame.display.update()  # 게임 화면을 다시 그리기 ( 반드시 계속 호출되어야 함 )

pygame.quit()  # pygame 종료