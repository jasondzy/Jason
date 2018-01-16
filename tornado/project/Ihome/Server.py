import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os
import models
import Handlers
from tornado.web import url, StaticFileHandler

tornado.options.define('port', default=8000, type=int, help=' runserver on given port')

 
class Application(tornado.web.Application):
	def __init__(self):
		self.mysql = models.HandleMysql()
		self.mysql.create_table()
		super(Application, self).__init__(
		[
		# url(r'^/$', Handlers.IndexHandler, name="IndexHandler"), #这里不采用get中的render返回index的原因是因为，index.html中使用了index.js脚本中的$.get等方式来和后台通讯从而获得数据，而render方式处理模板的时候会对模板进行解析处理会报错，只能通过直接加载index.html的方式
		url(r'/api/house/index', Handlers.House_index, dict(database = self.mysql), name="House_index"),
		url(r'^/register$', Handlers.House_register, dict(database = self.mysql), name="House_register"),
		url(r'^/api/piccode$', Handlers.PicCodeHandler, dict(database = self.mysql), name="PicCodeHandler"),
		url(r'^/api/smscode$', Handlers.Smscode, dict(database = self.mysql), name="Smscode"),
		url(r'^/api/register$', Handlers.Register_verity, dict(database = self.mysql), name="Register_verity"),
		url(r'/(.*)',StaticFileHandler, {"path":os.path.join(os.path.dirname(__file__),"template"), "default_filename":"index.html"}, name="index"),
		],
		debug = True, 
		static_path = os.path.join(os.path.dirname(__file__), 'static'),
		template_path = os.path.join(os.path.dirname(__file__), 'template'),

		)


def main():
	tornado.options.parse_command_line()

	app = Application()

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8000) 

	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()