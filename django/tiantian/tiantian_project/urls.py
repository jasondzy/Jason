from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$',views.register,name="register"),
    url(r'^register_handle/$',views.register_handle,name="register_handle"),
    url(r'^check_username/$',views.check_username,name="check_username"),
    url(r'^login/$',views.login,name="login"),
    url(r'^login_handle/$',views.login_handle,name="login_handle"),
    url(r'^user_center_info/$',views.user_center_info,name="user_center_info"),
    url(r'^user_center_info_register/$',views.user_center_info_register,name="user_center_info_register"),
    url(r'^user_center_info_register_handle$',views.user_center_info_register_handle,name
    	="user_center_info_register_handle"),
    url(r'^user_center_order$',views.user_center_order,name="user_center_order"),
]
