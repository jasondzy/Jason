import tornado.web
import json

class BaseHandler(tornado.web.RequestHandler):
	pass

class IndexHandler(BaseHandler):
	def get(self):
		print('*************************************')
		self.render('index.html')

class House_index(BaseHandler):
	def get(self):
		print('================================')
		houses = [
		{
			'house_id':0,
			'img_url':"/static/images/home01.jpg",
			'title':'111111',
		},
		{
			'house_id':1,
			'img_url':"/static/images/home02.jpg",
			'title':'222222',
		},
		{
			'house_id':2,
			'img_url':"/static/images/home03.jpg",
			'title':'333333333',
		}

		]

		area = [
			{
				'area_id':0,
				'name':'1111'
			}


		]

		json_houses = json.dumps(houses)
		json_areas = json.dumps(area)
		resp = '{"errcode":"0", "errmsg":"OK", "houses":%s, "areas":%s}' % (json_houses, json_areas)
		self.write(resp)
		self.set_header("Content-Type", "application/json; charset=UTF-8")
		# self.write('ok')