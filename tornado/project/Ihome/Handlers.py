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
		# print("session_id======",session_id)
		user_data = {}
		if session_id == None:
			print("session_id cookie do not exist")
			data = {
				"errcode":1,
				"data":None,
			}
		else:
			value = self.redis.get_value(session_id)
			if value == None:
				data = {
				"errcode":1,
				"data":None,
				}
			else:
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
		#这里将存在cookie中的session_id存放到redis中，这样就可以通过cookie来在redis中进行数据查询	
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
			print('password=====',password)
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
				self.redis.set_expire(session_id, 3600)
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

		# print("result[0][1]======", result[0][1])
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
	@required_login
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
	@required_login
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
	@required_login
	def get(self):
		house_id = self.get_query_argument('house_id')
		print(house_id)
		########### 获取房屋信息 #########################
		session_id = self.get_secure_cookie("session_id")
		mobile = self.redis.get_value(session_id).decode("utf-8")

		# 校验参数，判断传入的house_id是否正确
		if not house_id:
			return self.write(dict(errcode=RET.PARAMERR, errmsg="缺少参数"))

		# 这里可以添加从redis缓存中获取这些房屋信息，这样就避免了进行多次查询数据的操作
		# 这里以待加入功能
		# TODO

		# 查询数据库

		# 查询房屋基本信息
		sql = "select hi_title,hi_price,hi_address,hi_room_count,hi_acreage,hi_house_unit,hi_capacity,hi_beds," \
			  "hi_deposit,hi_min_days,hi_max_days,up_name,up_avatar,hi_user_id " \
			  "from ih_house_info inner join ih_user_profile on hi_user_id=up_user_id where hi_house_id=%s"%house_id

		ret = self.database.get_values_from_mysql(sql)
		# print("result=======", ret)
		# 用户查询的可能是不存在的房屋id, 此时ret为None
		if not ret:
			return self.write(dict(errcode=RET.NODATA, errmsg="查无此房"))

		data = {
			"hid":house_id,
			"user_id":ret[0][13],
			"title":ret[0][0],
			"price":ret[0][1],
			"address":ret[0][2],
			"room_count":ret[0][3],
			"acreage":ret[0][4],
			"unit":ret[0][5],
			"capacity":ret[0][6],
			"beds":ret[0][7],
			"deposit":ret[0][8],
			"min_days":ret[0][9],
			"max_days":ret[0][10],
			"user_name":ret[0][11],
			"user_avatar":ret[0][12]
		}

		# print("data===========",data)

		# 查询房屋的图片信息
		sql = "select hi_url from ih_house_image where hi_house_id=%s"%house_id
		ret = self.database.get_values_from_mysql(sql)
		# print("image=============",ret)

		# 如果查询到的图片
		images = []
		if ret:
			for image in ret:
				images.append(image[0])
		data["images"] = images

		# 查询房屋的基本设施
		sql = "select hf_facility_id from ih_house_facility where hf_house_id=%s"%house_id
		ret = self.database.get_values_from_mysql(sql)

		# 如果查询到设施
		facilities = []
		if ret:
			for facility in ret:
				facilities.append(facility[0])
		data["facilities"] = facilities

		# 查询评论信息
		sql = "select oi_comment,up_name,oi_utime,up_mobile from ih_order_info inner join ih_user_profile " \
			  "on oi_user_id=up_user_id where oi_house_id=%s and oi_status=4 and oi_comment is not null"%house_id

		ret = self.database.get_values_from_mysql(sql)
		comments = []
		if ret:
			for comment in ret:
				comments.append(dict(
					user_name = comment[1] if comment[1] != comment[3] else "匿名用户",
					content = comment[0],
					ctime = comment[2].strftime("%Y-%m-%d %H:%M:%S")
				))
		data["comments"] = comments

		# 存入到redis中
		json_data = json.dumps(data)

		## 可以在此处将上边查询到的这么多数据存储到redis中，这样下次查询的时候就能加快查询步骤
		#TODO

		resp = '{"errcode":"0", "errmsg":"OK", "data":%s, "user_id":%s}' % (json_data, mobile)
		# self.write(dict(errcode=RET.OK, errmsg="OK", data=data))
		self.write(resp)
		self.set_header("Content-Type", "application/json; charset=UTF-8")


############## 获取预定信息  /api/house/info ########################################
class House_reserve(BaseHandler):
	def post(self):
		house_id = self.json_args.get('house_id')
		start_date = self.json_args.get('start_date')
		end_date = self.json_args.get('end_date')
		print('====',house_id,start_date,end_date)

		sql = ' select oi_begin_date,oi_end_date from ih_order_info where oi_house_id=%s'%house_id
		ret = self.database.get_values_from_mysql(sql)
		if not ret:
			print(' query order info error')
			data = {
				'errcode':'4101',
			}
		############ 这里添加对 html中传来的事件信息，和该house在order数据库中存在的时间内信息进行比较来判断所选择的时间段是否可预定

		data = {
			'errcode':'0'
		}
		self.write(data)
		self.set_header('Content-Type', 'application/json; charset=UTF-8')

############### 处理显示订单信息 ##########################################
class Show_order(BaseHandler):
	@required_login
	def get(self):
		session_id = self.get_secure_cookie("session_id")
		# print("session_id===",session_id)
		mobile = self.redis.get_value(session_id).decode("utf-8")

		sql = ' select up_user_id from ih_user_profile where up_mobile=%s'%mobile
		ret = self.database.get_values_from_mysql(sql)
		if not ret:
			print('user_id doesr not exist')
			data = {
				'errcode':'1',
			}
		user_id = ret[0][0]
		print('user_id======',user_id)

		# 用户的身份，用户想要查询作为房客下的单，还是想要查询作为房东 被人下的单
		role = self.get_query_argument("role", "")
		try:
			# 查询房东订单
			if "landlord" == role:
				sql = 'select oi_order_id,hi_title,hi_index_image_url,oi_begin_date,oi_end_date,oi_ctime,oi_days,oi_amount,oi_status,oi_comment from ih_order_info inner join ih_house_infoon oi_house_id=hi_house_id where hi_user_id=%s order by oi_ctime desc'%user_id
				ret = self.database.get_values_from_mysql(sql)
				if not ret:
					print(' query order info fail')
					data = {
						'errcode':'1',
					}

			else:
				sql = 'select oi_order_id,hi_title,hi_index_image_url,oi_begin_date,oi_end_date,oi_ctime,oi_days,oi_amount,oi_status,oi_comment from ih_order_info inner join ih_house_info on oi_house_id=hi_house_id where oi_user_id=%s order by oi_ctime desc'%user_id
				ret = self.database.get_values_from_mysql(sql)
				if not ret:
					print(' query order info fail')
					data = {
						'errcode':'1',
					}

		except Exception as e:
			logging.error(e)
			return self.write({"errcode":'1', "errmsg":"get data error"})
		orders = []
		if ret:
			for l in ret[0]:
				order = {
					"order_id":l[0],
					"title":l[1],
					"img_url":l[2],
					"start_date":l[3].strftime("%Y-%m-%d"),
					"end_date":l[4].strftime("%Y-%m-%d"),
					"ctime":l[5].strftime("%Y-%m-%d"),
					"days":l[6],
					"amount":l[7],
					"status":l[8],
					"comment":l[9] if l[9] else ""
				}
				orders.append(order)
		self.write({"errcode":'0', "errmsg":"OK", "orders":orders})


