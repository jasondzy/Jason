
import pymysql
import redis
import mysql_settings

############################ mysql 处理类######################################################
class HandleMysql(object):
	def __init__(self):

		try:
			self.db = pymysql.connect(**mysql_settings.setting)
		except Exception as e:
			raise e
		else:
			print('connect mysql sucess')
			self.cursor = self.db.cursor()

	def create_table(self):

		for sql in mysql_settings.table1:
			try:
				self.cursor.execute(sql)
			except Exception as e:
				print(' %s alerady exist, do not create it again'% (sql.split("\n")[1].split(" ")[2]))
			else:
				self.db.commit()

	def get_values_from_mysql(self, sql):
		try:
			self.cursor.execute(sql)
		except Exception as e:
			print('data did not exist')
			result = None
		else:	
			result = self.cursor.fetchall()

		return result

	def insert_into_tbl(self, sql):
		try:
			self.cursor.execute(sql)
		except Exception as e:
			raise(e)
		else:
			self.db.commit()

	def close_mysql():
		self.cursor.close()
		self.db.close()





##################################### Redis 处理类####################################################

class HandRedis(object):
	######## connect to redis#########
	def __init__(self):
		try:
			self.redisInstance = redis.StrictRedis(host="localhost", port="6379") #这里的host只能使用localhost来进行连接，因为redis没有设置密码，且redis绑定了127.0.0.1这个地址
		except Exception as e:
			print(" connect to redis failed ")
			raise(e)
		else:
			print(" connect redis sucess")

	def set_value(self, key, value):
		result = self.redisInstance.set(key, value)
		print(result)

	def get_value(self, key):
		result = self.redisInstance.get(key)
		print(result)
		return result

	def set_expire(self, key, date):
		result = self.redisInstance.expire(key, date)
		print(result)

