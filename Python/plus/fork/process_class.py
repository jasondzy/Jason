
from multiprocessing import Process
import time


class New_process(Process):#这里定义了一个新的Newprocess类，这个类继承了Process这个父类,即可通过这个新建的类来创建一个自定义的进程
	def __init__(self,value):
		Process.__init__(self)#初始化调用了父类中的init函数，同时也加入了自定义的value的变量
		self.value = value

	def run(self):#定义了一个run方法，切记：此处定义的run方法是对父类Process中的run方法的一种重写，接下来的父类中的start方法启用的是这里重写了的run方法,这里也实现了一个不用通过tartget=xxx的方法传入一个方法
		while True:
			print('----son-----')
			time.sleep(1)

son = New_process(1)#用新创建的类来创建一个子进程,里边传入的参数并没有实际的作用
son.start()#调用start方法，这个start方法是在父类中定义的，但是这个start的方法实际调用的是run方法，由于在新建的类中重写了run方法所以最终调用的是新创建的类中的run方法

while True:
	print('---parent----')
	time.sleep(1)