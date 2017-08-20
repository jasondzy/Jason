

class  Dog(object):

    def __init__(self):
        print("init the var")

    def __new__(cls): # the func is used to create a new class , 
        print("create a class")
        return object.__new__(cls) # use the parent __new__ func to create a class,the arg need transfer cls
    
    def __str__(self):
        return "Hello world"


dog = Dog()
print(dog)

