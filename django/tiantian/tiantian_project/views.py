from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from .models import *
from hashlib import sha1
import re

# Create your views here.
def index(request):
	name = request.session.get('user',None)
	print(name)
	return render(request,'tiantian/index.html')

def register(request):
	return render(request,'tiantian/register.html')

def register_handle(request):
	#获取用户提交的信息
	name = request.POST['user_name']
	pwd = request.POST['pwd']
	cpwd = request.POST['cpwd']
	email = request.POST['email']

	#判断密码是否相同
	if pwd != cpwd:
		return redirect(reverse('tiantian:register'))

	#判断邮箱是否正确
	if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email) == None:
		return redirect(reverse('tiantian:register'))

	# 密码加密：
	s1 = sha1()
	s1.update(pwd.encode("utf-8"))
	passwd = s1.hexdigest()
	# 加密 end

	user = UserInfo()
	user.user_name = name
	user.user_passwd = passwd
	user.user_mail = email
	user.save()

	return redirect(reverse('tiantian:login'))

	# return render(request,)

def check_username(request):
	print('test')
	name = request.GET['name']
	print(name)
	count = UserInfo.objects.filter(user_name=name).count() #这里使用的是count的方式来计算过滤出来的值有多少个
	print(count)                     #能使用count的原因是过滤出来的是一个数组
	if count:
		print('1')
		return JsonResponse({'status':1})
	else:
		print('0')
		return JsonResponse({'status':0})

def login(request):
	return render(request,'tiantian/login.html')

def login_handle(request):
	name = request.POST['username']
	pwd = request.POST['pwd']

	#获取密码的加密格式字符串
	s1 = sha1()
	s1.update(pwd.encode("utf-8"))
	passwd = s1.hexdigest()	
	# 加密 end

	#比较用户名
	count = UserInfo.objects.filter(user_name=name).count()
	if count == 0:
		return redirect(reverse('tiantian:login'))
	else:
		user = UserInfo.objects.get(user_name=name)
		if user.user_passwd != passwd:
			status = 0
			return redirect(reverse('tiantian:login'))
		else:
			status = 1
			request.session['user']=name
			request.session.set_expiry(300)
			return redirect(reverse('tiantian:index'))







