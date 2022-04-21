from __future__ import unicode_literals

import re
from itertools import count
from django.utils import timezone
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .story_constants import VENUE_CHOICES, GENDER_CHOICES, PERSONALITY_CHOICES

# Create your models here
class Crew(models.Model):
	crew_name = models.CharField(max_length=20)
	owner = models.ForeignKey(User, default=User, on_delete=models.CASCADE)
	date_created = models.DateTimeField('date created', default=timezone.now)

	def __str__(self):
		return self.crew_name

	def get_members(self):
		return CrewMember.objects.filter(crew_name=self.crew_name)

	def verify_crew(self, logged_in_user):
		# Check and see if the owner of this crew matches the user that is logged in.
		if self.owner == logged_in_user:
			return True
		return False


class CreateCrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        exclude = ('owner', 'date_created',)
        fields = ('crew_name', 'owner', 'date_created')
    


class CrewMember(models.Model):
	name = models.CharField(max_length=20)
	crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
	gender = models.CharField(max_length=15, choices=GENDER_CHOICES, default='Genderless')
	personality = models.CharField(max_length=20, 
								choices=PERSONALITY_CHOICES, 
								default='Angry')


	def __str__(self):
		return self.name

class CreateCrewMemberForm(forms.ModelForm):
    class Meta:
        model = CrewMember
        exclude = ('crew',)
        fields = ('name', 'gender','personality', 'crew')

        labels = {
            'personality': _('Best describe them during a night out for drinks'),
        }


class Story(models.Model):
	story_name = models.CharField(max_length=30)
	crew = models.ForeignKey(Crew, on_delete=models.CASCADE)
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	venue = models.CharField(max_length=20,
							choices=VENUE_CHOICES,
							default='Bar')

	class Meta:
		verbose_name = "Story"
		verbose_name_plural = "Stories"
		

	def __str__(self):
		return "'{}' By: {}.".format(self.story_name, self.creator)

	def get_all_substories(self):
		sub_stories = MemberSubStory.objects.all().filter(id=this.id)
		return sub_stories


class CreateStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        exclude = ('creator',)
        fields = ('story_name', 'crew', 'venue')

        labels = {
            'story_name': _('Story Title'),
        }


class MemberSubStory(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	member = models.ForeignKey(CrewMember, on_delete=models.CASCADE)
	content = models.TextField()

	class Meta:
		verbose_name = "SubStory"
		verbose_name_plural = "SubStories"
		
	def __str__(self):
		return "{}'s part in, '{}'".format(self.member, self.story)

	def get_member_dict(self, crew):
		member_list = CrewMember.objects.all().filter(crew_name=crew)
		return member_list



class StoryTemplate(models.Model):


	id = models.BigAutoField(primary_key=True)
	venue = models.CharField(max_length=20,
							choices=VENUE_CHOICES,
							default='Bar')
	template = models.TextField()
	creator = models.CharField(max_length=255)

	class Meta:
		verbose_name = "StoryTemplate"
		verbose_name_plural = "StoryTemplates"

	def __str__(self):
		return "'{}:{}' By: {}.".format(self.venue, self.id, self.creator)

	def convert_to_empty_curlybraces(self, placeholder='{action}'):
		""" given a substring, convert each occurance to use empty placeholders (i.e {}, {}, etc.."""
		self.template = self.template.replace(placeholder, '{}')




