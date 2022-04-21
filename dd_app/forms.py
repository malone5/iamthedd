from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Crew, Story, StoryTemplate
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


EXAMPLE_TEMPLATE = """Example:
I knew {name} was going to be a problem when {subj_pronoun} {action_event}.
{poss_pronoun} mission was to be the most popular person there.
That backfired when {name} {action_event}
"""

class StoryTemplateForm(forms.Form):

	venue = forms.ChoiceField(choices=VENUE_CHOICES)
	textarea_attrs = {"placeholder": EXAMPLE_TEMPLATE, "cols": 75}
	template = forms.CharField(widget=forms.Textarea(attrs=textarea_attrs))
	
	def save(self, commit=True):
		st = StoryTemplate(venue=self.cleaned_data['venue'], template=self.cleaned_data['template'])
		st.convert_to_empty_curlybraces('{action_event}')
		if commit:
			st.save()
		return st




