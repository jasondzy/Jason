from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index,name="index"),
    url(r'^register/$',views.register,name="register"),
    url(r'^register_handle/$',views.register_handle,name="register_handle"),
    url(r'^check_username/$',views.check_username,name="check_username"),
    url(r'^login/$',views.login,name="login"),
    url(r'^login_handle/$',views.login_handle,name="login_handle"),
]
