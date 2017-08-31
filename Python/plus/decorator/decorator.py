def func(function): #这里的func定义的是一个闭包，这里的参数是function
	print('Tis is a decorate1---')
	def func_inner(*args,**kwargs):#这里的func_inner是闭包中的内嵌函数，最终闭包的返回值就是这个内嵌函数的地址
		print('----func_inner----')
		function(*args,**kwargs)#这里的function()的作用是执行函数function，从这里可以验证闭包的参数是一个函数的地址

	return func_inner#这里是闭包的返回值，该返回值是函数的地址


def func2(function):
	print('This is a decorate2')
	def func_inner(*args,**kwargs):#这里对内嵌函数定义了不定参数，注意这里的内嵌函数就是将来调用的函数test()，所以要实现test(x,y...)带入参数，那么这里的内嵌函数必须定义成带参数的形式
		print('-----func_inner2---')
		function(*args,**kwargs)#这里的函数调用的是定义的test函数，所以这里的参数要使用内嵌函数中的参数，可以不一致。因为最终所有的参数都是通过装饰后的test传递进来的。
	return func_inner



@func #这里的作用是试用装饰器func，传入的参数就是下一行中的函数地址，即test
@func2 #通过执行这个py脚本，注意管着两个连续的装饰器的执行顺序是如何的
def test(a):
	print('----test---a=%d---'%a)
@func#通过对改脚本的输出log可知，装饰器的执行是在所有函数之前的，即这三个装饰器的最先打印处This is a decoratex，其中decorate2最先打印出来
def test1(a):
	print('----test1-- a=%d--'%a)

test(0)#调用test函数，注意这里的test函数已经不再是上边定义了的test函数，而是经过装饰器装饰了的函数
test1(1)

#@func的作用就是对函数进行装饰，流程原理如下：
#@func => test = func(test) => func_inner()
#即最后的test的地址为func_inner的地址，而在func_inner中有调用test所以实现了对test的封装