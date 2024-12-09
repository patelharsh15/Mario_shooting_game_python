import pygame
import math

# different from main to have a better curve of the throw
GRAVITY = 0.4


class ChickenBombHandler():
    def __init__(self):
        #set the max and current amount of chicken bombs.
        self.max_amount = 10
        self.current_amount = 0
        #sets the time limiit of the bomb until explosion and how long the exposion will last
        self.time_limit = 80
        self.explo_time = 20

        # list of all active bombs and explosions
        self.active_bombs = list()
        self.detonated_bombs = list()

        # setup all sprites used for the chicken and the explosion.
        # 1-2 = chicken
        # 3 = feather
        # 4-7 = poof cloud
        self.animationFrames = []
        animation_types = [("chicken_bomb", 2, 1), ("feather", 1, 1), ("poof", 4, 2)]
        for (animation, num_of_frames, scale) in animation_types:
            temp_list = []
            #Get a list of all the files in the directory
            for i in range(1, num_of_frames+1):
                img = pygame.image.load(f'img/icons/{animation}_{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animationFrames.append(temp_list)

        # variables imported from main
        self.player = None
        self.screen = None
        self.enemyHandler = None
        self.terrain = None

    #import data from main
    def setup(self, playerChar, mainScreen, enemy_handler, GameTerrain):
        self.player = playerChar
        self.screen = mainScreen
        self.enemyHandler = enemy_handler
        self.terrain = GameTerrain

    def spawn_chicken_bomb(self, player):
        # if the amount of spawned chickens bombs are larger than the allowed max value, will then reurn and not spawn a new one.
        if self.current_amount >= self.max_amount:
            return
        rect = self.animationFrames[0][0].get_rect()
        rect.center = (player.rect.midtop[0], player.rect.midtop[1])
        dir = player.direction
        time = 0

        dx = 5 * dir
        dy = -10
        
        on_ground = False
        sensor_right = pygame.Rect(rect.midright, (10,30))
        sensor_right.center = rect.midright
        sensor_left = pygame.Rect(rect.midleft, (10,30))
        sensor_left.center = rect.midleft
        sensor_bottom = pygame.Rect(rect.midbottom, (40,10))
        sensor_bottom.center = rect.midbottom

        chicken_bomb_dict = {"Rectangle":rect, 
                             "Direction":dir, 
                             "Time":time, 
                             "dx":dx, 
                             "dy":dy, 
                             "onGround":on_ground, 
                             "rightSensor":sensor_right, 
                             "leftSensor":sensor_left, 
                             "bottomSensor":sensor_bottom}
        self.active_bombs.append(chicken_bomb_dict)
        self.current_amount += 1 

    def chicken_explo(self):
        # removes the chicken bombs first in the list and decrease the current amount of chickens bombs with 1
        chicken = self.active_bombs.pop(0)
        self.current_amount -= 1

        # variables for setting the explosion
        time = 0
        x = chicken["Rectangle"].centerx
        y = chicken["Rectangle"].centery

        # set the size of the exposion for collision with other objects, ex. player, enemies
        area = 50
        explosion_area = pygame.Rect(x-area, y-area, area*2, area*2)
        explosion_area.center = (x,y)

        exploion_dict = {"Rectangle":explosion_area,
                         "Time":time}
        self.detonated_bombs.append(exploion_dict)

    def update(self, camera_offsetX, camera_offsetY): #update everything
        
        #draws all chicken bombs and explosions before updating timer
        for chicken in self.active_bombs:
            self.draw_chicken(chicken, camera_offsetX, camera_offsetY)
        for explo in self.detonated_bombs:
            self.draw_explosion(explo, camera_offsetX, camera_offsetY)
        
        self.update_timer()

        
    def update_timer(self): #update bomb path, timer, and draw.

        # ---------- updates all chicken bombs ------
        # -------------------------------------------
        for chicken in self.active_bombs: 
            chicken["Time"] += 1 #increase chicken bomb timer
            if chicken["Time"] >= self.time_limit:
                self.chicken_explo()

            # path of the chicken bomb when thrown

            # checks if the chicken bomb collide with terrain on its sides
            # will bounce and go the other way if it is the air
            # will stop rolling if it on the ground
            
            if pygame.Rect.collidelist(chicken["rightSensor"], self.terrain) > -1:
                if chicken["onGround"]:
                    chicken["dx"] *= 0
                else:
                    if chicken["dx"] > 0:
                        chicken["dx"] *= -1
            if pygame.Rect.collidelist(chicken["leftSensor"], self.terrain) > -1:
                if chicken["onGround"]:
                    chicken["dx"] *= 0
                else:
                    if chicken["dx"] < 0:
                        chicken["dx"] *= -1
                        
            
            # add dx to the x value of the chicken bomb
            chicken["Rectangle"].x += chicken["dx"] 

            # calculate dy for y axis
            calc_dy = 0

            # check if the chicken bomb have collision downwards with any terrain
            terrain_index = pygame.Rect.collidelist(chicken["bottomSensor"], self.terrain)
            if terrain_index > -1:
                terrain = self.terrain[terrain_index]
                calc_dy = terrain.top - chicken["Rectangle"].bottom
                chicken["onGround"]=True
                chicken["dy"] = 0
            else: 
                chicken["onGround"]=False

            if not chicken["onGround"]: # if the chicken bomb is on ground, don't increase or decrease dy
                calc_dy = chicken["dy"] + GRAVITY # calculate new dy based on gravite
                chicken["dy"] = calc_dy
            chicken["Rectangle"].y += calc_dy
            
            #increment the value of x and y for the sensors
            for name in ["right","left","bottom"]:
                chicken[name+"Sensor"].x += chicken["dx"]
                chicken[name+"Sensor"].y += calc_dy

        # ---------- updates all exposions ----------
        # -------------------------------------------
        for explo in self.detonated_bombs:
            explo["Time"] += 1 #increase eplosion timer
            self.check_Explosion_Collision(explo["Rectangle"])
            if explo["Time"] >= self.explo_time:
                self.detonated_bombs.remove(explo)

    def check_Explosion_Collision(self, exploRect):
        #checked every update/frame
        if pygame.Rect.colliderect(self.player.rect, exploRect):
            if self.player.alive:
                self.player.health -= 1
        listOfHitEnemies = self.enemyHandler.checkRectCollision(exploRect)
        for enemy in listOfHitEnemies:
            enemy.health -= 5
    
    #draws the chicken bomb
    def draw_chicken(self, chicken, camera_offsetX, camera_offsetY):
        time = chicken["Time"]
        rotation_speed = 4
        # rotates the chicken while alterating between the two sprites
        self.screen.blit(pygame.transform.rotate(self.animationFrames[0][((time % 8) // 4)], time*rotation_speed), 
                         (chicken["Rectangle"].x-camera_offsetX, chicken["Rectangle"].y-camera_offsetY))

        #draws the sensors of the bomb - only for testing
        for name in ["right","left","bottom"]:
            pygame.draw.rect(self.screen, (0,0,0), 
                             pygame.Rect((chicken[name+"Sensor"].x-camera_offsetX), (chicken[name+"Sensor"].y-camera_offsetY), 
                                         chicken[name+"Sensor"].width, chicken[name+"Sensor"].height))
            #pygame.draw.rect(self.screen, (0,0,0), chicken[name+"Sensor"])
        

    #draws the expolosion, both the cloud and the feathers
    def draw_explosion(self, explo, camera_offsetX, camera_offsetY):
        time = explo["Time"]
        speed = 4
        #all directions of the feathers written in x y coordinates. the values is also use for the speed of the feathers
        directions = [(1,0), (-1,0), (0,1), (0,-1),
                      (0.707,0.707), (-0.707,0.707), (0.707,-0.707), (-0.707,-0.707),
                      (0.924,0.383), (0.383,0.924), (-0.924,0.383), (-0.383,0.924),
                      (0.924,-0.383), (0.383,-0.924), (-0.924,-0.383), (-0.383,-0.924)]
        for (i, j) in directions:
            # get the roation degree from x,y
            rotation = math.atan2(i,j)/math.pi*180-90
            # draws the feather
            self.screen.blit(pygame.transform.rotate(self.animationFrames[1][0], rotation), 
                             (explo["Rectangle"].centerx+(time*speed*i)-camera_offsetX, explo["Rectangle"].centery+(time*speed*j)-camera_offsetY))

        #draws the cloud in the middle with an offset to make sure it is in the middle of the explosion.
        offestX = -40
        offestY = -40
        self.screen.blit(self.animationFrames[2][(time // 5)], (explo["Rectangle"].centerx+offestX-camera_offsetX, explo["Rectangle"].centery+offestY-camera_offsetY))