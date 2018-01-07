import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.httpclient
import tornado.gen
import os
import pymysql
import base64, uuid, json
from tornado.web import url, StaticFileHandler

tornado.options.define("port", default=8000, type=int, help="runserver on given port")


class IndexHander(tornado.web.RequestHandler):
	def get(self):
		context = {
			'price':398,
			'title':'宽窄巷子+160平大空间+文化保护区双地铁',
			'address':'北京市丰台区六里桥地铁',

		}
		self.render("index.html",context=context) #注意，render的第二个参数是一个关键字参数，需要传入xx=xxx类型的参数，或者**xx这里的xx是一个字典，**表示的是对字典进行解引用，解引用就是一个关键字参数
              #render的第一个参数是可变参数类型

class NewHander(tornado.web.RequestHandler):
	def get(self):
		self.render('newindex.html',text="")

	def post(self):
		text = self.get_argument('text')
		self.render('newindex.html', text=text)

class SetCookie(tornado.web.RequestHandler):
	def get(self):

		cookie = self.get_secure_cookie('count')
		count = int(cookie) +1 if cookie else 1
		self.set_secure_cookie('count', str(count))

		return self.write(str(count))

class csrf_test(tornado.web.RequestHandler):
	def get(self):
		# self.xsrf_token #这里是用来设置_xsrf这个cookie的值得，若采用模板的{% module xxX%}格式则不需要在这里进行手动测试
		self.render('csrf_test.html')
	def post(self):
		self.write("ok")

class AsyncHandler(tornado.web.RequestHandler):
	@tornado.gen.coroutine  #这里的作用相当于python3中最近加入的async模块，此模块对Python的异步操作功能紧进行了封装，用协程的方式实现，当遇到IO阻塞的时候系统能够自动切换到其他未阻塞的协程中去执行
	def get(self):
		http = tornado.httpclient.AsyncHTTPClient()
		response = yield http.fetch("http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=14.130.112.24")
				#如上的作用是当http.fetch阻塞的时候，系统自动的切换到其他协程中去执行，
		if response.error:
			self.send_error(500)
		else:
			print('type of data:',type(response.body))
			print(str(response.body))
			data = json.loads(response.body.decode('utf-8'))
			self.write('country:%s, provice:%s, city:%s'% (data['country'], data['province'],data['city']))


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			url(r'^/$', IndexHander, name="index"),
			url(r'^/cookie$', SetCookie, name="cookie"),
			url(r'^/new$', NewHander, name="newhander"),
			url(r'/csrf', csrf_test, name="csrf_test"),
			url(r'^/async$', AsyncHandler, name="AsyncHandler"),
		]

		settings = dict(
			static_path = os.path.join(current_path,"static"), #这里加入静态文件所在的位置
			template_path = os.path.join(current_path, "templates"), #这里加入模板文件的路劲
			debug = True,
			cookie_secret = str(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)), #这里使用uuid和base64共同合成了一个随机的字符串，添加到cookie从而形成secure_cookie的机制
			xsrf_cookies = True,
			)
		super(Application, self).__init__(handlers,**settings)
		try:
			self.db = pymysql.connect(
				host = '115.159.62.43',
				port = 3306,
				db = 'LoveHome',
				user = 'root',
				passwd = 'dzy',
				charset = 'utf8'
				)
		except Exception as e:
			print(e)
			print('connect to mysql fail!!')
		else:
			print('connect sucess')
			self.cursor = self.db.cursor()

	def create_table(self):
		sql = '''
			create table houses (
    			id bigint(20) unsigned not null auto_increment comment '房屋编号',
    			title varchar(64) not null default '' comment '标题',
    			position varchar(32) not null default '' comment '位置',
    			price int not null default 0,
    			score int not null default 5,
    			comments int not null default 0,
    			primary key(id)
			)ENGINE=InnoDB default charset=utf8 comment='房屋信息表'
		'''
		self.cursor.execute(sql)
		self.db.commit()

		self.cursor.close()
		self.db.close()

if __name__ == '__main__':

	current_path = os.path.dirname(__file__)

	tornado.options.parse_command_line()

	# app = tornado.web.Application([
	# 	url(r'^/$', IndexHander, name="index"),
	# 	url(r'^/new$', NewHander, name="newhander"),
	# 	# url(r'/()',StaticFileHandler, {"path":os.path.join(current_path,"static/html"), "default_filename":"index.html"}, name="index"),
	# 	#注意如上的/后必须加上正则匹配的()，因为StaticFileHandler中的get方法需要参数，不加会报错，这里实现了任意url地址访问静态文件的方式

	# 	],

	# 	static_path = os.path.join(current_path,"static"), #这里加入静态文件所在的位置
	# 	template_path = os.path.join(current_path, "templates"), #这里加入模板文件的路劲

	# 	 debug=True)


	app = Application()
	# app.create_table()  #这里创建一个表
	# app.cursor.execute('select * from test_tbl')
	# result = app.cursor.fetchone()
	# print(result) 

	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(tornado.options.options.port)

	tornado.ioloop.IOLoop.current().start()

	

