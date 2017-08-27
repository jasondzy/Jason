#!/usr/bin/python
#! -*- coding:utf-8 -*-

import pygame
import time 

from pygame.locals import *

class Window(object):
    def __init__(self,temp1,temp2,temp3):
        self.size = temp1
        self.pos = temp2
        self.color = temp3        
        self.window = pygame.display.set_mode(self.size,self.pos,self.color)
        self.image = pygame.image.load('./feiji/background.png')


    def __str__(self):
        return "create a window size:%s pos:%d color_size:%d"%(str(self.size),self.pos,self.color)


class Base_plane(object):
    def __init__(self,name0,name1,name2,name3,name4,x,y):
        self.image0 = pygame.image.load(name0)
        self.image1 = pygame.image.load(name1)
        self.image2 = pygame.image.load(name2)
        self.image3 = pygame.image.load(name3)
        self.image4 = pygame.image.load(name4)
        self.x = x
        self.y = y




class My_hero(Base_plane):
    def __init__(self,name0,name1,name2,name3,name4,x,y):
        Base_plane.__init__(self,name0,name1,name2,name3,name4,x,y)
        self.bullet_list = []
        self.mouse_flag = 0

    def display(self,temp):
        temp.window.blit(self.image0,(self.x,self.y))

        for i in self.bullet_list:
            i.display(temp)
            if i.y < 0 :
                self.bullet_list.remove(i)

    def shoot(self,temp):
        bullet = Bullet(self.x,self.y)
        self.bullet_list.append(bullet)
        bullet.enemy.add(temp)

    def mouse_move(self):
        self.x,self.y = pygame.mouse.get_pos()
        self.x -= 50
        self.y -= 62


class Enemy1(Base_plane):
    def __init__(self,name0,name1,name2,name3,name4,x,y):
        Base_plane.__init__(self,name0,name1,name2,name3,name4,x,y)
        self.disappear_flag = 0 
        self.disappear = 0
        self.recreate = 0
        self.direction = 'right'

    def display(self,temp):
        if self.disappear_flag==0 and self.disappear==0:
            temp.window.blit(self.image0,(self.x,self.y))
        if self.disappear_flag == 4 and self.disappear ==0:
            temp.window.blit(self.image1,(self.x,self.y))
            self.disappear_flag -=1
        elif self.disappear_flag == 3 and self.disappear ==0:
            temp.window.blit(self.image2,(self.x,self.y))
            self.disappear_flag -=1
        elif self.disappear_flag == 2 and self.disappear ==0:
            temp.window.blit(self.image3,(self.x,self.y))
            self.disappear_flag -=1
        elif self.disappear_flag == 1 and self.disappear ==0:
            temp.window.blit(self.image4,(self.x,self.y))
            self.disappear_flag -=1
            self.disappear = 1

    def mov(self):
        if self.x >420-10 :
            self.direction = 'left'
        elif self.x <10 :
            self.direction = 'right'
        if self.direction == 'left':
            self.x -=5
        elif self.direction == 'right':
            self.x += 5
        print('direction:%s  x:%d'%(self.direction,self.x))
            

class Bullet(object):

    def __init__(self,temp_x,temp_y):
        self.image = pygame.image.load('./feiji/bullet.png')
        self.x = temp_x
        self.y = temp_y
        self.enemy = set()

    def display(self,temp):
        temp.window.blit(self.image,(self.x,self.y))
        self.y -=20

        for temp in self.enemy:
            print('x:%d  y:%d'%(self.x,self.y))
            if self.x-55 <temp.x and self.x+15 > temp.x and self.y-45 <temp.y and self.y+45 >temp.y and temp.disappear_flag==0:
                temp.disappear_flag = 4
                break
        



def move(temp1,temp2):

    for event in pygame.event.get():

        if event.type == QUIT:
            print('exit')
            exit()  #use to quit frome a programe
        elif event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                print('left')
                temp1.x -=10

            elif event.key == K_d or event.key == K_RIGHT:
                print('right')
                temp1.x +=10

            elif event.key == K_c:
                print('exit')
                exit()
            elif event.key == K_m:
                print('use mouse for moving')
                temp1.mouse_flag = 1
            
            elif event.key == K_SPACE:
                print('space')
                temp1.shoot(temp2)

            elif event.key == K_n:
                print('create a new game')
                temp2.recreate = 1


def main():
    pygame.init() # pygame init
    screen = Window((480,852),0,32)
    pygame.display.set_caption('Plane War') #创建窗口标签
#---------above create a whole background class-----------------
    hero = My_hero('./feiji/hero1.png','./feiji/hero_blowup_n1.png','./feiji/hero_blowup_n2.png','./feiji/hero_blowup_n3.png','./feiji/hero_blowup_n4.png',210,700)
    enemy1 = Enemy1('./feiji/enemy1.png','./feiji/enemy1_down1.png','./feiji/enemy1_down2.png','./feiji/enemy1_down3.png','./feiji/enemy1_down4.png',210,0)
#--------above create a hero plane class----------------------       

    while True:
        screen.window.blit(screen.image,(0,0))
#---------above create a background----------------------------
        hero.display(screen)
        if hero.mouse_flag == 1 :
            hero.mouse_move()
        enemy1.display(screen)
        enemy1.mov()
#---------above create plane--------------------------
        if enemy1.recreate ==1 :
            enemy1 = Enemy1('./feiji/enemy1.png','./feiji/enemy1_down1.png','./feiji/enemy1_down2.png','./feiji/enemy1_down3.png','./feiji/enemy1_down4.png',210,0)
            enemy1.recreate = 0
        move(hero,enemy1)

     
        pygame.display.update()

        time.sleep(0.01)





if __name__ == '__main__':

    main()


