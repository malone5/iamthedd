from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'dd_app'
urlpatterns = [
	
	#url('^', include('django.contrib.auth.urls')),
	url(r'^$', views.index, name='index'),
	url(r'^login/', auth_views.login, name="login"),
	url(r'^logout/', views.logout_user, name="logout"),
	#url(r'^login/$', views.login, name='login'),
	#url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register, name='register'),
	url(r'^mycrews/$', views.mycrews, name='mycrews'),


]