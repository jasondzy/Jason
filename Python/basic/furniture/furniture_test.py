

class room():
    
    def __init__(self,area,addr,info):
        
        self.area = area
        self.addr = addr
        self.info = info
        self.useful = self.area

    def __str__(self):

        msg = "romm:size is :%d area useful is:%d   addr is:%s  info is:%s   "%(self.area,self.useful,self.addr,self.info)
        return msg
    def add_item(self,item):
        self.useful -= item.get_size()




class bed():
    
    def __init__(self,size,name):
        self.size = size
        self.name = name

    def __str__(self):
        msg = "bed : size is:%d   name is:%s"%(self.size,self.name)
        return msg

    def get_size(self): #define a func to get the private data;
        return self.size

room_dzy = room(200,"hangzhou,xihu area","four rooms")

print(room_dzy)


bed_one = bed(8,"yijia")

print(bed_one)

room_dzy.add_item(bed_one)# arg is a class type

print(room_dzy)


