from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Crew, CrewMember, Story
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

	class Meta:
		model = Story
		fields = ("story_name", "crew", "creator", "venue")
		exclude = ["creator"]

	def save(self, commit=True):
		user = super(StoryDetailsForm, self).save(commit=False)
		if commit:
			user.save()
		return user






