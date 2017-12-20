from django.db import models

# Create your models here.

class UserInfo(models.Model):
	user_name = models.CharField(max_length=20)
	user_passwd = models.CharField(max_length=40)
	user_mail = models.CharField(max_length=30)

	