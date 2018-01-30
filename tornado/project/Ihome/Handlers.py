import tornado.web
import json
import models
from hashlib import sha1
import base64, uuid
from utils.captcha.captcha import captcha
from utils.commons import required_login

Image_id = "1111"
class BaseHandler(tornado.web.RequestHandler):
	def initialize(self, database, database_redis):
		self.database = database
		self.redis = database_redis

	def prepare(self):
		"""预解析json数据"""  #这里判断请求的类型是否是json类型
		self.xsrf_token
		# print(self.request.body)
		if self.request.headers.get("Content-Type", "").startswith("application/json"):
			self.json_args = json.loads(self.request.body.decode("utf-8"))  #对body中的json数据进行解析成字典的类型，lods是解析，dumps是翻译成json类
		else:
			self.json_args = {}

	def get_current_user(self):
		session_id = self.get_secure_cookie('session_id')
		if session_id == None:
			print(" not login!!!")
			return None
		value = self.redis.get_value(session_id)
		if value == None or len(value) == 0:
			print("not login!!!")
			return None

		return value

###################这里实现一个主页处理函数#########################################
class House_index(BaseHandler):
	def get(self):
		print('================================')
		sql = "select hi_house_id,hi_title,hi_index_image_url from ih_house_info order by hi_order_count desc limit 3;"
		result = self.database.get_values_from_mysql(sql)
		print(result)

		houses = []
		for value in result:
			houses.append({'house_id':value[0], 'img_url':value[2], 'title':value[1]})


		sql = " select * from ih_area_info"
		result = self.database.get_values_from_mysql(sql)
		# print(result)

		area = []
		for value in result:
			area.append({'area_id':value[0], 'name':value[1]})
		# print(area)

		json_houses = json.dumps(houses) #注意在tornado中self.write(xx)中的xx要是字典型的数据，这样tornado就会自动将xx转换为json数据传输
		json_areas = json.dumps(area) #注意，字典型数据xx中的子元素的值若是个字典或数组等组合类型的值。需要将子元素的值转换为json型数据包裹在外层自动类型变量中进行传输
		resp = '{"errcode":"0", "errmsg":"OK", "houses":%s, "areas":%s}' % (json_houses, json_areas)
		self.write(resp) #这里就是返回数据，自动将字典类型变量转换为json数据类型
		self.set_header("Content-Type", "application/json; charset=UTF-8") #设置传输类型的头部为 json类型，若是不设置可能会出错
		# self.write('ok') #以上的这么多设置主要是针对$ajax类型的数据请求，因为javascript擅长解析的是json类型数据

#############这里实现的是一个检查用户是否登录的功能 ########
class Check_login(BaseHandler):
	def get(self):
		session_id = self.get_secure_cookie('session_id')
		user_data = {}
		if session_id == None:
			print("session_id cookie do not exist")
			data = {
				"errcode":1,
				"data":None,
			}
		else:
			value = self.redis.get_value(session_id)
			sql = 'select up_name from ih_user_profile where up_mobile="%s" '%value.decode("utf-8")
			result = self.database.get_values_from_mysql(sql)
			if result == None or len(result)==0:
				print("session_id do not exist in redis")
				data = {
				"errcode":1,
				"data":None,
				}
			else:
				print(" login user:", value)
				user_data['name'] = result
				# user_data = json.dumps(user_data)
				data = {
					"errcode":0,
					"data":user_data,
				}

		self.write(data)
		self.set_header("Content-Type", "application/json; charset=UTF-8")

############# 这里实现的是注册的主页面显示功能 ############

class House_register(BaseHandler):
	def get(self):
		print("register============")
		self.render('register.html')

##############验证码功能#################################

class PicCodeHandler(BaseHandler): #前端的img中的src是一个GET方式的请求
	"""图片验证码"""
	def get(self):
		global Image_id #这里使用的是Image_id这个全局变量来传递图片验证码数据
		"""获取图片验证码"""
		pre_code_id = self.get_argument("pre", "")
		cur_code_id = self.get_argument("cur")
		# 生成图片验证码
		name, text, pic = captcha.generate_captcha() #这里使用了外接包，导入的captcha是对象，生成了图片信息
		# print(text) #这里的text是真正的数据，是用来判断用户传入过来的验证是否是正确的
		Image_id = text
		#这里的pic是直接生成的图片二进制码，所以接下来可以直接通过self.write往html写入数据
		self.set_header("Content-Type", "image/jpg")
		self.write(pic) #这里的作用是将图片的二进制数据写入到前端系统


###############手机验证码功能#################################
class Smscode(BaseHandler):
	def post(self):
		global Image_id
		mobile = self.json_args.get('mobile')  #这里的json_args是个字典类型，存放的是json类型的数据，ajax中的json数据的获取是通过self.request.body()中获取的
		imageCode = self.json_args.get('piccode') #这里的字典中的值是在BaseHandler中进行预解析的
		imageCodeId = self.json_args.get('piccode_id')
		# print("image_id===============")
		# print(Image_id)
		if imageCode == Image_id:
			print("iamge code true",imageCode)
			data = {
				"errcode":0,
				"errmsg":'ok',
			}
		else:
			data = {
				"errcode":1,
				"errmsg":"imagecode wrong"
			}
		self.write(data)
		self.set_header("Content-Type", "application/json; charset=UTF-8")

################注册验证功能################################
class Register_verity(BaseHandler):
	def post(self):
		mobile = self.json_args.get('mobile')
		phoneCode = self.json_args.get('phonecode')
		passwd = self.json_args.get('password')
		passwd2 = self.json_args.get('password2')
		# print(mobile,phoneCode,passwd,passwd2)

		################这里用来判断手机号是否已经注册了###########
		sql = "select up_name from ih_user_profile where up_mobile='%s'"%mobile
		result = self.database.get_values_from_mysql(sql)
		print("#############",result)
		if len(result) != 0:
			print("mobile number existed")
			data = {
			'errcode':'1',
			'errmsg':'mobile number existed'
			}
			self.write(data)
			self.set_header("Content-Type", "application/json; charset=UTF-8")
		################这里判断两次输入的密码是否一致###########
		elif passwd != passwd2:
			data = {  
			'errcode':'1',
			'errmsg':'password mismatch'
			}
			self.write(data)
			self.set_header("Content-Type", "application/json; charset=UTF-8")
		else:
		#############这里对密码进行加密处理#####################
			s1 = sha1()
			s1.update(passwd.encode("utf-8"))
			password = s1.hexdigest()
		
		#############这里暂时留作空白作为验证手机的验证码是否正确####
			#if 

		#######将手机号和密码存入数据库中去####################
			sql = "insert into ih_user_profile(up_name,up_mobile,up_passwd) values('%s','%s','%s')"%(mobile, mobile, password)
			print(sql)
			self.database.insert_into_tbl(sql)

		####### 将注册成功后的用户写入session 机制 ############
		#这里生成一个独一无二的session_id号
			session_id = str(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))
			self.set_secure_cookie("session_id", session_id, expires_days=1)
			self.redis.set_value(session_id, str(mobile))
			self.redis.set_expire(session_id, 360)
		###########返回状态码给到js端##########################
			data = {
				'errcode':'0',
				'errmsg':'ok'
			}

			self.write(data)
			self.set_header("Content-Type", "application/json; charset=UTF-8")


###############################登陆处理功能###################################
class Login_verity(BaseHandler):
	def post(self):
		mobile = self.json_args.get('mobile')
		passwd = self.json_args.get('password')

		################# 从mysql数据库中查询是否存在该手机号 ###########
		sql = "select up_passwd from ih_user_profile where up_mobile=%s"%mobile
		result = self.database.get_values_from_mysql(sql)
		# print("result=====",result)
		if result == None or len(result) == 0:
			print(" mobile dot exist please register")
			data = {
				'errcode':'1',
				'errmsg':'do not exist'
			}
			self.write(data)
			self.set_header("Content-Type", "application/json; charset=UTF-8")
		else:
			############ 对输入的密码进行加密后和数据库中的密码进行比较 ####
			s1 = sha1()
			s1.update(passwd.encode("utf-8"))
			password = s1.hexdigest()
			############# end #########################################
			# print("password===== result======",password,result[0])

			if password != result[0][0]:
				print("password wrong")
				data = {
				'errcode':'1',
				'errmsg':'password wrong'
				}
				self.write(data)
				self.set_header("Content-Type", "application/json; charset=UTF-8")
			else:
				print(" login sucess")
				#############这里设置 session 功能######################
				session_id = str(base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes))
				self.set_secure_cookie("session_id", session_id, expires_days=1)
				self.redis.set_value(session_id, str(mobile))
				self.redis.set_expire(session_id, 360)
				############# end #####################################
				data = {
				'errcode':'0',
				'errmsg':'login sucess'
				}
				self.write(data)
				self.set_header("Content-Type", "application/json; charset=UTF-8")

#############################个人信息处理################################

class Personal_info(BaseHandler):
	@required_login
	def get(self):
		session_id = self.get_secure_cookie("session_id")
		# print("session_id===",session_id)
		mobile = self.redis.get_value(session_id).decode("utf-8")
		# print("mobile=====",mobile)
		sql = "select up_name,up_avatar from ih_user_profile where up_mobile=%s"%mobile
		result = self.database.get_values_from_mysql(sql)
		# print("name====",result)
		if result == None or len(result) == 0: 
			print("can not search name")
			self.write(dict(errcode="4101", errmsg="用户未登录"))

		print("result[0][1]======", result[0][1])
		if result[0][1] == None:
			image_path = "/static/images/landlord01.jpg"
		else:
			image_path = result[0][1]

		user_data = {
			"name":result[0][0],
			"mobile":mobile,
			"avatar":image_path
		}

		data = {
			"errcode":"0",
			"data":user_data,
		}

		self.write(data)
		self.set_header("Content-Type", "application/json; charset=UTF-8")

##########################处理用户修改用户名#########################
class Personal_name(BaseHandler):
	def post(self):
		user_name = self.json_args.get('name')
		# print('user_name====',user_name)
		################# 获取当前登录的用户id ######################
		session_id = self.get_secure_cookie("session_id")
		# print("session_id===",session_id)
		mobile = self.redis.get_value(session_id).decode("utf-8")
		sql = 'update ih_user_profile set up_name="%s" where up_mobile="%s" '%(user_name, mobile)
		# print(sql)
		result = self.database.update_tbl(sql)
		if result != True:
			print(" update sql failed ")
			return 0
		else:
			print(" update sql sucess ")

			data = {
				"errcode":"0",
			}

			self.write(data)
			self.set_header("Content-Type", "application/json; charset=UTF-8")

######################### 这里用来处理用户上传的头像信息 #############
#####---这里使用的技术栈是直接保存在了服务器/static/images/personal_images中
#####---这里可使用七牛技术存储到远程服务器上(由于账号实名问题，七牛账号暂时不可用)
class Personal_img(BaseHandler):
	def post(self):
		################# 获取当前登录的用户id ######################
		session_id = self.get_secure_cookie("session_id")
		# print("session_id===",session_id)
		mobile = self.redis.get_value(session_id).decode("utf-8")
		print("test_test======")
		files = self.request.files
		image_file = files.get("avatar")
		if image_file:
			file_name = image_file[0]["filename"]
			# print("filename=====", file_name)
			image = image_file[0]["body"]

			file_path = './static/images/personal_images/' + mobile# + "." + ".".join(file_name.split(".")[1:])
			file = open(file_path, 'wb')
			file.write(image)

			file.close()

			data = {
				'errcode':'0',
				'data':file_path,
			}

			############## 这里需要添加将图片路径保存在mysql的功能#####
			sql = 'update ih_user_profile set up_avatar="%s" where up_mobile="%s" '%(file_path, mobile)
			result = self.database.update_tbl(sql)
			if result != True:
				print(" update sql failed ")
				return 0

		else:
			data = {
				'errcode':'4001',
				'data':"/static/images/landlord01.jpg",
			}

		self.write(data)
		self.set_header("Content-Type", "application/json; charset=UTF-8")

######################## 房屋信息显示 #######################
class House_info(BaseHandler):
	def get(self):
		house_id = self.get_query_argument('house_id')
		# print(house_id)

