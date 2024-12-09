import pygame
import os

import EnemyAI as AI
import BombHandler as BH
import Tutorial
from enum import Enum
import codecs
import math


#from pygame.sprite import _Group

# Initialising game
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.6)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), depth=32)

pygame.display.set_caption("Bullet Blitz")

# To set a frame time

clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
LOWER_FLOOR = 500
TILE_SIZE = 64#40
TILE_TYPES = 21
bg_scroll = 0

# Define player actions variable
move_left = False
move_right = False
shoot = False

img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'img/Tile/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

#load images
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

title_image = pygame.image.load('img/Title2.png').convert_alpha()
title_img = pygame.transform.scale(title_image, (int(title_image.get_width() * 1), int(title_image.get_height() * 1)))
#store tiles in a list
water_img = pygame.image.load('img/tile/0.png').convert_alpha()

# Define bullet
bullet_img = pygame.image.load('img/icons/bullet.png').convert_alpha()

#define camera offset
camera_offsetX = 600
camera_offsetY = 600

#pick up boxes
health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'Ammo'		: ammo_box_img,
}

# Define colours
BG = (255, 201, 120)
White = (255, 255, 255)

font = pygame.font.SysFont('',30)
large_font = pygame.font.SysFont('',50)



def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

TextList = list()
generaltextFile = codecs.open("gameText.txt", "r", encoding='utf-8')
#generaltextFile = open("gameText.txt", "r")
for line in generaltextFile:
    TextList.append(line)
generaltextFile.close()

def getTextFromFile(index):
    if index == 0 or index == 1:
        returnText = TextList[index]
    else:
        textIndex = index + selectedLanguage * 9
        returnText = TextList[textIndex]
    return returnText[:-2]

Xsky = 0
Xmountain = 0
Xpine1 = 0
Xpine2 = 0

def draw_menu_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    
    increase = 2
    global Xsky, Xmountain, Xpine1, Xpine2

    Xsky += increase
    Xmountain += increase
    Xpine1 += increase
    Xpine2 += increase

    if Xsky > width * 2:
        Xsky = 0
    if Xmountain > width * (1/0.6):
        Xmountain = 0
    if Xpine1 > width * (1/0.7):
        Xpine1 = 0
    if Xpine2 > width * 1.25:
        Xpine2 = 0

    for x in range(4):
        screen.blit(sky_img, ((x * width) - Xsky * 0.5, 0))
    for x in range(4):
        screen.blit(mountain_img, ((x * width) - Xmountain * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
    for x in range(4):
        screen.blit(pine1_img, ((x * width) - Xpine1 * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
    for x in range(4):
        screen.blit(pine2_img, ((x * width) - Xpine2 * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))
    screen.blit(title_img, (50, 0))

def draw_menu():
    xPlacement = 410
    yPlacement = 480
    boxWidth = 280
    boxHeight = 43
    yIncrease = boxHeight + 15
    textOffset = 5

    for i in range(4):
        color = (0,0,0)
        if selectedMenuOption == i:
            color = (100,100,100)
            
        pygame.draw.rect(screen, color, pygame.Rect(xPlacement, yPlacement+(yIncrease*i), boxWidth, boxHeight))
        if i == 2:
            if selectedDiffuculty is not 2:
                pygame.draw.polygon(screen, color, [(xPlacement-30, yPlacement+(yIncrease*2)+boxHeight/2), 
                                                    (xPlacement-10, yPlacement+(yIncrease*2)),
                                                    (xPlacement-10, yPlacement+(yIncrease*2)+boxHeight)])
            if selectedDiffuculty is not 0:
                pygame.draw.polygon(screen, color, [(xPlacement+boxWidth+30, yPlacement+(yIncrease*2)+boxHeight/2),
                                                    (xPlacement+boxWidth+10, yPlacement+(yIncrease*2)), 
                                                    (xPlacement+boxWidth+10, yPlacement+(yIncrease*2)+boxHeight)])
        if i == 3:
            if selectedLanguage is not 1:
                pygame.draw.polygon(screen, color, [(xPlacement-30, yPlacement+(yIncrease*3)+boxHeight/2),
                                                    (xPlacement-10, yPlacement+(yIncrease*3)), 
                                                    (xPlacement-10, yPlacement+(yIncrease*3)+boxHeight)])
            if selectedLanguage is not 0:
                pygame.draw.polygon(screen, color, [(xPlacement+boxWidth+30, yPlacement+(yIncrease*3)+boxHeight/2),
                                                    (xPlacement+boxWidth+10, yPlacement+(yIncrease*3)), 
                                                    (xPlacement+boxWidth+10, yPlacement+(yIncrease*3)+boxHeight)])
    
    # draw text "start game" or "continue game"
    if gameStarted:
        draw_text(getTextFromFile(4), large_font, (255,255,255), xPlacement+textOffset, yPlacement+textOffset)
    else:
        draw_text(getTextFromFile(3), large_font, (255,255,255), xPlacement+textOffset, yPlacement+textOffset)

    # draw text tutorial
    draw_text(getTextFromFile(5), large_font, (255,255,255), xPlacement+textOffset, yPlacement+yIncrease+textOffset)

    # draw text regarding difficulty
    if selectedDiffuculty == 0:
        draw_text(getTextFromFile(6), large_font, (255,255,255), xPlacement+textOffset, yPlacement+(yIncrease*2)+textOffset)
    elif selectedDiffuculty == 1:
        draw_text(getTextFromFile(7), large_font, (255,255,255), xPlacement+textOffset, yPlacement+(yIncrease*2)+textOffset)
    elif selectedDiffuculty == 2:
        draw_text(getTextFromFile(8), large_font, (255,255,255), xPlacement+textOffset, yPlacement+(yIncrease*2)+textOffset)

    # draw text regarding language
    if selectedLanguage == 0:
        draw_text(getTextFromFile(0), large_font, (255,255,255), xPlacement+textOffset, yPlacement+(yIncrease*3)+textOffset)
    elif selectedLanguage == 1:
        draw_text(getTextFromFile(1), large_font, (255,255,255), xPlacement+textOffset, yPlacement+(yIncrease*3)+textOffset)
    

def draw_bg():
    screen.fill(BG)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - camera_offsetX * 0.5, 0))
        screen.blit(mountain_img, ((x * width) - camera_offsetX * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - camera_offsetX * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - camera_offsetX * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_terrain():
    for terrain in All_terrain:
        drawTerrainForRect(terrain, True)

        #pygame.draw.rect(screen, White, pygame.Rect((terrain.x-camera_offsetX), (terrain.y-camera_offsetY), terrain.width, terrain.height))
    #pygame.draw.rect(screen, White, ground_platform)
    #pygame.draw.rect(screen, (0,0,255), upper_platform)
    #pygame.draw.rect(screen, (0,255,0), second_platform)



def drawTerrainForRect(rect, withEdge):
    height = img_list[0].get_height()
    width = img_list[0].get_width()
    amount_height = math.ceil(rect.height / height)
    amount_width = math.ceil(rect.width / width)
        
    StartX = rect.x
    StartY = rect.y
    if withEdge:
        for x in range(1, amount_width-1):
            screen.blit(img_list[0], (StartX + x*width - camera_offsetX, 
                                      StartY - camera_offsetY))
            for y in range(1, amount_height):
                screen.blit(img_list[4], (StartX + x*width - camera_offsetX, 
                                          StartY + y*height - camera_offsetY))
        screen.blit(img_list[1], (StartX - camera_offsetX, 
                                  StartY - camera_offsetY))
        screen.blit(img_list[2], (StartX + (amount_width-1)*width - camera_offsetX, 
                                  StartY - camera_offsetY))
        for y in range(1, amount_height):
            screen.blit(img_list[3], (StartX - camera_offsetX, 
                                      StartY + y * height - camera_offsetY))
            screen.blit(img_list[5], (StartX + (amount_width-1)*width - camera_offsetX, 
                                      StartY + y * height - camera_offsetY))
    else:
        for x in range(amount_width):
            screen.blit(img_list[0], (StartX + x*width - camera_offsetX, 
                                      StartY - camera_offsetY))
            for y in range(1, amount_height):
                screen.blit(img_list[4], (StartX + x*width - camera_offsetX, 
                                          StartY + y*height - camera_offsetY))

transitionTimer = 0
def black_Transition():
    global transitionTimer, currentGameState, nextGameState, camera_offsetX, camera_offsetY
    transitionTimerMax = 120
    middlePotionHalf = 2

    transitionTimer += 1

    blackBackground = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    blackBackground.fill((0,0,0))
    alpha = 255
    firstHalf = (transitionTimerMax/2-middlePotionHalf)
    secondHalf = (transitionTimerMax/2+middlePotionHalf)
    if transitionTimer < firstHalf:
        alpha = (transitionTimer/firstHalf)*255
    elif transitionTimer > secondHalf:
        if nextGameState == State.MENU:
            draw_menu_bg()
            draw_menu()
        elif  nextGameState == State.TUTORIAL:
            camera_offsetX = 0
            camera_offsetY = 0
            draw_bg()
            TutorialPlayer.updateTutorialTerrain()
        else:
            transitionTimer = transitionTimerMax+1
        alpha = ((transitionTimerMax-transitionTimer)/secondHalf)*255
    else:
        screen.fill((0,0,0))
    blackBackground.set_alpha(alpha)
    screen.blit(blackBackground, (0,0))

    if transitionTimer > transitionTimerMax:
        currentGameState = nextGameState
        transitionTimer = 0



class Soldier(pygame.sprite.Sprite):
     def __init__(self , char_type, x, y , scale, speed, ammo):  # Creating instance for the movement of characters of sprites 
         self.alive = True
         self.char_type = char_type 
         self.speed = speed
         self.ammo = ammo
         self.start_ammo = ammo
         self.shoot_cooldown = 0
         self.health = 100
         self.max_health = self.health
         self.direction = 1
         self.vel_y = 0
         self.jump = False
         self.in_air = True
         self.flip = False
         self.animation_list = []
         self.frame_index = 0
         self.action = 0
         self.update_time = pygame.time.get_ticks()


         animation_types = ['Idle', 'Run', 'Jump', 'Death']
         for animation in animation_types:
            temp_list = []
            #Get a list of all the files in the directory
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        

         # To create a boundary tp contol the environemnt , 
         # where the image is drawn and self controls as instance 
         self.image = self.animation_list[self.action][self.frame_index]
         self.rect = img.get_rect()

         # Aligning to the cordinates
         self.rect.center = (x ,y)
         
         # initialize and sets the sensors for the characters
         self.left_sensor = pygame.Rect(x,y, 10, self.rect.height-8)
         self.left_sensor.center = self.rect.midleft
         self.right_sensor = pygame.Rect(x,y, 10, self.rect.height-8)
         self.right_sensor.center = (self.rect.right-20, self.rect.centery)
         self.bottom_sensor = pygame.Rect(self.rect.left+5, self.rect.bottom-5, self.rect.width-30, 10)

         # These instances are like blue prints,
         #  we can create as many as we want for the various actions

     def update(self):
         self.update_animation()
         self.check_alive()
         if self.shoot_cooldown > 0:
             self.shoot_cooldown -= 1

     def movement(self, move_left, move_right): # Create variables for the movements
         self.movementBase(move_left, move_right, All_terrain)

     def movementBase(self, move_left, move_right, terrainList): # Create variables for the movements
         #set movement variables
         dx = 0
         dy = 0
        
         # will move the character left or right
         # if collision with terrain, will stop movement in the corresponding direction
         if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
            if pygame.Rect.collidelist(self.left_sensor, terrainList) > -1:
                dx = 0
         if move_right:
             self.flip = False
             self.direction = 1
             dx = self.speed
             if pygame.Rect.collidelist(self.right_sensor, terrainList) > -1:
                dx = 0
        
         # checks if the player have collision downwards and set the vairable "self.in_air" accorddingly
         terrain_index = pygame.Rect.collidelist(self.bottom_sensor, terrainList)
         if terrain_index > -1:
            terrain = terrainList[terrain_index]
            dy = terrain.top - self.rect.bottom
            self.in_air = False
            self.vel_y = 0
         else: 
            self.in_air = True

         # Jump
         if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True
        
        # Gravity
         if self.in_air:
            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y
            dy += self.vel_y

         #if self.rect.bottom + dy > LOWER_FLOOR:
         #   dy = LOWER_FLOOR - self.rect.bottom
         #   self.in_air = False

        # Update rect position   
         self.rect.x += dx
         self.rect.y += dy
         
         # updates the x and y for the sensors
         self.left_sensor.x += dx
         self.left_sensor.y += dy
         self.right_sensor.x += dx
         self.right_sensor.y += dy
         self.bottom_sensor.x += dx
         self.bottom_sensor.y += dy

         if self.char_type == 'player' or self.char_type == 'player2':
            global camera_offsetX, camera_offsetY
            camera_offsetX += dx
            camera_offsetY += dy

     def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            gunSound.play()
            self.shoot_cooldown = 20 # Reload number, lower number faster speed
            bullet = Bullet(self.rect.centerx + (0.6* self.rect.size[0]* self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
    
     def update_animation(self):
        #as long as it fast enough it can update animation prefectly.
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #when animation ran out then reset it
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index =0
     
     
     def update_action(self, new_action):
		#check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
			#update settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
     def check_alive(self):
         if self.health <= 0:
             self.health = 0
             self.speed = 0
             self.alive = False
             self.update_action(3)

     def draw(self): # Create methods to reduce the calling
         
          #Blit function copies image from the surface to the screen 
          # using Object Oriented Programmingm

          # tests - used to visualize the sensor of the soldiers (inlc. the player)
         #pygame.draw.rect(screen, (0,0,0), pygame.Rect((self.right_sensor.x-camera_offsetX), (self.right_sensor.y-camera_offsetY), self.right_sensor.width, self.right_sensor.height))
         #pygame.draw.rect(screen, (0,0,100), pygame.Rect((self.left_sensor.x-camera_offsetX), (self.left_sensor.y-camera_offsetY), self.left_sensor.width, self.left_sensor.height))
         #pygame.draw.rect(screen, (0,0,200), pygame.Rect((self.bottom_sensor.x-camera_offsetX), (self.bottom_sensor.y-camera_offsetY), self.bottom_sensor.width, self.bottom_sensor.height))
         #pygame.draw.rect(screen, (0,0,0), self.right_sensor)
         #pygame.draw.rect(screen, (0,0,100), self.left_sensor)
         #pygame.draw.rect(screen, (0,0,200), self.bottom_sensor)
         
         screen.blit(pygame.transform.flip(self.image, self.flip, False),
                         pygame.Rect((self.rect.x-camera_offsetX), (self.rect.y-camera_offsetY), self.rect.width, self.rect.height)) 
         #screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) 
         


class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
        # Check  collision 
		
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 15
			self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # Bullet move forward
        self.rect.x += (self.direction * self.speed)
        # If bullet disppaer from screen then kill it 
        if self.rect.right < (0+camera_offsetX) or self.rect.left > (SCREEN_WIDTH+camera_offsetX):
            self.kill()
        # Collision check
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        #get collision of all enemies and pick out the first in the list
        listOfHitEnemies = EnemyHandler.checkSpriteCollision(bullet_group)
        if listOfHitEnemies: # check if non empty list
            hitEnemy = listOfHitEnemies[0]
            if hitEnemy.alive:
                hitEnemy.health -= 20
                self.kill()
        #if pygame.sprite.spritecollide(enemy, bullet_group, False):
        #    if enemy.alive:
        #        enemy.health -= 20
        #        self.kill()

    #def draw(self, surface):
    #    surface.blit(self.image, pygame.Rect((self.rect.x-camera_offsetX), (self.rect.y-camera_offsetY), self.rect.width, self.rect.height)) 
        
class State(Enum):
    MENU = 0
    GAME = 1
    TUTORIAL = 2
    TRANSITION = 3

upper_platform = pygame.Rect(1600, 400, 192, SCREEN_HEIGHT-400)
ground_platform = pygame.Rect((-100, LOWER_FLOOR), (SCREEN_WIDTH*3, SCREEN_HEIGHT-400))
second_platform = pygame.Rect((1300, 450), (640, SCREEN_HEIGHT-400))
right_wall = pygame.Rect((0, 200), (576, SCREEN_HEIGHT-400))

All_terrain = [upper_platform, second_platform, right_wall, ground_platform]

# Create a group for bullte 
bullet_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()


item_box = ItemBox('Health', 800, 435)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 700, 435)
item_box_group.add(item_box)




#Creating instances with the given x,y and size co ordinates
player = Soldier('player2', 1100, 450, 3, 5, 20)
enemy = Soldier('enemy2', 1050, 250, 3, 5, 20)
 
# player2 = Soldier(400, 200, 3) #since we have created instances, just need to specify the co ordinates
#x = 200        
#y = 200
#scale = 3 # Try to avoid a float

bombHandler = BH.ChickenBombHandler()
EnemyHandler = AI.EnemyHandler()
TutorialPlayer = Tutorial.Tutorial(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

bombHandler.setup(player, screen, EnemyHandler, All_terrain)

EnemyHandler.setup(player, screen, All_terrain)
EnemyHandler.addEnemyToList(enemy)

background_size = 1376 * 2 

pygame.mixer.init()
gunSound = pygame.mixer.Sound("click.wav")

#Event handler
running = True
gameStarted = False

# 0 = play game
# 1 = play tutorial
# 2 = select difficulty
# 3 = select language
selectedMenuOption = 0
maxMenuOptionsIndex = 3

# 0 = easy
# 1 = normal
# 2 = hard
selectedDiffuculty = 1
maxDifficultyIndex = 2

# 0 = english
# 1 = swedish
selectedLanguage = 0
maxLanguageIndex = 1

currentGameState = State.MENU
nextGameState = State.MENU

while running:

    if currentGameState == State.MENU:
        #tick camera offset to have scrolling background
        clock.tick(FPS)

        draw_menu_bg()
        draw_menu()

        startGame = False
        startTutorial = False

        for event in pygame.event.get():

            # To quit game
            if event.type == pygame.QUIT:
                running = False

            # Event handler for Keyboard controls  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if selectedMenuOption == 2:
                        selectedDiffuculty += 1
                    if selectedMenuOption == 3:
                        selectedLanguage += 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if selectedMenuOption == 2:
                        selectedDiffuculty -= 1
                    if selectedMenuOption == 3:
                        selectedLanguage -= 1
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    selectedMenuOption -= 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    selectedMenuOption += 1
                if event.key == pygame.K_SPACE  or event.key == pygame.K_RETURN:
                    if selectedMenuOption == 0:
                        startGame = True
                    if selectedMenuOption == 1:
                        startTutorial = True
        
        if (selectedMenuOption > maxMenuOptionsIndex):
            selectedMenuOption = maxMenuOptionsIndex
        if (selectedMenuOption < 0):
            selectedMenuOption = 0

        if (selectedDiffuculty > maxDifficultyIndex):
            selectedDiffuculty = maxDifficultyIndex
        if (selectedDiffuculty < 0):
            selectedDiffuculty = 0

        if (selectedLanguage > maxLanguageIndex):
            selectedLanguage = maxLanguageIndex
        if (selectedLanguage < 0):
            selectedLanguage = 0

        if startGame:
            nextGameState = State.GAME
            currentGameState = State.TRANSITION
            gameStarted = True

        if startTutorial:
            nextGameState = State.TUTORIAL
            currentGameState = State.TRANSITION
            TutorialCharacter = Soldier('player2', SCREEN_WIDTH/2, -100, 3, 5, 20)
            TutorialPlayer.startTutorial(TutorialCharacter, camera_offsetX, camera_offsetY)

        pygame.display.update()
    elif currentGameState == State.GAME:
        if(False): #disables the camera offset
            camera_offsetX = 0
        camera_offsetY = 0

        clock.tick(FPS)
        draw_bg()
        draw_terrain()
        draw_text(f'{getTextFromFile(9)}:{player.ammo}',font,White, 15, 20)
        draw_text(f'{getTextFromFile(10)}:{player.health}',font,White, 15, 50)

        player.update()
        player.draw() 
        
        EnemyHandler.update()

        bombHandler.update(camera_offsetX, camera_offsetY)
        
        bullet_group.update()
        # have to blit and not call ".draw" of group as camera offset doesn't work.
        for spr in bullet_group.sprites():
            bullet_group.spritedict[spr] = screen.blit(spr.image, pygame.Rect((spr.rect.x-camera_offsetX), (spr.rect.y-camera_offsetY), spr.rect.width, spr.rect.height))

        item_box_group.update()
        # have to blit and not call ".draw" of group as camera offset doesn't work.
        for spr in item_box_group.sprites():
            item_box_group.spritedict[spr] = screen.blit(spr.image, pygame.Rect((spr.rect.x-camera_offsetX), (spr.rect.y-camera_offsetY), spr.rect.width, spr.rect.height))
        #item_box_group.draw(screen)
        



        if player.alive:
            if shoot:
                player.shoot()
            if player.in_air:
                player.update_action(2)#2: jump
            elif move_left or move_right:
                player.update_action(1)#1: run
            else:
                player.update_action(0)#0: idle
            player.movement(move_left, move_right)


        
        for event in pygame.event.get():

            # To quit game
            if event.type == pygame.QUIT:
                running = False

            # Event handler for Keyboard controls  
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # keyboard button a is set for the left movemen
                    nextGameState = State.MENU
                    currentGameState = State.TRANSITION
                if event.key == pygame.K_a: # keyboard button a is set for the left movemen
                    move_left = True    
                if event.key == pygame.K_d: # keyboard button b is set for the right movemen
                    move_right  = True 
                if event.key == pygame.K_SPACE: # keyboard button SPACE is set for shooting
                    shoot  = True    
                if event.key == pygame.K_w and player.alive:
                    player.jump = True
                if event.key == pygame.K_b:
                    bombHandler.spawn_chicken_bomb(player)

            # Set a release mode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False    
                if event.key == pygame.K_d: 
                    move_right = False    
                if event.key == pygame.K_SPACE: 
                    shoot = False  
                if event.key == pygame.K_ESCAPE : # set a button for esc button
                    run = False 
    
        # To update and call the image according to the rectangle  from the blit
        pygame.display.update()
    elif currentGameState == State.TUTORIAL:
        clock.tick(FPS)

        if(True): #disables the camera offset
            camera_offsetX = 0
            camera_offsetY = 0
        
        draw_bg()

        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                running = False

        if running:
            TutorialPlayer.updateTutorial(eventList, selectedLanguage)

        if TutorialPlayer.TutorialEnd:
            (camera_offsetX, camera_offsetY) = TutorialPlayer.resetTutorial()

            nextGameState = State.MENU
            currentGameState = State.TRANSITION

        pygame.display.update()
    elif currentGameState == State.TRANSITION:
        clock.tick(FPS)

        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                running = False

        if running:
            black_Transition()
        pygame.display.update()
    else:
        running = False
    

pygame.quit()







