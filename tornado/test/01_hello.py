import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import url

tornado.options.define("port",default=8000,type=int, help="run server on the given port.") #这里定义了port参数，这样就可以在命令行启动的时候将改参数传入了
tornado.options.define("itcast",default=[],type=str, multiple=True, help="itcast subjects.")#这里定义了一个多参数变量，命令行传参的时候需要用,号隔开
class IndexHander(tornado.web.RequestHandler):

	def get(self):
		self.write("hello world")

class SecondHander(tornado.web.RequestHandler):
	def initialize(self,subject):
		self.subject = subject

	def get(self):
		self.write(self.subject)


if __name__ == '__main__':
	tornado.options.parse_config_file("./config") #这里定义了解析命令行参数的函数，命令行中的参数通过这个函数进行解析
	print (tornado.options.options.itcast)#这里打印出itcase参数，注意解析后的参数有两个options

	app = tornado.web.Application(
		[url(r'/',IndexHander,name="index"),

		 url(r'/cpp',SecondHander,{"subject":"c++"},name="cpp"),

		], debug=True) #这里的作用是添加路由，这里创建了一个应用app
	# app.listen(8000) #这里监听8000端口

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.bind(tornado.options.options.port)
	http_server.start(1)#0表示的是开启的进程数目和所使用的的服务器的核心数有关，当大于0的时候就是所设置的进程数目

	tornado.ioloop.IOLoop.current().start() #此处的函数才是真正运行服务器

