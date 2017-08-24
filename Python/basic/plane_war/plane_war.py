
#! -*- coding:utf-8 -*-

import pygame
import time 

class Window(object):
    def __init__(self,temp1,temp2,temp3):
        self.size = temp1
        self.pos = temp2
        self.color = temp3
        self.window = pygame.display.set_mode(self.size,self.pos,self.color)
        self.image = pygame.image.load('./feiji/background.png')


    def __str__(self):
        return "create a window size:%s pos:%d color_size:%d"%(str(self.size),self.pos,self.color)




class My_hero(object):
    def __init__(self):
        self.image = pygame.image.load('./feiji/hero1.png')
        self.x = 210
        self.y = 700

    def plane_display(self,temp):
        temp.window.blit(self.image,(self.x,self.y))








def main():

    screen = Window((480,852),0,32)

#---------above create a whole background class-----------------
    hero = My_hero()
#--------above create a hero plane class----------------------       

    while True:
        screen.window.blit(screen.image,(0,0))
#---------above create a background----------------------------
        hero.plane_display(screen)

#---------above create a hero plane--------------------------


        pygame.display.update()

        time.sleep(0.01)





if __name__ == '__main__':

    main()


