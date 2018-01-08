from tornado.web import url
import Handlers

urls = [
		url(r'^/$', Handlers.IndexHandler, name="IndexHandler"),
	]