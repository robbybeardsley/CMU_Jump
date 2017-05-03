'''
  .--.     ___ .-. .-.    ___  ___         .-.   ___  ___   ___ .-. .-.      .-..   
 /    \   (   )   '   \  (   )(   )       ( __) (   )(   ) (   )   '   \    /    \  
|  .-. ;   |  .-.  .-. ;  | |  | |        (''")  | |  | |   |  .-.  .-. ;  ' .-,  ; 
|  |(___)  | |  | |  | |  | |  | |         | |   | |  | |   | |  | |  | |  | |  . | 
|  |       | |  | |  | |  | |  | |         | |   | |  | |   | |  | |  | |  | |  | | 
|  | ___   | |  | |  | |  | |  | |         | |   | |  | |   | |  | |  | |  | |  | | 
|  '(   )  | |  | |  | |  | |  ; '         | |   | |  ; '   | |  | |  | |  | |  ' | 
'  `-' |   | |  | |  | |  ' `-'  /     ___ | |   ' `-'  /   | |  | |  | |  | `-'  ' 
 `.__,'   (___)(___)(___)  '.__.'     (   )' |    '.__.'   (___)(___)(___) | \__.'  
                                       ; `-' '                             | |      
                                        .__.'                             (___)   
'''

import pygame
from pygame.locals import *
import sys
import os
import random
import pickle

'''
Template used from Pygame Lecture
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
'''

class cmuJump():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.gameDisplay = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("CMU Jump")
        self.font = pygame.font.SysFont("Comic Sans MS", 30)
        self.scoreFont = pygame.font.SysFont("Comic Sans MS", 22)
        self.titleFont = pygame.font.SysFont("Comic Sans MS", 50)

        self.width, self.height = pygame.display.get_surface().get_size()
        self.playerX = 250
        self.playerY = 400
        self.jump = 0
        self.gravity = 0
        self.direction = True
        self.shooting = False

        #IMAGES : https://www.pinterest.com/pin/82050024436991915/ +
        #         https://github.com/Max00355/DoodleJump/tree/master/assets
        self.player1R = pygame.image.load("assets/right.png").convert_alpha()
        self.player2R = pygame.image.load("assets/right_1.png").convert_alpha()
        self.player1L = pygame.image.load("assets/left.png").convert_alpha()
        self.player2L = pygame.image.load("assets/left_1.png").convert_alpha()
        self.shootingPlayer = pygame.image.load("assets/shootingPlayer.jpg").convert_alpha()
        self.greenPlatform = pygame.image.load("assets/green.jpg").convert_alpha()
        self.monster = pygame.image.load("assets/blueMonster.jpg").convert_alpha()
        self.alien = pygame.image.load("assets/alien.jpg").convert_alpha()
        self.bullet = pygame.image.load("assets/bullet.jpg").convert_alpha()
        #PLAYER 2 IMAGES
        self.player1R2 = pygame.image.load("assets/right2.png").convert_alpha()
        self.player2R2 = pygame.image.load("assets/right2_1.png").convert_alpha()
        self.player1L2 = pygame.image.load("assets/left2.png").convert_alpha()
        self.player2L2 = pygame.image.load("assets/left2_1.png").convert_alpha()
        self.bam = pygame.image.load("assets/bam.gif").convert_alpha()

        self.score = 0
        #COLORS
        self.greenColor = (76,160,0)
        self.whiteColor = (255,255,255)
        self.lightGreenColor = (0,204,0)
        self.blackColor = (0,0,0)

        self.mouse = pygame.mouse.get_pos()
        self.clock = pygame.time.Clock()
        self.yScroller = 0
        self.reached = True
        self.check = 0
        self.offset = 450
        self.platforms = [(250,550),(100,500)]

        #PLAYER 2
        self.player2X = 100
        self.player2Y = 350
        self.jump2 = 0
        self.direction2 = True
        self.gravity2 = 0

        self.playerDead = False
        self.player2Dead = False
        #MONSTERS
        self.monsters = []
        self.monsterOffset = 0
        self.counter = 0

        self.bullets = []

    def splashScreen(self):
        self.__init__()

        playerX = 50
        playerY = 425
        gravity = 0
        jump = 0

        splash = True
        while splash:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()

                self.mouse = pygame.mouse.get_pos() 

            #These check if any buttons are pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #play button pressed
                    if 100+40 > self.mouse[0] > 100-40 and 170+25 > self.mouse[1] > 170-25:
                        splash = False
                        #enter play mode
                        self.mode = "play"
                        return

                    #info button pressed
                    if 205+80 > self.mouse[0] > 205-85 and 280+25 > self.mouse[1] > 280-25:
                        splash = False
                        self.mode = "multiplayer"
                    #highscores button pressed
                    if 280+80 > self.mouse[0] > 280-85 and 370+25 > self.mouse[1] > 370-25:
                        splash = False
                        self.mode = "highscores"

            #checks if mouse hovers over "play" and "info" and "highscores"
            if 100+40 > self.mouse[0] > 100-40 and 170+25 > self.mouse[1] > 170-25:
                play = self.font.render("Play!", False, self.blackColor)
            else:
                play = self.font.render("Play!", False, self.greenColor)

            if 205+80 > self.mouse[0] > 205-85 and 280+25 > self.mouse[1] > 280-25:
                multiplayer = self.font.render("Multiplayer!", False, self.blackColor)
            else:
                multiplayer = self.font.render("Multiplayer!", False, self.greenColor)

            if 280+80 > self.mouse[0] > 280-85 and 370+25 > self.mouse[1] > 370-25:
                highscores = self.font.render("Highscores!", False, self.blackColor)
            else:
                highscores = self.font.render("Highscores!", False, self.greenColor)

            self.gameDisplay.fill(self.whiteColor)

            title = self.titleFont.render("CMU Jump", False, self.greenColor)
            self.gameDisplay.blit(title, (75, 50))
            self.gameDisplay.blit(play, (75,150))
            self.gameDisplay.blit(multiplayer, (120,260))
            self.gameDisplay.blit(highscores, (200, 350))
            self.gameDisplay.blit(self.alien, (250, 150))
            self.gameDisplay.blit(self.greenPlatform, (50,500))

            if playerY >= 450:
                jump = 18
                gravity = 0

            #Got this block of code online: https://www.raywenderlich.com/15230/
            #how-to-make-a-platform-game-like-super-mario-brothers-part-1
            #Physics of player jumping
            if not jump:
                playerY += gravity
                gravity += 1
            else:
                playerY -= jump
                jump -= 1

            if jump:
                self.gameDisplay.blit(self.player2R, (playerX, playerY))
            else:
                self.gameDisplay.blit(self.player1R, (playerX, playerY))

            pygame.display.update()
            self.clock.tick(30)

    def updatePlayer(self):
        move = 10
        key = pygame.key.get_pressed()
        #CITATION: https://github.com/Max00355/DoodleJump
        if key[K_RIGHT]:
            self.shooting = False
            self.direction = True
            self.playerX += move
            if self.playerX > 430:
                self.playerX = -40
        if key[K_LEFT]:
            self.shooting = False
            self.direction = False
            self.playerX -= move
            if self.playerX < -50:
                self.playerX = 425
        #DISPLAYING PLAYER FACING RIGHT DIRECTION AND JUMPING
        if self.direction and not self.shooting:
            if self.jump:
                self.gameDisplay.blit(self.player2R, 
                    (self.playerX,self.playerY-self.yScroller))
            else:
                self.gameDisplay.blit(self.player1R, 
                    (self.playerX,self.playerY-self.yScroller))
        elif not self.direction and not self.shooting:
            if self.jump:
                self.gameDisplay.blit(self.player2L, 
                    (self.playerX,self.playerY-self.yScroller))
            else:
                self.gameDisplay.blit(self.player1L, 
                    (self.playerX,self.playerY-self.yScroller))
        else:
            self.gameDisplay.blit(self.shootingPlayer, 
                (self.playerX,self.playerY - self.yScroller))
        #END CITATION ##########################################


        #CITATION: https://www.raywenderlich.com/15230/
        #how-to-make-a-platform-game-like-super-mario-brothers-part-1
        #Physics of player jumping
        if not self.jump:        
            self.playerY += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playerY -= self.jump
            self.jump -= 1
        #####################################

        #SCROLLER
        displayMid = 300 + self.yScroller
        if self.playerY < displayMid:
            self.yScroller -= (displayMid - self.playerY)//25
        #KEEPING SCORE
        if not self.jump and not self.gravity:
            self.score = 200 - self.playerY//10

        #MONSTER INTERACTION
        monsterWidth = self.monster.get_width()
        monsterHeight = self.monster.get_height()
        player = pygame.Rect((self.playerX, self.playerY+10), 
            (self.player1R.get_width()-10, 50))  
        player2 = pygame.Rect((self.player2X, self.player2Y+10),
            (self.player1R.get_width()-10,50))

        for monster in self.monsters:
            monsterDead = False
            monsterRect = pygame.Rect(monster[0]+10,monster[1], monsterWidth-15, 10)
            if monsterRect.colliderect(player) and self.playerY > monster[1]-20:
                self.playerDead = True
            elif monsterRect.colliderect(player) and (self.playerY < monster[1])\
            and not self.jump:
                monster[1] = 700
                self.jump = 25
                self.gravity = 0
            if monsterRect.colliderect(player2) and self.playerY > monster[1]-20:
                self.player2Dead = True
            elif monsterRect.colliderect(player2) and (self.player2Y < monster[1])\
            and not self.jump2:
                monster[1] = 700
                self.jump2 = 25
                self.gravity2 = 0

        if self.playerDead:
            self.playerY += 25
            self.gameDisplay.blit(self.bam, (self.playerX,self.playerY-self.yScroller-15))
        elif self.player2Dead:
            self.playerY += 25
            self.gameDisplay.blit(self.bam, (self.player2X,self.player2Y-self.yScroller-15))

    #SAME CITATIONS AS updatePlayer()
    def updatePlayer2(self):
        move = 10
        key = pygame.key.get_pressed()
        if key[K_d]:
            self.direction2 = True
            self.player2X += move
            if self.player2X > 430:
                self.player2X = -40
        if key[K_a]:
            self.direction2 = False
            self.player2X -= move
            if self.player2X < -50:
                self.player2X = 425
        
        #DISPLAYING PLAYER FACING RIGHT DIRECTION AND JUMPING OR NOT
        if self.direction2:
            if self.jump2:
                self.gameDisplay.blit(self.player2R2, 
                    (self.player2X,self.player2Y-self.yScroller))
            else:
                self.gameDisplay.blit(self.player1R2, 
                    (self.player2X,self.player2Y-self.yScroller))
        else:
            if self.jump2:
                self.gameDisplay.blit(self.player2L2, 
                    (self.player2X,self.player2Y-self.yScroller))
            else:
                self.gameDisplay.blit(self.player1L2, 
                    (self.player2X,self.player2Y-self.yScroller))

        #CITATION: https://www.raywenderlich.com/15230/
        #how-to-make-a-platform-game-like-super-mario-brothers-part-1
        #Physics of player jumping
        if not self.jump2:        
            self.player2Y += self.gravity2
            self.gravity2 += 1
        elif self.jump2:
            self.player2Y -= self.jump2
            self.jump2 -= 1
        #SCROLLER
        displayMid = 300 + self.yScroller
        if self.player2Y < displayMid:
            self.yScroller -= (displayMid - self.player2Y)//25

    def shootBullets(self, x, y):
        self.bullets.append([x,y])

    def drawBullets(self):
        monsterWidth = self.monster.get_width()
        monsterHeight = self.monster.get_height()

        for bullet in self.bullets:
            if bullet[1] < self.yScroller - 600:
                continue
            self.gameDisplay.blit(self.bullet, (bullet[0],bullet[1]-self.yScroller))
            bullet[1] -= 20

            bulletRect = pygame.Rect((bullet[0],bullet[1]),(5,5))
            for monster in self.monsters:
                monsterRect = pygame.Rect((monster[0]+10,monster[1]),(monsterWidth-15,10))

                if bulletRect.colliderect(monsterRect):
                    monster[1] = 700
                    bullet[1] = -1000000000

        if self.bullets != []:
            if self.bullets[0][1] < self.yScroller - 700:
                self.bullets.pop(0)

    def updatePlatforms(self):
        width,height = self.greenPlatform.get_width(), self.greenPlatform.get_height()
        playerW, playerH = self.player2R.get_width(), self.player2R.get_height()
        player = pygame.Rect((self.playerX, self.playerY+10), 
            (self.player1R.get_width()-10, 50))  
        player2 = pygame.Rect((self.player2X, self.player2Y+10),
            (self.player1R.get_width()-10,50))   
        tempPlatforms = []
        for platform in self.platforms:
            if platform[1] < self.yScroller:
                return
            self.gameDisplay.blit(self.greenPlatform, (platform[0],platform[1]-self.yScroller))
            platformRect = pygame.Rect(platform[0]+10,platform[1], width-15, 10)

            #JUMP OFF PLATFORMS for player 
            if platformRect.colliderect(player) and not self.jump and\
            self.playerY < platform[1] - 15:
                self.jump = 18
                self.gravity = 0
            #JUMP for player2
            if platformRect.colliderect(player2) and not self.jump2 and\
            self.player2Y < platform[1] - 15:
                self.jump2 = 18
                self.gravity2 = 0

    def makePlatforms(self):
        self.offset -= 90 - self.yScroller//10 + random.randint(-15,15)
        x = random.randint(0,350)
        y = self.offset 
        for platform in self.platforms:
            if abs(platform[0] - x) < 55 and abs(platform[1] - y) < 25:
                return
        self.platforms.append((x,y))

    def makePlatformsMultiplayer(self):
        self.offset -= 45 + random.randint(-15,15)
        x = random.randint(0,350)
        y = self.offset 
        for platform in self.platforms:
            if abs(platform[0] - x) < 55 and abs(platform[1] - y) < 25:
                return
        self.platforms.append((x,y))

    def makeMonsters(self):
        self.counter += 1
        if self.counter%100 == 0:
            self.monsterOffset -= 1500
            x = random.randint(0,350)
            y = self.monsterOffset
            for platform in self.platforms:
                if abs(platform[0]-x) < 30 and abs(platform[1]-y) < 30:
                    return
            self.monsters.append([x,y])

    def drawMonsters(self):
        for monster in self.monsters:
            self.gameDisplay.blit(self.monster, (monster[0], 
                monster[1] - self.yScroller))

    def checkPlayerCollision(self):
        player = pygame.Rect((self.playerX, self.playerY+10), 
            (self.player1R.get_width()-10, 50))  
        player2 = pygame.Rect((self.player2X, self.player2Y+10),
            (self.player1R.get_width()-10,50))

        if player.colliderect(player2) and self.playerY < self.player2Y:
            self.player2Dead = True

        elif player2.colliderect(player) and self.player2Y < self.playerY:
            self.playerDead = True

        if self.playerDead:
            self.playerY += 20
            self.gameDisplay.blit(self.bam, (self.playerX,self.playerY-self.yScroller-15))
        elif self.player2Dead:
            self.player2Y += 20
            self.gameDisplay.blit(self.bam, (self.player2X,self.player2Y-self.yScroller-15))

    def play(self):
        self.__init__()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        self.shootBullets(self.playerX+5, self.playerY)
            self.gameDisplay.fill(self.whiteColor)
            self.mouse = pygame.mouse.get_pos()
            self.gameDisplay.blit(self.scoreFont.render(str(self.score), 
                False, self.greenColor), (25, 25))
            self.makePlatforms()
            self.makeMonsters()
            self.drawMonsters()
            self.drawBullets()
            self.updatePlatforms()
            self.updatePlayer()
            pygame.display.update()
            self.clock.tick(30)
            if self.playerY > 570 + self.yScroller:
                self.mode = "gameOver"
                return self.gameOver(self.score, 0)

    def multiplayer(self):
        self.__init__()
        playing = True
        while playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE:
                        self.shootBullets(self.playerX+5, self.playerY)
                    if event.key == K_s:
                        self.shootBullets(self.player2X+5, self.player2Y)
            self.gameDisplay.fill(self.whiteColor)
            self.mouse = pygame.mouse.get_pos()
            self.gameDisplay.blit(self.scoreFont.render(str(self.score), 
                False, self.greenColor), (25, 25))
            self.makePlatformsMultiplayer()
            self.updatePlatforms()
            self.makeMonsters()
            self.drawMonsters()
            self.drawBullets()
            if not self.playerDead:
                self.updatePlayer()
            if not self.player2Dead:
                self.updatePlayer2()
            self.checkPlayerCollision()
            pygame.display.update()
            self.clock.tick(30)
            if self.playerY > 570 + self.yScroller:
                self.mode = "gameOver1"
                return self.gameOver(self.score, 2)
            if self.player2Y > 570 + self.yScroller:
                self.mode = "gameOver1"
                return self.gameOver(self.score, 1)

    def gameOver(self, score, whoWon):
        highscore = self.highscores(score)

        gameOver = True
        while gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        pygame.quit()
                        quit()

                self.mouse = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    #play again button pressed
                    if 220+70 > self.mouse[0] > 220-75 and 380+20 > self.mouse[1] > 380-20:
                        #gameOver = not gameOver #False
                        if self.mode == "gameOver":
                            self.mode = "play"
                            return
                        elif self.mode == "gameOver1":
                            self.mode = "multiplayer"
                            return

                    #menu button pressed
                    if 275+40 > self.mouse[0] > 275-40 and 470+20 > self.mouse[1] > 470-20:
                        gameOver = not gameOver #False
                        #enter splash screen
                        self.mode = "splash"
                        return

            #checks if mouse hovers over "play again!" and "menu"
            if 220+70 > self.mouse[0] > 220-75 and 380+20 > self.mouse[1] > 380-20:
                play = self.font.render("Play again!", False, self.blackColor)
            else:
                play = self.font.render("Play again!", False, self.greenColor)

            if 275+40 > self.mouse[0] > 275-40 and 470+20 > self.mouse[1] > 470-20:
                menu = self.font.render("Menu", False, self.blackColor)
            else:
                menu = self.font.render("Menu", False, self.greenColor)

            self.gameDisplay.fill(self.whiteColor)

            title = self.titleFont.render("Game Over!", False, self.greenColor)
            self.gameDisplay.blit(title, (75, 50))

            if whoWon != 0:
                whoWonDisplay = self.font.render("Player "+str(whoWon)+" won!", False, self.blackColor)
                self.gameDisplay.blit(whoWonDisplay, (115,120))

            scoreString = "score: " + str(score)
            self.gameDisplay.blit(self.font.render(str(scoreString), False, self.greenColor), (35,175))

            #PLACE HOLDER: need to get high score somehow...
            #highscore = 50
            highscoreDraw = self.font.render("highscore: "+ str(highscore), False, self.greenColor)
            self.gameDisplay.blit(highscoreDraw, (35,250))

            self.gameDisplay.blit(play, (150,355))
            self.gameDisplay.blit(menu, (240,450))

            #RANDOM MOVEMENT OF MONSTER 
            monsterX = random.randint(25,90)
            monsterY = random.randint(440,475)
            self.gameDisplay.blit(self.monster, (monsterX,monsterY))

            pygame.display.update()
            self.clock.tick(10)

    def highscores(self, score):
        #write scores to txt file then read file by splitlines to find highest
        #score 
        try:
            high_scores = open("highscores.txt","rb")
            prevHighScore = pickle.load(high_scores)
            high_scores.close()
        except EOFError:
            prevHighScore = 0

        high_scores = open("highscores.txt", "wb")
        if score > prevHighScore:
            pickle.dump(score, high_scores)
            high_scores.close()
            return score
        else:
            high_scores.close()
            return prevHighScore

    def highscoresScreen(self):
        highscores = True
        menuFont = pygame.font.SysFont("Comic Sans MS", 40)
        while highscores:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameOver = False
                        pygame.quit()
                        quit()

                self.mouse = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #menu button pressed
                    if 275+40 > self.mouse[0] > 275-40 and 470+20 > self.mouse[1] > 470-20:
                        highscores = not highscores #False
                        #enter splash screen
                        self.mode = "splash"
                        return

            if 275+65 > self.mouse[0] > 275-50 and 470+35 > self.mouse[1] > 470-50:
                menu = menuFont.render("Menu", False, self.blackColor)
            else:
                menu = menuFont.render("Menu", False, self.greenColor)

            self.gameDisplay.fill(self.whiteColor)

            title = self.titleFont.render("Highscores!", False, self.greenColor)
            self.gameDisplay.blit(title, (75, 50))

            score1 = self.font.render("Kosbie : 100,000", False, self.greenColor)
            score2 = self.font.render("DGA : 100,000", False, self.greenColor)
            score3 = self.font.render("Rohan : 50,000", False, self.greenColor)
            score4 = self.font.render("Eddie : 50,000", False, self.greenColor)
            score5 = self.font.render("Tetris : 10,000", False, self.greenColor)
            score6 = self.font.render("playGame42 : -50,000 !", False, self.greenColor)

            self.gameDisplay.blit(score1,(40, 150))
            self.gameDisplay.blit(score2, (40,200))
            self.gameDisplay.blit(score3, (40,250))
            self.gameDisplay.blit(score4, (40,300))
            self.gameDisplay.blit(score5, (40,350))
            self.gameDisplay.blit(score6, (40,400))
            self.gameDisplay.blit(menu, (240,450))

            #RANDOM MOVEMENT OF MONSTER 
            monsterX = random.randint(25,90)
            monsterY = random.randint(440,475)
            self.gameDisplay.blit(self.monster, (monsterX,monsterY))

            pygame.display.update()
            self.clock.tick(8)

    def main(self):
        self.mode = "splash"
        On = True
        while On:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    On = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        On = False
                        pygame.quit()
                        quit()
            if self.mode == "splash":
                self.splashScreen()
            elif self.mode == "play":
                self.play()
            elif self.mode == "highscores":
                self.highscoresScreen()
            elif self.mode == "multiplayer":
                self.multiplayer()
        pygame.quit()
        quit()









