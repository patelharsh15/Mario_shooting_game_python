import pygame
import os
import codecs
import math

class Tutorial():
    def __init__(self, mainScreen, screenWidth, screenHeight):
        self.screen = mainScreen
        self.WIDTH = screenWidth
        self.HEIGHT = screenHeight
        self.selectedLanguage = 0

        self.platformEdge = 14
        self.terrainList = list()
        floorLevel = screenHeight - (64 * 1)
        floor = pygame.Rect((0, floorLevel), (self.WIDTH, screenHeight-floorLevel))
        rightPlatform = pygame.Rect((64*self.platformEdge, floorLevel-64), (64*self.platformEdge, screenHeight-floorLevel))
        leftWall = pygame.Rect((-10, 0), (10, screenHeight))
        rightWall = pygame.Rect((self.WIDTH, 0), (10, screenHeight))
        test = pygame.Rect((200, 200), (256, 256))
        self.terrainList.append(floor)
        self.terrainList.append(rightPlatform)
        self.terrainList.append(test)
        self.terrainList.append(leftWall)
        self.terrainList.append(rightWall)

        # variables for controlling the tutorials
        # will change during the run and will be reset at the end
        self.TutorialPaused = False
        self.TutorialEnd = False
        self.selectedMenuOption = 0
        self.TuturialInternalClock = 0
        self.TuturialInternalClockCount = True
        self.controlsDisabled = True
        self.jumpDisabled = True
        
        self.playerMoveRight = False
        self.playerMoveLeft = False

        self.playerHaveMovedRight = False
        self.playerHaveMovedLeft = False
        self.playerHaveReachedPaltform = False
        self.counter = 0

        self.large_font = pygame.font.SysFont('',50)
        self.extreme_font = pygame.font.SysFont('',100)

        self.keyBoardSpriteList = list()
        scale = 1
        for i in range(4):
            img = pygame.image.load(f'img/keyboard/Keyboard{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.keyBoardSpriteList.append(img)

        self.TerrainSpriteList = list()
        scale = 2
        for i in range(9):
            img = pygame.image.load(f'img/tile/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.TerrainSpriteList.append(img)
        
        self.player = None

        self.colorLightGreen = (208,240,192)
        self.firstLineY = 200
        self.secondLineY = 250

        self.TextList = list()
        tutorialTextFile = codecs.open("TutorialText.txt", "r", encoding='utf-8')
        for line in tutorialTextFile:
            self.TextList.append(line)
        tutorialTextFile.close()

        # saved variables that is changed from the main game but will be restored at the end

    def getTextFromFile(self, index):
        textIndex = index + self.selectedLanguage * 25
        returnText = self.TextList[textIndex]
        return returnText[:-2]


    def draw_text(self, text, font, text_color, x, y, centerScreen, outLine):
        img = font.render(text, True, text_color)
        img_rect = (x,y)
        if centerScreen:
            img_rect = img.get_rect(center=(self.WIDTH/2, y))
        if outLine:
            for (offsetX, offsetY) in [(0,2),(0,-2),(2,0),(-2,0),(1,1),(-1,-1),(1,-1),(-1,1)]:
                outlineIMG = font.render(text, True, (0,0,0))
                outLine_rect = img.get_rect(center=(self.WIDTH/2+offsetX, y+offsetY))
                self.screen.blit(outlineIMG, outLine_rect)
        self.screen.blit(img, img_rect)

    def resetTutorial(self):
        self.selectedMenuOption = 0
        self.TutorialPaused = False
        self.TutorialEnd = False
        self.TuturialInternalClock = 0
        self.TuturialInternalClockCount = True
        self.controlsDisabled = True
        self.jumpDisabled = True
        
        self.playerMoveRight = False
        self.playerMoveLeft = False
        self.playerHaveMovedRight = False
        self.playerHaveMovedLeft = False
        self.playerHaveReachedPaltform = False
        
        # reseting the camera offset
        return (self.storedOffsetX, self.storedOffsetY)

    def startTutorial(self, player, currentOffsetX, currentoffsetY):
        self.player = player
        self.storedOffsetX = currentOffsetX
        self.storedOffsetY = currentoffsetY

    def updateTutorial(self, eventList, language):
        #update varaibles from the main file
        self.selectedLanguage = language

        #updates the terrain for the tutorial
        self.updateTutorialTerrain()
        
        #check if the tutorial is paused
        if self.TutorialPaused:
            self.updateTutorialMenu()

            for event in eventList:
                # event Type "QUIT" is handled before enetering update in tutorial
                # Event handler for Keyboard controls  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.TutorialPaused = False
                    if event.key == pygame.K_RETURN:
                        if self.selectedMenuOption == 0:
                            self.TutorialPaused = False
                        elif self.selectedMenuOption == 1:
                            self.TutorialEnd = True
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.selectedMenuOption -= 1
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.selectedMenuOption += 1
            
            if (self.selectedMenuOption > 1):
                self.selectedMenuOption = 1
            if (self.selectedMenuOption < 0):
                self.selectedMenuOption = 0

        else:
            if self.TuturialInternalClockCount:
                self.TuturialInternalClock += 1

            if self.TuturialInternalClock < 1250:
                self.tutorialFirstSection()

            if self.TuturialInternalClock == 1260:
                self.controlsDisabled = False
                self.TuturialInternalClockCount = False

            if self.TuturialInternalClock > 1300 and self.TuturialInternalClock < 2150:
                self.tutorialSecondSection()

            if self.TuturialInternalClock == 2160:
                self.controlsDisabled = False
                self.jumpDisabled = False
                self.TuturialInternalClockCount = False

            if self.TuturialInternalClock > 2200 and self.TuturialInternalClock < 3000:
                self.tutorialSecondSection()
                if self.TuturialInternalClock > 2600:
                    self.TutorialEnd = True

            if(self.TuturialInternalClock > 600):
                self.player.draw()
                self.player.update()

                if self.player.alive:
                    #if shoot:
                    #    self.player.shoot()
                    if self.player.in_air:
                        self.player.update_action(2)#2: jump
                    elif self.playerMoveLeft or self.playerMoveRight:
                        self.player.update_action(1)#1: run
                    else:
                        self.player.update_action(0)#0: idle
                    self.player.movementBase(self.playerMoveLeft, self.playerMoveRight, self.terrainList)

            for event in eventList:
                # event Type "QUIT" is handled before enetering update in tutorial
                # Event handler for Keyboard controls  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.TutorialPaused = True
                    if not self.controlsDisabled:
                        if event.key == pygame.K_a: # keyboard button a is set for the left movement
                            self.playerMoveLeft = True
                        if event.key == pygame.K_d: # keyboard button b is set for the right movement
                            self.playerMoveRight  = True
                        if not self.jumpDisabled:
                            if event.key == pygame.K_w and self.player.alive:
                                self.player.jump = True
                
                if event.type == pygame.KEYUP:
                    if not self.controlsDisabled:
                        if event.key == pygame.K_a:
                            self.playerMoveLeft = False
                            self.counter = 0
                        if event.key == pygame.K_d: 
                            self.playerMoveRight = False
                            self.counter = 0

            if not self.controlsDisabled:
                if self.playerMoveRight:
                    self.counter += 1
                    if self.counter > 20:
                        self.playerHaveMovedRight = True
                if self.playerMoveLeft:
                    self.counter += 1
                    if self.counter > 20:
                        self.playerHaveMovedLeft = True
                if self.player.rect.centerx > self.WIDTH - 200:
                    self.playerHaveReachedPaltform = True

            if self.playerHaveMovedRight and self.playerHaveMovedLeft and self.TuturialInternalClock < 1270:
                self.controlsDisabled = True
                self.TuturialInternalClockCount = True

                self.playerMoveLeft = False
                self.playerMoveRight = False

            if self.playerHaveReachedPaltform and self.TuturialInternalClock < 2170:
                self.controlsDisabled = True
                self.TuturialInternalClockCount = True
                self.jumpDisabled = True

                self.playerMoveLeft = False
                self.playerMoveRight = False
            


    def updateTutorialTerrain(self):
        self.drawTerrainForRect(self.terrainList[0], False)
        self.drawTerrainForRect(self.terrainList[1], True)

    def drawTerrainForRect(self, rect, withEdge): 
        height = self.TerrainSpriteList[0].get_height()
        width = self.TerrainSpriteList[0].get_width()
        amount_height = math.ceil(rect.height / height)
        amount_width = math.ceil(rect.width / width)
        
        StartX = rect.x
        StartY = rect.y
        if withEdge:
            for x in range(1, amount_width-1):
                self.screen.blit(self.TerrainSpriteList[0], (StartX + x*width, StartY))
                for y in range(1, amount_height):
                    self.screen.blit(self.TerrainSpriteList[4], (StartX + x*width, StartY + y*height))
            self.screen.blit(self.TerrainSpriteList[1], (StartX, StartY))
            self.screen.blit(self.TerrainSpriteList[2], (StartX + (amount_width-1)*width, StartY))
            for y in range(1, amount_height):
                self.screen.blit(self.TerrainSpriteList[3], (StartX, StartY + y * height))
                self.screen.blit(self.TerrainSpriteList[5], (StartX + (amount_width-1)*width, StartY + y * height))
        else:
            for x in range(amount_width):
                self.screen.blit(self.TerrainSpriteList[0], (StartX + x*width, StartY))
                for y in range(1, amount_height):
                    self.screen.blit(self.TerrainSpriteList[4], (StartX + x*width, StartY + y*height))




    def updateTutorialMenu(self):
        backgroundDim = pygame.Surface((self.WIDTH, self.HEIGHT))
        backgroundDim.set_alpha(100)
        backgroundDim.fill((0,0,0))
        self.screen.blit(backgroundDim, (0,0))

        self.draw_text(self.getTextFromFile(1), self.extreme_font, (220,220,220), 240, 200, True, False)

        xPlacement = 370
        yPlacement = 480
        boxWidth = 380
        textOffset = 40 - 30 * self.selectedLanguage

        for i in range(2):
            color = (0,0,0)
            if self.selectedMenuOption == i:
                color = (100,100,100)
                
            pygame.draw.rect(self.screen, color, pygame.Rect(xPlacement, yPlacement+(70*i), boxWidth, 50))

        self.draw_text(self.getTextFromFile(2), self.large_font, (255,255,255), xPlacement+textOffset, 490, False, False)
        self.draw_text(self.getTextFromFile(3), self.large_font, (255,255,255), xPlacement+textOffset, 560, False, False)


    def tutorialFirstSection(self):
        TimebetweenText = 20
        DurationOfText = 270
        TimeForSecondRow = 90

        StartTime = 0
        SecondText = 0
        EndTime = 0

        for index in (5,7,9,11,13):
            StartTime = EndTime + TimebetweenText
            SecondText = StartTime + TimeForSecondRow
            EndTime = StartTime + DurationOfText

            if(self.TuturialInternalClock > StartTime and 
                self.TuturialInternalClock < EndTime):
                self.draw_text(self.getTextFromFile(index), self.large_font, (220,220,220), 500, self.firstLineY, True, True)
                if(self.TuturialInternalClock > SecondText):
                    self.draw_text(self.getTextFromFile(index+1), self.large_font, (220,220,220), 500, self.secondLineY, True, True)

        TimeToMove = DurationOfText*3 + 170
        
        self.playerMoveRight = False
        self.playerMoveLeft = False

        keyboardX = self.WIDTH/2 - 400
        keyboardY = self.secondLineY + 50
        if(self.TuturialInternalClock > TimeToMove  and self.TuturialInternalClock < TimeToMove+40):
            self.screen.blit(self.keyBoardSpriteList[1], (keyboardX, keyboardY))
            self.playerMoveRight = True
        elif(self.TuturialInternalClock > TimeToMove+60  and self.TuturialInternalClock < TimeToMove+140):
            self.screen.blit(self.keyBoardSpriteList[2], (keyboardX, keyboardY))
            self.playerMoveLeft = True
        elif(self.TuturialInternalClock > TimeToMove+160  and self.TuturialInternalClock < TimeToMove+200):
            self.screen.blit(self.keyBoardSpriteList[1], (keyboardX, keyboardY))
            self.playerMoveRight = True
        elif(self.TuturialInternalClock > TimeToMove-20  and self.TuturialInternalClock < TimeToMove+220):
            self.screen.blit(self.keyBoardSpriteList[0], (keyboardX, keyboardY))
        

        
    def tutorialSecondSection(self):
        TimebetweenText = 20
        DurationOfText = 270
        TimeForSecondRow = 90

        StartTime = 0
        SecondText = 0
        EndTime = 1300

        for index in (15,17,19,21,23):
            StartTime = EndTime + TimebetweenText
            SecondText = StartTime + TimeForSecondRow
            EndTime = StartTime + DurationOfText

            if(self.TuturialInternalClock > StartTime and 
                self.TuturialInternalClock < EndTime):
                self.draw_text(self.getTextFromFile(index), self.large_font, (220,220,220), 500, self.firstLineY, True, True)
                if(self.TuturialInternalClock > SecondText):
                    self.draw_text(self.getTextFromFile(index+1), self.large_font, (220,220,220), 500, self.secondLineY, True, True)
                    
        self.playerMoveRight = False
        self.playerMoveLeft = False

        #reset position to middle of screen
        
        if ((self.TuturialInternalClock > 1305 and self.TuturialInternalClock < 1400) or 
            (self.TuturialInternalClock > 2000 and self.TuturialInternalClock < 2100)):
            if self.player.rect.centerx < self.WIDTH/2:
                self.playerMoveRight = True
            if self.player.rect.centerx > self.WIDTH/2:
                self.playerMoveLeft = True
        
        keyboardX = self.WIDTH/2 - 400
        keyboardY = self.secondLineY + 50

        jumpTime = 1650
        if(self.TuturialInternalClock == jumpTime or self.TuturialInternalClock == jumpTime+100 ):
            self.player.jump = True

        if(self.TuturialInternalClock > jumpTime and self.TuturialInternalClock < jumpTime+20):
            self.screen.blit(self.keyBoardSpriteList[3], (keyboardX, keyboardY))
        elif(self.TuturialInternalClock > jumpTime+100 and self.TuturialInternalClock < jumpTime+120):
            self.screen.blit(self.keyBoardSpriteList[3], (keyboardX, keyboardY))
        elif(self.TuturialInternalClock > jumpTime-20  and self.TuturialInternalClock < jumpTime+160):
            self.screen.blit(self.keyBoardSpriteList[0], (keyboardX, keyboardY))

        
        platformJump = 1870
        if(self.TuturialInternalClock == platformJump):
            self.player.jump = True
        if(self.TuturialInternalClock > platformJump-45 and self.TuturialInternalClock < platformJump+30):
            self.playerMoveRight = True

    def tutorialThirdSection(self):
        TimebetweenText = 20
        DurationOfText = 270
        TimeForSecondRow = 90

        StartTime = 0
        SecondText = 0
        EndTime = 2200

        for index in (25,27):
            StartTime = EndTime + TimebetweenText
            SecondText = StartTime + TimeForSecondRow
            EndTime = StartTime + DurationOfText

            if(self.TuturialInternalClock > StartTime and 
                self.TuturialInternalClock < EndTime):
                self.draw_text(self.getTextFromFile(index), self.large_font, (220,220,220), 500, self.firstLineY, True, True)
                if(self.TuturialInternalClock > SecondText):
                    self.draw_text(self.getTextFromFile(index+1), self.large_font, (220,220,220), 500, self.secondLineY, True, True)