from django.urls import re_path 
from django.contrib.auth import views as auth_views


from . import views
from dd_app.views import CrewView, RegisterView, CreateCrewView, DeleteCrewMemberView, DeleteCrewView, DeleteStoryView, CreateStoryView


app_name = 'dd_app'
urlpatterns = [
	
	#re_path('^', include('django.contrib.auth.urls')),
	re_path(r'^$', views.index, name='index'),
	re_path(r'^login/', auth_views.LoginView.as_view(), name="login"),
	re_path(r'^logout/', views.logout_user, name="logout"),
	re_path(r'^register/$', RegisterView.as_view(), name='register'),

	re_path(r'^mycrews/$', views.mycrews, name='mycrews'),
	re_path(r'^mycrews/create/$', CreateCrewView.as_view(), name='create_crew'), 
	re_path(r'^mycrews/new_story/$', CreateStoryView.as_view(), name='create_story'),
	
	re_path(r'^crew/(?P<crew_id>[0-9]+)/$', CrewView.as_view(), name='crew'), 
	re_path(r'^crew/delete_member/(?P<pk>\d+)/$', DeleteCrewMemberView.as_view(), name='delete_member'),
	re_path(r'^crew/delete_crew/(?P<pk>\d+)/$', DeleteCrewView.as_view(), name='delete_crew'),
	re_path(r'^crew/delete_story/(?P<pk>\d+)/$', DeleteStoryView.as_view(), name='delete_story'),
	
	re_path(r'^story/(?P<story_id>[0-9]+)/$', views.story, name='story'),



]
