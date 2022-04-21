from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages


from . import models
from .models import Crew, CrewMember, Story, MemberSubStory, CreateCrewForm, CreateCrewMemberForm, CreateStoryForm, StoryTemplate
from .forms import UserCreateForm, StoryTemplateForm
from .generator import StoryGenerator


# Create your views here.

def index(request):
	return render(request, 'dd_app/index.html')


class RegisterView(View):

	def get(self, request):
		form = UserCreateForm()
		form.error_messages = {} #clear errors on get
		return render(request, 'registration/register.html', {'form': form})

	def post(self, request):
		form = UserCreateForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/login/')
		return render(request, 'registration/register.html', {'form': form})



def logout_user(request):
    logout(request)
    # Redirect to a success page.
    return redirect('dd_app:index')



@login_required(redirect_field_name='/login/')
def mycrews(request):
	context = {}
	# Get crews and stories from database
	if request.user:
		context['crews'] = Crew.objects.all().filter(owner=request.user)
		context['stories'] = Story.objects.all().filter(creator=request.user)
		return render(request, 'dd_app/mycrews.html', context)
	else:
		return render(request, 'dd_app/mycrews.html')


@method_decorator(login_required, name='dispatch')
class CrewView(View):

	def get(self, request, crew_id):
		crew = Crew.objects.get(id=crew_id)

		if request.user and crew: 
			if crew.verify_crew(request.user):

				crew_members = CrewMember.objects.filter(crew=crew)
				form = CreateCrewMemberForm()
				return render(request, 'dd_app/crew_page.html', {'form': form, 
																'crew': crew, 
																'crew_members': crew_members})
			else:
				return HttpResponseForbidden('<h2>You are not allowed to view this crew.</h2>')
		else:
			return render(request, 'dd_app/mycrews.html')

	def post(self, request, crew_id):
		#Create the crew member
		crew = Crew.objects.get(id=crew_id)
		form = CreateCrewMemberForm(request.POST)
		crew_members = CrewMember.objects.filter(crew=crew)
		if form.is_valid():	
			obj = form.save(commit=False)
			obj.crew = crew
			form.save()
			return HttpResponseRedirect(reverse('dd_app:crew', args=(crew.id,)))
		else:
			return render(request, 'dd_app/crew_page.html', {'form': form, 
															'crew': crew, 
															'crew_members': crew_members})



class DeleteCrewView(DeleteView):
	model = Crew
	template_name = 'dd_app/delete_confirm_template.html'

	def get_success_url(self):
		return reverse('dd_app:mycrews')

class DeleteStoryView(DeleteView):
	model = Story
	template_name = 'dd_app/delete_confirm_template.html'

	def get_success_url(self):
		return reverse('dd_app:mycrews')

class DeleteCrewMemberView(DeleteView):
	model = CrewMember
	template_name = 'dd_app/delete_confirm_template.html'

	def get_success_url(self):
		crew = self.object.crew
		return reverse('dd_app:crew', args=(crew.id,))






@method_decorator(login_required, name='dispatch')
class CreateCrewView(View):

	def get(self, request):
		form = CreateCrewForm()
		return render(request, 'dd_app/create_crew.html', {'form': form})
		

	def post(self, request):
		form = CreateCrewForm(request.POST)

		if form.is_valid():	
			obj = form.save(commit=False)
			obj.owner = request.user
			form.save()
			return HttpResponseRedirect('/mycrews/')
		

@method_decorator(login_required, name='dispatch')
class CreateStoryView(View):

	def get(self, request):

		form = CreateStoryForm()
		form.fields['crew'].queryset = Crew.objects.filter(owner=request.user)
		return render(request, 'dd_app/new_story.html', {'form': form})

	def post(self, request):
		form = CreateStoryForm(request.POST)

		if form.is_valid():	
			
			# 1. Create the story object and add to the database
			story_obj = form.save(commit=False)
			story_obj.creator = request.user
			story_obj.save()

			# 2. Loop through the crew members and create a substory for each member. 
			gen = StoryGenerator(venue=story_obj.venue)
			crew_members = CrewMember.objects.filter(crew=story_obj.crew)
			for member in crew_members:
				substory = gen.createSubStory(member)
				submitted_substory = MemberSubStory.objects.create(story=story_obj, member=member, content=substory)
				if submitted_substory == None:
					return HttpResponse("There was a problem creating your story. Sorry!")
			
			return HttpResponseRedirect('/mycrews/') # should change this to rediract to the story page

		else:
			return render(request, 'dd_app/new_story.html', {'form': form})



def story(request, story_id):
	context = {}
	story = Story.objects.get(id=story_id)
	context['story'] = story
	substories = MemberSubStory.objects.filter(story=story)
	context['substories'] = substories

	return render(request, 'dd_app/story.html', context)


@method_decorator(login_required, name='dispatch')
class StoryTemplateListView(View):

	def get(self, request):
		context = {}
		context['story_template_list'] = StoryTemplate.objects.all()
		context['form'] = StoryTemplateForm()
		return render(request, 'dd_app/storytemplate_list.html', context)

	def post(self, request):
		form = StoryTemplateForm(request.POST)
		if form.is_valid():
			# save to db
			st = form.save(commit=False)
			st.creator = request.user
			st.save()
			messages.success(request, "New story template added!")
			return HttpResponseRedirect('/templates/')
		
		messages.error(request, "Something went wrong creating story!")
		return HttpResponseRedirect('/templates/')



@method_decorator(login_required, name='dispatch')
class StoryTemplateView(View):

	def get(self, request):

		form = StoryTemplateForm()
		return render(request, 'dd_app/create_storytemplate.html', {'form': form})

	def post(self, request):
		form = StoryTemplateForm(request.POST)

		if form.is_valid():	
			return HttpResponseRedirect('/templates/') # should change this to rediract to the story page
		else:
			return render(request, 'dd_app/new_story.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class DeleteStoryTemplateView(DeleteView):
	model = StoryTemplate
	template_name = 'dd_app/delete_confirm_template.html'

	def get_success_url(self):
		return reverse('dd_app:templates')