import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os
import models
import Handlers
import base64, uuid
from tornado.web import url, StaticFileHandler

tornado.options.define('port', default=8000, type=int, help=' runserver on given port')

 
class Application(tornado.web.Application):
	def __init__(self):
		################# create mysql object #######
		self.mysql = models.HandleMysql()
		self.mysql.create_table()
		################# end #######################
		################# create redis object #######
		self.redis = models.HandRedis()
		################# end #######################

		################# 进行域名地址的映射 ##########
		super(Application, self).__init__(
		[
		# url(r'^/$', Handlers.IndexHandler, name="IndexHandler"), #这里不采用get中的render返回index的原因是因为，index.html中使用了index.js脚本中的$.get等方式来和后台通讯从而获得数据，而render方式处理模板的时候会对模板进行解析处理会报错，只能通过直接加载index.html的方式
		url(r'/api/house/index', Handlers.House_index, dict(database = self.mysql, database_redis = self.redis), name="House_index"),
		url(r'^/register$', Handlers.House_register, dict(database = self.mysql, database_redis = self.redis), name="House_register"),
		url(r'^/api/piccode$', Handlers.PicCodeHandler, dict(database = self.mysql, database_redis = self.redis), name="PicCodeHandler"),
		url(r'^/api/smscode$', Handlers.Smscode, dict(database = self.mysql, database_redis = self.redis), name="Smscode"),
		url(r'^/api/register$', Handlers.Register_verity, dict(database = self.mysql, database_redis = self.redis), name="Register_verity"),
		url(r'^/api/login$', Handlers.Login_verity, dict(database = self.mysql, database_redis = self.redis), name="database = self.mysql"),
		url(r'/(.*)',StaticFileHandler, {"path":os.path.join(os.path.dirname(__file__),"template"), "default_filename":"index.html"}, name="index"),
		],
		################# end ########################
		debug = True, 
		static_path = os.path.join(os.path.dirname(__file__), 'static'),
		template_path = os.path.join(os.path.dirname(__file__), 'template'),
		cookie_secret = str(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)), #这里使用uuid和base64共同合成了一个随机的字符串，添加到cookie从而形成secure_cookie的机制
		xsrf_cookies = True,
		)


def main():
	tornado.options.parse_command_line()

	app = Application()

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8000) 

	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()