import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os
import url

tornado.options.define('port', default=8000, type=int, help=' runserver on given port')



def main():
	tornado.options.parse_command_line()
	current_path = os.path.dirname(__file__)

	app = tornado.web.Application(
		url.urls,
		debug = True,
		static_path = os.path.join(current_path, 'static'),
		)

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(8000) 

	tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
	main()