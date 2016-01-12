from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models
from .models import Crew, CrewMember, CreateCrewForm, Story
from .forms import UserCreateForm


# Create your views here.

def index(request):
	return render(request, 'dd_app/index.html')


# def logout(request):
# 	pass

def register(request):
	if request.method == 'POST':
		form = UserCreateForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form = UserCreateForm()

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

@login_required(redirect_field_name='/login/')
def create_crew(request):
	if request.method == 'POST':
		form = CreateCrewForm(request.POST)

		if form.is_valid():	
			obj = form.save(commit=False)
			obj.owner = request.user
			form.save()
			return HttpResponseRedirect('/mycrews/')
	else:
		form = CreateCrewForm()

	return render(request, 'dd_app/create_crew.html', {'form': form})

@login_required(redirect_field_name='/login/')
def crew(request, crew_id):
	# match user id with Crew Id
	# match all storys that share that crew ID
	return render(request, 'dd_app/crew_page.html')
