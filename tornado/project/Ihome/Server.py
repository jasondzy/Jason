import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os
import url
import Settings
import models

tornado.options.define('port', default=8000, type=int, help=' runserver on given port')


class Application(tornado.web.Application):
	def __init__(self, *args, **kwargs):
		self.mysql = models.HandleMysql()
		self.mysql.create_table()
		super(Application, self).__init__(*args, **kwargs)


def main():
	tornado.options.parse_command_line()

	app = Application(
		url.urls,
		**Settings.settings
		)

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8000) 

	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()