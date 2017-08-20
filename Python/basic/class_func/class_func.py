

class Game(object):

    num = 0

    def __init__(self):
        self.name = "croos fire"


    #define a class func , use classmethod to define

    @classmethod
    def class_num(cls):
        cls.num +=1

    #staticmethod can no args . so no self or cls and so on...
    @staticmethod
    def print_info():
        print("---------------------")
        print("   cross fire    ")
        print ("___________________")


game = Game()

# call the object func
print(game.name)

#call the class func
#Game.class_num()  or
game.class_num()
print(Game.num)

#call the static func
#Game.print_info() or
game.print_info()




