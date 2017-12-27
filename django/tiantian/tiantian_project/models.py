from django.db import models

# Create your models here.

class UserInfo(models.Model):
	user_name = models.CharField(max_length=20)
	user_passwd = models.CharField(max_length=40)
	user_mail = models.CharField(max_length=30)

	def __str__(self):
		return self.user_name



class User_address_info(models.Model):
	address = models.CharField(max_length=100)
	tel_num = models.CharField(max_length=12)
	user = models.ForeignKey(UserInfo)
	
	def __str__(self):
		return str(self.user)