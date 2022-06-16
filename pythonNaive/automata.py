import code
from email.errors import BoundaryError
from email.iterators import body_line_iterator
from sqlite3 import converters
import time
from tkinter import CENTER, X
import pygame
import numpy as np
import random
import sys

#TODO:--------------
    # [x] Game of Life base code
    # [x] Game of Life improved code + push
    # [x] Game of life snek food
    # [x] snek movement
    # [] snek dead
    # [x] little brain snek
    # [] big brain snek
    # [x] elongated snek
    # [] more snek
    # [] big brain snek have children 
    # [] Pararell multi-threaded sneks with GPU

#[:+:] -- for 16:9 1080p: H=9, W=16, scalar=12, cellsize=10
# less ideal Cellsize= 12, scalar9, HW:9,16,
cellSize= 10
scalar= 9
H= 9*scalar
W= 16*scalar
gridDim= (H,W)
gridTrim= (H-1,W-1)
resolution= (W*cellSize,H*cellSize)
CENTER_YX= (resolution[1]//2, resolution[0]//2)

automata= True
wasd= True
ai= True
#snake= False
randomSpawn= False


tickInterval= 0.0001
spawnRate= 35
deathRate= 30
timeSpan= 1023
snakeLimit= 10
chronolog= pygame.time.Clock()


# https://colordesigner.io/#F34A53-FAE3B4-AAC789-437356-1E4147
# https://colordesigner.io/#FF6138-FFFF9D-BEEB9F-79BD8F-00A388
rgb_beige= (255, 255, 157)
rgb_brightGreen= (190, 235, 159)
rgb_midGreen= (121, 189, 143)
rgb_turquoise= (0, 163, 136)
rgb_darkGreen= (67, 115, 86)
rgb_darkBlue= (30, 65, 71)
rgb_purple= (128, 110, 158)
rgb_red= (243, 74, 83)
rgb_orange= (255, 97, 56)
rgb_white= (255,255,255)
rgb_brightYellow= (251, 255, 128)
rgb_lBlue= (30, 176, 224)
colorRand= [0,0,0]
# rgb_seedGreen= (210, 0, 255)


class SynchronousSnakeMachine:
    def __init__(self):
        self.x= CENTER_YX[1]
        self.y= CENTER_YX[0]
        # self.yx= [cellSize, cellSize]
        self.headPos= (self.x, self.y)
        self.bodPos= (self.x-cellSize, self.y)
        self.xStep= 1
        self.yStep= 0
        self.headSize= (cellSize+2, cellSize+2)
        self.bodSize= ((cellSize), (cellSize))
        self.head= pygame.Rect((self.headPos),(self.headSize))
        self.bodArr= [pygame.Rect((self.bodPos), (self.bodSize))]
    def step(self):
        self.bodArr.append(self.head)
        for i in range(len(self.bodArr)-1):
            self.bodArr[i].x = self.bodArr[i+1].x
            self.bodArr[i].y = self.bodArr[i+1].y
        self.head.x+= self.xStep*cellSize
        self.head.y+= self.yStep*cellSize
        if(self.head.x <= 1):
            self.xStep= 1
        elif(self.head.x >= W*cellSize-1):
            self.xStep= -1
        if(self.head.y <= 1):
            self.yStep= 1
        elif(self.head.y >= H*cellSize-1):
            self.yStep= -1
        self.bodArr.remove(self.head)

    


def tick(canvas, cellMatrix, cellSize, clk, snek,snake):
    matrixReloaded = np.zeros(gridDim)
    snek.step()
    snek_i= 0
    snekLen= len(snek.bodArr)
    if (clk%73):canvas.fill('black')

  

    # for y, x in np.ndindex(gridTrim):
    if(automata):
        for y in range(0,gridTrim[0]):
            #canvas.fill('black')
            for x in range(0,gridTrim[1]):
                left= cellMatrix[y][x-1] 
                right= cellMatrix[y][x+1]
                top= cellMatrix[y-1][x] 
                bot= cellMatrix[y+1][x] 
                topLeft= cellMatrix[y-1][x-1] 
                topRight= cellMatrix[y-1][x+1]
                botLeft= cellMatrix[y+1][x-1] 
                botRight= cellMatrix[y+1][x+1] 
                neighborhood= left+right+top+bot+topLeft+topRight+botLeft+botRight 

                #[:+:] -- Cell Logic ------------------------------------------------------------------------------------------------------/////
                rgbState=  ('black')
                if cellMatrix[y,x]:
                    rgbState= rgb_darkGreen
                    if 2 <= neighborhood <=3:
                        matrixReloaded[y,x]= 1
                        if(neighborhood==2):
                            if (left and right) or (top and bot):
                                rgbState=  rgb_orange
                                # print("foodYX:  " + str(y)+"."+str(x))
                            elif (topLeft+topRight+botRight+botLeft==2)and(topLeft+botRight==1)and(top+left+bot+right==0):
                                rgbState= rgb_purple if (clk%9) else rgb_darkBlue
                            if (abs(x*cellSize-snek.head.x)<=1) and (abs(y*cellSize-snek.head.y)<=10) and (snake):
                                if(snekLen<snakeLimit):
                                    snekTangle= pygame.Rect(((snek.head.x, snek.head.y),(cellSize+snekLen//3,cellSize+snekLen//3)))
                                    snek.bodArr.append(snekTangle)
                                    snekLen+= 1
                                    # snek.bodArr.append(pygame.Rect((snek.head.x, snek.head.y),(snek.bodSize)))
                                rgbState= (0,0,0)
                                matrixReloaded[y,x]= 0
                        else:
                            if(top):
                                if((topLeft and left) or (topRight and right)):
                                    rgbState= rgb_darkBlue
                            elif(bot):
                                if((botLeft and left)):
                                    rgbState= rgb_darkBlue
                                elif (botRight and right):
                                    rgbState=  rgb_darkGreen
                            else:
                                rgbState= rgb_brightGreen
                    elif neighborhood < 2:
                        matrixReloaded[y,x]= 0
                        rgbState= rgb_brightGreen
                    elif neighborhood > 3:
                        matrixReloaded[y,x]= 0
                        rgbState= rgb_midGreen
                    else:
                        rgbState= rgb_brightYellow
                else:
                    if neighborhood == 3:
                        matrixReloaded[y,x]= 1
                        rgbState= rgb_darkGreen
                #-------------------------------------------------------------------------------------------------------------------------////



                # [+]:: -- //process rectangles + snek brain-----------------------------------------------------//
                cellTangle = pygame.Rect((cellSize*x, cellSize*y),(cellSize-1, cellSize-1))
                if(ai) and (snake) and (rgbState==rgb_purple):
                    if (clk%11):
                        if (snek.head.x<x*cellSize):
                            snek.xStep= 1
                        elif (snek.head.x>x*cellSize):
                            snek.xStep = -1
                        if (snek.head.y<y*cellSize):
                            snek.yStep = 1
                        elif (snek.head.y>y*cellSize):
                             snek.yStep = -1
                    else:
                        randX= random.randint(-1,1)
                        randY= random.randint(-1,1)
                        snek.xStep= randX
                        snek.yStep= randY
                    # if (abs(x*cellSize-snek.head.x)<=5) and (abs(y*cellSize-snek.head.y)<=5) and (snake):
                    # #if(snekLen<10):
                    #     #snekTangle= pygame.Rect(((snek.head.x, snek.head.y),(snek.bodSize)))
                    #     snek.bodArr.append(cell)
                    #     # snek.bodArr.append(pygame.Rect((snek.head.x, snek.head.y),(snek.bodSize)))
                    #     snekLen+= 1
                    #     rgbState= (0,0,0)
                    #     matrixReloaded[y,x]= 0
                render(canvas, cellMatrix, cellTangle, rgbState, clk,snek,snake,x)
    return matrixReloaded
        



def render(canvas,cellMatrix, cellTangle, rgbState,clk,snek,snake,x):
    pygame.draw.rect(canvas, rgbState, (cellTangle))
    if(snake):
        if(x%3):
            for i in range(0,len(snek.bodArr)):
                pygame.draw.rect(canvas, rgb_lBlue, snek.bodArr[i])
                pygame.draw.rect(canvas, rgb_red, snek.head)


    
   


def main():
    #---[+]:: Initializatin ---------------------//
    pygame.init()
    grid= pygame.display.set_mode(resolution)
    cellMatrix= np.zeros(gridDim)
    clk= 0
    paused= False
    snake= False
    snek= SynchronousSnakeMachine()
    snekMom= SynchronousSnakeMachine()
    snekDad= SynchronousSnakeMachine()
    numSnek=1
    grid.fill('black')
    pygame.display.flip()
    pygame.display.update()
    #------------------------------------------//


    

    while True:
        #---[+]:: Event Handler -------------------------------------------//
        for event in pygame.event.get():
            mouseX= pygame.mouse.get_pos()[0]//cellSize
            mouseY= pygame.mouse.get_pos()[1]//cellSize 
            mouseYXRez= (mouseY*cellSize, mouseX*cellSize)
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused= not paused
                    print("[:+:] -- Cell Calculations: "+ str(clk))
                    print("snake size: " + str(len(snek.bodArr)))
                    print("Grid Size: " + str(gridDim))
                    print("snakeYX:  " + str(snek.head.y) +" , " + str(snek.head.x))
                    #print(str(chronolog.get_fps))
                if event.key == pygame.K_0:
                    print('Snek0YX:  ' + str(mouseYXRez))
                    snake = True
                    # tick(grid,cellMatrix,cellSize,clk, Snek())
                    # pygame.display.update()
                if (event.key==pygame.K_e) or (pygame.mouse.get_pressed()[1]):
                    cellMatrix[mouseY, mouseX:mouseX+2]= 1
                    cellMatrix[mouseY, mouseX+4:mouseX+7]= 1
                    mouseX= (W-4) if mouseX >= (W-3) else mouseX
                    cellMatrix[mouseY-1, mouseX+3]= 1
                    cellMatrix[mouseY-2, mouseX+1]= 1
                if(wasd):
                    if event.key == pygame.K_w:
                        snek.yStep= -1 
                        #snek.xStep= 0  
                    if event.key == pygame.K_a:
                        #snek.yStep= 0
                        snek.xStep= -1 
                    if event.key == pygame.K_s:
                        snek.yStep= 1
                        #snek.xStep= 0 
                    if event.key == pygame.K_d:
                        #snek.yStep= 0
                        snek.xStep= 1 
            if pygame.mouse.get_pressed()[0]:
                print('left clickYX:  ' + str(mouseYXRez) )
                mouseX= (W-4) if mouseX >= (W-3) else mouseX
                cellMatrix[mouseY,mouseX]= not cellMatrix[mouseY,mouseX]
                tick(grid,cellMatrix,cellSize,clk,snek, snake)
                pygame.display.update()
            if pygame.mouse.get_pressed()[2]:
                print('Right clickYX:  ' + str(mouseYXRez) )
                mouseX= (W-2) if mouseX >= (W-1) else mouseX
                cellMatrix[mouseY][mouseX-1]= 1 
                cellMatrix[mouseY][mouseX+1]= 1
                cellMatrix[mouseY-1][mouseX]= 1 
                cellMatrix[mouseY+1][mouseX]= 1 
            if (pygame.mouse.get_pressed()[1]):
                print('middle clickYX:  ' + str(mouseYXRez) )
                cellMatrix[mouseY, mouseX:mouseX+2]= 1
                cellMatrix[mouseY, mouseX+4:mouseX+7]= 1
                mouseX= (W-4) if mouseX >= (W-3) else mouseX
                cellMatrix[mouseY-1, mouseX+3]= 1
                cellMatrix[mouseY-2, mouseX+1]= 1
        #---[+]:: \\Event Handler -------------------------------------------//

        

        #---[+]:: Random Cell Spawner-----------------------------------//
        if(randomSpawn):
            acornX= random.randint(1,W-7)
            acornY= random.randint(2,H-1)
            if not(clk%(timeSpan//spawnRate)): 
                if(clk%2):
                    cellMatrix[acornY, acornX:acornX+2]= 1
                    cellMatrix[acornY, acornX+4:acornX+7]= 1
                    cellMatrix[acornY-1, acornX+3]= 1
                    cellMatrix[acornY-2, acornX+1]= 1
                else:
                    cellMatrix[acornY-1:acornY+2, acornX-1:acornY+2]= 1
            if not(clk%(timeSpan//deathRate)):
                if(clk%2):
                    cellMatrix[acornY,acornX]= 0;
                    cellMatrix[acornY-2,acornX]= 0;
                    cellMatrix[acornY,acornX-1]= 0;
                    cellMatrix[acornY,acornX+6]= 0;
                else:
                    cellMatrix[acornY-1:acornY+2, acornX-1:acornY+2]= 0
        #---[+]:: \\Random Cell Spawner-----------------------------------//



        #---[+]:: Update Functions + Clock Stuff-------------------------------//
        if not paused:
            cellMatrix = tick(grid, cellMatrix, cellSize,clk, snek, snake)
            clk = 0 if clk >= timeSpan else clk+1 
            pygame.display.update()
            chronolog.tick
            clk+=1
            #clock.tick(10)
            time.sleep(tickInterval)
        #---[+]:: \\Update Functions----------------------------//

if __name__ == '__main__':
    main()


    ##How I made the executable
    # to install converter:
    #     $ pop install auto-py-to-exe
    # to run the converter:
    #     $ auto-py-toexe.exe 