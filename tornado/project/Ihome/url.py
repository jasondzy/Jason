from tornado.web import url, StaticFileHandler
import Handlers
import os

urls = [
		# url(r'^/$', Handlers.IndexHandler, name="IndexHandler"),
		url(r'/api/house/index', Handlers.House_index, name="House_index"),
		url(r'/(.*)',StaticFileHandler, {"path":os.path.join(os.path.dirname(__file__),"template"), "default_filename":"index.html"}, name="index"),
	]