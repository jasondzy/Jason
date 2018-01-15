
import pymysql
import mysql_settings

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
		self.cursor.execute(sql)
		result = self.cursor.fetchall()

		return result

	def close_mysql():
		self.cursor.close()
		self.db.close()
