from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'dd_app'
urlpatterns = [
	
	#url('^', include('django.contrib.auth.urls')),
	url(r'^$', views.index, name='index'),
	url(r'^login/', auth_views.login, name="login"),
	url(r'^logout/', views.logout_user, name="logout"),
	url(r'^register/$', views.register, name='register'),

	url(r'^mycrews/$', views.mycrews, name='mycrews'), # list of crews CRUD Crews
	url(r'^mycrews/create/$', views.create_crew, name='create_crew'), # create crew

	url(r'^crew/(?P<crew_id>[0-9]+)/$', views.crew, name='crew'), #lists of stories and creat new story CRUD Stories
	url(r'^story/(?P<story_id>[0-9]+)/$', views.story, name='story'), #lists of stories and creat new story CRUD Stories
	#url(r'^crew/(?P<crew_id>[0-9]+)/new_story/$', views.vote, name='vote'), # create story
	#url(r'^crew/(?P<crew_id>[0-9]+)/(?P<story_id>[0-9]+)/$', views.vote, name='vote') # the story itself



]