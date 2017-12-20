from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class BookInfo(models.Model):
	btitle = models.CharField(max_length=20)
	bpub_date = models.DateTimeField()
	bread = models.IntegerField(default=0)
	bcommet = models.IntegerField(default=0)
	isDelete = models.BooleanField(default=False)
	bcontent = HTMLField()




	def __str__(self):
		return self.btitle


class HeroInfo(models.Model):
	hname = models.CharField(max_length=20)
	hgender = models.BooleanField(default=1)
	hBook = models.ForeignKey('BookInfo')
	hcontent = models.CharField(max_length=100)
	isDelete = models.BooleanField(default=False)
	

	def __str__(self):
		return self.hname