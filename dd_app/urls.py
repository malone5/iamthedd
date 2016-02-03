from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views
from dd_app.views import CrewView, RegisterView, CreateCrewView, DeleteCrewMemberView, DeleteCrewView, DeleteStoryView, CreateStoryView


app_name = 'dd_app'
urlpatterns = [
	
	#url('^', include('django.contrib.auth.urls')),
	url(r'^$', views.index, name='index'),
	url(r'^login/', auth_views.login, name="login"),
	url(r'^logout/', views.logout_user, name="logout"),
	url(r'^register/$', RegisterView.as_view(), name='register'),

	url(r'^mycrews/$', views.mycrews, name='mycrews'),
	url(r'^mycrews/create/$', CreateCrewView.as_view(), name='create_crew'), 
	url(r'^mycrews/new_story/$', CreateStoryView.as_view(), name='create_story'),
	
	url(r'^crew/(?P<crew_id>[0-9]+)/$', CrewView.as_view(), name='crew'), 
	url(r'^crew/delete_member/(?P<pk>\d+)/$', DeleteCrewMemberView.as_view(), name='delete_member'),
	url(r'^crew/delete_crew/(?P<pk>\d+)/$', DeleteCrewView.as_view(), name='delete_crew'),
	url(r'^crew/delete_story/(?P<pk>\d+)/$', DeleteStoryView.as_view(), name='delete_story'),
	
	url(r'^story/(?P<story_id>[0-9]+)/$', views.story, name='story'),



]