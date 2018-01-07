import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.web import url


tornado.options.define("port", default=8000, type=int, help="runserver on given port")

class IndexHander(tornado.web.RequestHandler):

	def post(self):

		para_query = self.get_query_arguments('a') #这里的作用是在url中获取a的参数值，获取的是一个列表，存放的是a的所有值
		para_body = self.get_body_arguments('b')
		print('body',para_body)
		print('query',para_query)
		self.write("ok")

class SecondHander(tornado.web.RequestHandler):
	def post(self):
		print(self.request.method)
		print(self.request.uri)
		print(self.request.host)
		print(self.request.headers)

class ThirdHander(tornado.web.RequestHandler):
	def post(self):
		files = self.request.files #获取request中所有的files类型的文件，这些文件是用字典的形式组织的
		img = files.get('image1') #从这些字典类型数据中获取指定image图片信息
		print(img[0]['filename']) #获取的img信息也是一个列表信息，即相同名字image1可以传入多张file文件，列表中的值又是字典类型的数据

		with open('/home/ubuntu/user_jason/temp/image.jpg','wb') as f: #将从request中获取的图片信息写入到文件中去
			f.write(img[0]['body']) #body中存放的就是image1的信息，这里将image1中的信息写入到新创建的文件中
		self.write('ok')

class FiveHander(tornado.web.RequestHandler):
	def initialize(self,arg1):  #这里的参数接收的是路由中传递过来的字典类型参数
		print(arg1)

if __name__ == '__main__':
	tornado.options.parse_command_line()

	app = tornado.web.Application([
		url(r'/',IndexHander,name="index"),
		url(r'/second',SecondHander,name="second"),
		url(r'/third',ThirdHander,name="third"),
		url(r'/five',FiveHander,{'arg1':'111'},name="five"),
		], debug=True)

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(tornado.options.options.port)

	tornado.ioloop.IOLoop.current().start()