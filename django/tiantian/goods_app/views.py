from django.shortcuts import render

# Create your views here.

def index(request):
	name = request.session.get('user',None)
	if name != None:
		context = {'user':name,'status':1}
	else:
		context = {'user':"",'status':0}
	return render(request,'goods/index.html',context)