


class Person():

    def __init__(self,name):
        self.name = name
        self.gun = None
        self.hp = 100

    def __str__(self):
        return "The person name is %s hp is:%s the gun is: %s"%(self.name,self.hp,self.gun)
    def load_bullet(self,temp1,temp2):
        temp1.add_bullet(temp2)

    def load_bullet_package(self,temp1,temp2):
        temp1.bullet_package = temp2

    def load_gun(self,temp):
        self.gun = temp

    def shoot(self,enemy):
        self.gun.shoot(enemy)

    def hp_down(self,temp):
        self.hp -= temp
        if self.hp < 0 :
            print("enemy has died!!!")


class Gun():

    def __init__(self,name):
        self.name = name
        self.bullet_package = None
        self.bullet = None
    def __str__(self):
        return "The name of gun is %s  the bullet_package is:%s"%(self.name,self.bullet_package)#这里的self.bullet_package变量，其实就是调用bullet_package中的__str__方法，因为__str__方法中用的就是return，所以对象名称中保存的值就是__str__

    def add_bullet_package(self,temp):
        self.bullet_package = temp
    
    def shoot(self,temp):
        self.bullet = self.bullet_package.pop_bullet()
        if self.bullet :
            self.bullet.hurt(temp)
        else :
            print("Do not have bullet")


class Bullet_package():
    def __init__(self,max_num):
        self.max_num = max_num
        self.bullet_num=[]


    def __str__(self):
        return "The max num of bullets is %d  load bullet is %d"%(self.max_num,len(self.bullet_num))


    def add_bullet(self,temp):
        self.bullet_num.append(temp)
        

    def pop_bullet(self):
        return self.bullet_num.pop()


class Bullet():
    def __init__(self,ability):
        self.ability = ability

    def __str__(self):
        return "the ability is %d"%self.ability
    
    def hurt(self,temp):
        temp.hp_down(self.ability)



def main():

    bullet = Bullet(10) #创建一个bullet实体，每一个实体都有一个独立的存储空间，即使是由同一个类创造出来的，他们中的属性值（即__init__下的变量值）是不一样的，这也是self的作用，若不用self.xx那么xx表示的就是类的属性，对由其创建的对象是一样的
    print(bullet)

    bullet_package = Bullet_package(30)
    print(bullet_package)


    gun = Gun("AK47")
    print(gun)


    laowang = Person("laowang")
    print(laowang)

#---------above create three classes-----------------------

    for i in range(30):
        bullet = Bullet(10)#创建一个bullet实体
        laowang.load_bullet(bullet_package,bullet) # 这里的参数传递的是对象，不要传递类，因为对象才是实体，类只是一个模具
        print(bullet_package)
#---------above add some bullets--------------------------

    laowang.load_bullet_package(gun,bullet_package)#从这些对象之间的调用可知，python是一种解释性语言，其按照顺序的方式对程序进行解释执行，所以这里的参数对象，必定是前边已经赋值了的
    print(gun)

#---------above add a bullet_package into gun------------

    laowang.load_gun(gun)#在这里的各个函数调用过程中，时刻都会改变main一开始创建的四个对象中的值，因为这四个对象是一个在内存空间中的实体，对象中的属性值通过引用的方式改变其自身的值
    print(laowang)

#--------above add a gun -------------------------------

    laosong = Person("laosong")#这里再次创建一个Person对象，注意这里并不是和laowang是同一个对象，他们分别是独立的一块内存空间，其属性值是不一定相同的

#--------above create a enemy------------------- -------

    laowang.shoot(laosong)
    print(laosong)

    laowang.shoot(laosong)
    print(laosong)
    laowang.shoot(laosong)
    print(laosong)

    laowang.shoot(laosong)
    print(laosong)

    laowang.shoot(laosong)
    print(laosong)


    laowang.shoot(laosong)
    print(laosong)



#---------above shoot enemy-----------------------------





if __name__ == "__main__" :#python中用来区别import和执行运行的方式
    main()

