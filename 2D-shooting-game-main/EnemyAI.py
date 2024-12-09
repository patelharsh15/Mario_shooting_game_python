import pygame
import os
from enum import Enum

class EnemyHandler():

    def __init__(self):

        self.listOfEnemies = []
        self.EnemyVisionLenght = 120 # will be doubled when used in function

        self.player = None
        self.screen = None
        self.terrain = None

    #import values from main
    def setup(self, playerChar, mainScreen, GameTerrain):
        self.player = playerChar
        self.screen = mainScreen
        self.terrain = GameTerrain

    #add enemy and information regarding their current state
    def addEnemyToList(self, enemy):
        InternalTimer = 0
        previousState = self.State.MOVE_LEFT
        # [current State, previous State, timer for current state]
        EnemyInfo = [self.State.STAY, previousState, InternalTimer] 

        self.listOfEnemies.append([enemy, EnemyInfo])

    #update everything
    def update(self):
        self.updateEnemiesPath()

    #update enemies
    def updateEnemiesPath(self):
        for enemyStack in self.listOfEnemies:
            #Decompile 
            enemy = enemyStack[0]
            enemyInfo = enemyStack[1]

            enemy.update()
            enemy.draw()

            #default values of moving
            move_left = False
            move_right = False

            if enemy.alive:
                
                
                # ---------------------- check player --------------------------------------
                # --------------------------------------------------------------------------
                # looking either right or left depending on "enemy.direction"
                hitRect = pygame.Rect(enemy.rect.centerx+(self.EnemyVisionLenght*(enemy.direction-1)+20*enemy.direction), enemy.rect.centery, self.EnemyVisionLenght*2-20, 1)
                
                if pygame.Rect.colliderect(self.player.rect, hitRect) and self.player.alive:
                    enemy.shoot()

                # test - visualizing hitRect
                #pygame.draw.rect(self.screen, (0, 0, 0), hitRect)


                # ---------------------- check movement ------------------------------------
                # --------------------------------------------------------------------------
                if enemyInfo[0] == self.State.STAY:
                    enemyInfo[2] += 1 # update timer
                    
                    #reset Timer
                    if enemyInfo[2] >= self.getStateTimerValues(self.State.STAY):
                        self.updateState(enemyInfo)

                elif enemyInfo[0] == self.State.MOVE_LEFT:
                    enemyInfo[2] += 1 # update timer
                    move_left = True
                    
                    #reset Timer
                    if enemyInfo[2] >= self.getStateTimerValues(self.State.MOVE_LEFT):
                        self.updateState(enemyInfo)

                elif enemyInfo[0] == self.State.MOVE_RIGHT:
                    enemyInfo[2] += 1 # update timer
                    move_right = True
                    
                    #reset Timer
                    if enemyInfo[2] >= self.getStateTimerValues(self.State.MOVE_RIGHT):
                        self.updateState(enemyInfo)

                # ---------------------- check low ground (for jumps) ----------------------
                # --------------------------------------------------------------------------
                scan_beam_length = 40
                scan_bottom = pygame.Rect(enemy.rect.centerx+(scan_beam_length*(enemy.direction-1)), enemy.rect.centery+45, scan_beam_length*2, 1)
                scan_top = pygame.Rect(enemy.rect.centerx+(scan_beam_length*(enemy.direction-1)), enemy.rect.centery-20, scan_beam_length*2, 1)

                if pygame.Rect.collidelist(scan_bottom, self.terrain) > -1 and not pygame.Rect.collidelist(scan_top, self.terrain) > -1 and not enemy.in_air:
                    enemy.jump = True

                # test - visualizing scan beams
                #pygame.draw.rect(self.screen, (200, 0, 0), scan_bottom)
                #pygame.draw.rect(self.screen, (200, 0, 0), scan_top)

                # ---------------------- update animations ---------------------------------
                # --------------------------------------------------------------------------
                if enemy.in_air:
                    enemy.update_action(2)#2: jump
                elif move_left or move_right:
                    enemy.update_action(1)#1: run
                else:
                    enemy.update_action(0)#0: idle

            #update enemy movement
            enemy.movement(move_left, move_right)


            
        
    #States of the enemy
    class State(Enum):
        STAY = 1
        MOVE_RIGHT = 2
        MOVE_LEFT = 3
        #SHOOTING = 4

    #time values for the different states
    def getStateTimerValues(self, state):
        if state == self.State.STAY:
            return 90
        elif state == self.State.MOVE_LEFT or state == self.State.MOVE_RIGHT:
            return 90
        else:
            return 0
    
    # will reset the timer and update the current and previous state
    def updateState(self, enemyInfo):

        enemyInfo[2] = 0 # reset Timer
        currentState = enemyInfo[0]

        #set new current state based on the current and previous state
        if currentState == self.State.STAY:
            #check previous state and set new current
            if enemyInfo[1] == self.State.MOVE_LEFT:
                enemyInfo[0] = self.State.MOVE_RIGHT
            else:
                enemyInfo[0] = self.State.MOVE_LEFT
        
        elif currentState == self.State.MOVE_LEFT:
            enemyInfo[0] = self.State.STAY
        elif currentState == self.State.MOVE_RIGHT:
            enemyInfo[0] = self.State.STAY
        else:
            enemyInfo[0] = self.State.STAY
        
        enemyInfo[1] = currentState # set previous state to current

    # checks collision of enemies with sprites 
    def checkSpriteCollision(self, spriteGroup):
        temp_list = []
        for enemyStack in self.listOfEnemies:
            enemy = enemyStack[0]
            if enemy.alive and pygame.sprite.spritecollide(enemy, spriteGroup, False):
                temp_list.append(enemy)
        return temp_list
    
    # checks collision of enemies with rect 
    def checkRectCollision(self, collisionRect):
        temp_list = []
        for enemyStack in self.listOfEnemies:
            enemy = enemyStack[0]
            if enemy.alive and pygame.Rect.colliderect(enemy.rect, collisionRect):
                temp_list.append(enemy)
        return temp_list