from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name="index"),
	url(r'^upload/',views.upload,name="upload"),
	url(r'^pages/',views.pages,name="pages"),
	url(r'^book_index/',views.book_index, name="book_index"),
	url(r'^ajax_get/',views.ajax_get,name="ajax_get"),
	url(r'^get_bookinfo/',views.get_bookinfo,name="get_bookinfo"),
	url(r'^editor/',views.editor,name="editor"),
	url(r'^editor_handle',views.editor_handle,name="editor_handle"),
]