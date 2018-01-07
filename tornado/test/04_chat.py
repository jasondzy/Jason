import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.web import url
from tornado.websocket import WebSocketHandler

import os

tornado.options.define('port', default=8000, type=int, help='runserver on given port')

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('chat.html')

class ChatHander(WebSocketHandler):
	users = set()

	def open(self):
		self.users.add(self)

		for u in self.users:
			u.write_message("%s 进入聊天室" % self.request.remote_ip)

	def on_message(self,message):
		for u in self.users:
			u.write_message(" %s发送消息:%s" %(self.request.remote_ip, message))

	def on_close(self):
		users.remove(self)
		for u in self.users:
			u.write_message("%s退出聊天室"% self.request.remote_ip)

	def check_origin(self, origin):
		return True


class Application(tornado.web.Application):
	def __init__(self):
		handler = [
			url(r'^/$', IndexHandler, name="IndexHandler"),
			url(r'^/chat$', ChatHander, name="ChatHander"),
		]

		settings = dict(
			debug= True,
			static_path = os.path.join(current_path, 'static'),
			template_path = os.path.join(current_path, 'templates'),
			)

		super(Application, self).__init__(handler, **settings)                                                 


if __name__ == '__main__':

	tornado.options.parse_command_line()
	current_path = os.path.dirname(__file__)

	app = Application()

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(tornado.options.options.port)

	tornado.ioloop.IOLoop.current().start()

