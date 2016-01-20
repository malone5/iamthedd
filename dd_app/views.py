from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.views.generic.base import View, TemplateView
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



from . import models
from .models import Crew, CrewMember, CreateCrewForm, CreateCrewMemberForm, Story
from .forms import UserCreateForm


# Create your views here.

def index(request):
	return render(request, 'dd_app/index.html')


# def logout(request):
# 	pass

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
	#get crew from database and distplay them
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

		if request.user and crew: #if the user and crew selected exists
			if crew.verify_crew(request.user): # if crew is under this users name
				# display form and crew members
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
		


def story(request, story_id):
	context = {}
	context['story'] = Story.objects.get(id=story_id)

	return render(request, 'dd_app/story.html', context)
