from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .models import *
from django.core.paginator import Paginator
import json
# Create your views here.

def index(request):
    return render(request,'booktest/index.html')
    # return HttpResponse('ok')


def upload(request):

    if request.method == 'POST':
        picture = request.FILES['picture']
        fname = '%s/cars/%s'%(settings.MEDIA_ROOT, picture.name)
        # return HttpResponse(settings.MEDIA_ROOT)
        with open(fname,'wb') as pic:
            for c in picture.chunks():
                pic.write(c)
        return HttpResponse('ok')
    else:
        return HttpResponse('error')
def my_custom_page_not_found_view(request):
    return HttpResponse('fail 404 fail')

def pages(request,id):
    if id == '':
        id = '1'
    list = HeroInfo.objects.all()
    paginator = Paginator(list,5)
    page = paginator.page(int(id))
    context = {'page':page}

    return render(request,'booktest/pages.html',context)

def book_index(request):
    return render(request,'booktest/book_index.html')

def ajax_get(request):
    # print('hello')
    book_list = BookInfo.objects.all()
    # print(book_list)
    # return JsonResponse({'data':book_list}) #这样返回数据会报错
    l = []
    for list in book_list:
        l.append((list.id,list.btitle)) #这里必须要将获得的book_list进行遍历，取出元素放在一个数组中才行，否则会报错
    return JsonResponse({'data':l}) #具体为什么这样的原因还有待解析

def get_bookinfo(request):
    print('test')
    id = request.GET['id'] #这里使用的是ajax的方式进行数据的传递
    print(id)
    list=HeroInfo.objects.filter(hBook_id=id)#这里的filter返回的是一个查询集，并不是一个对象，而是一个对象集合
    print(list)
    hero_list = []
    for i in list:
        hero_list.append((i.id,i.hname))
    return JsonResponse({'data':hero_list})

#富文本编辑器
def editor(request):
    data = BookInfo.objects.all()
    list = []
    for l in data:
        list.append([l.id,l.btitle])
    print(list)
    context = {'data':list}
    return render(request,'booktest/editor.html',context)

def editor_handle(request):
    html = request.POST['hcontent'] #此处获取的是大文本提交的内容
    id = request.POST['select'] #此处获取的是要提交的id号
    print('id:',id)
    print(html)
    book = BookInfo.objects.get(pk=id) #注意filter方法返回的是一个查询集合，是一个集合，get返回的是一个对象
    print(book.btitle)
    book.bcontent = html
    book.save()
    return HttpResponse('ok')