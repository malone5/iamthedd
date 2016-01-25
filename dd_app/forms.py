from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Crew, CrewMember
from .story_constants import VENUE_CHOICES

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

class StoryDetailsForm(forms.Form):

	creator = forms.ModelChoiceField(queryset=User.objects.none())
	crew = forms.ModelChoiceField(queryset=Crew.objects.none())
	story_name = forms.CharField(max_length=30)
	venue = forms.ChoiceField(choices=VENUE_CHOICES)

	# def generate_story(self, data):
	# 	dd = data['creator']
	# 	venue = data['venue']
	# 	obj1 = data['obj1']
	# 	obj2 = data['obj2']
	# 	verb1 = data['verb1']
	# 	verb2 = data['verb2']

	# 	# get the crew members
		#





