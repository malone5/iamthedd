from __future__ import unicode_literals

from django.utils import timezone
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

# Create your models here


class Crew(models.Model):
	crew_name = models.CharField(max_length=20)
	owner = models.ForeignKey(User, default=User)
	date_created = models.DateTimeField('date created', default=timezone.now())

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
	ANGRY = 'Angry'
	PARENT = 'Parental Figure'
	DRAMA_QUEEN = 'Drama-queen'
	FLIRT = 'Flirt'
	NO_CHANGE = 'No Change'
	PARTY_STARTER = 'Party Starter'
	REBEL = 'Rebel'
	RECKLESS = 'Reckless'
	SUPER_FRIENDLY = 'Super-friendly'

	PERSONALITY_CHOICES = (
		(ANGRY, 'Angry'),
		(PARENT, 'Parental Figure'),
		(DRAMA_QUEEN, 'Drama-queen'),
		(FLIRT, 'Flirt'),
		(NO_CHANGE, 'No Change'),
		(PARTY_STARTER, 'Party Starter'),
		(REBEL, 'Rebel'),
		(RECKLESS, 'Reckless'),
		(SUPER_FRIENDLY, 'Super-friendly'),
	)

	GENDER_CHOICE = (
		('Male', 'Male'),
		('Female', 'Female')
	)

	name = models.CharField(max_length=20)
	crew = models.ForeignKey(Crew)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICE, default='Male')
	personality = models.CharField(max_length=20, 
								choices=PERSONALITY_CHOICES, 
								default=ANGRY)


	def __str__(self):
		return self.name

class CreateCrewMemberForm(forms.ModelForm):
    class Meta:
        model = CrewMember
        exclude = ('crew',)
        fields = ('name', 'personality', 'crew')

        labels = {
            'personality': _('Best describe them during a night out for drinks'),
        }


class Story(models.Model):
	story_name = models.CharField(max_length=30)
	crew = models.ForeignKey(Crew)
	creator = models.ForeignKey(User)

	class Meta:
		verbose_name = "Story"
		verbose_name_plural = "Stories"
		
	def __str__(self):
		return self.story_name

	def get_all_substories(self):
		sub_stories = MemberSubStory.objects.all().filter(id=this.id)
		return sub_stories

class MemberSubStory(models.Model):
	story = models.ForeignKey(Story)
	member = models.ForeignKey(CrewMember)
	content = models.TextField()

	class Meta:
		verbose_name = "SubStory"
		verbose_name_plural = "SubStories"
		
	def __str__(self):
		return "{}'s part in, '{}'".format(this.member, this.story)

	def get_member_dict(self, crew):
		member_list = CrewMember.objects.all().filter(crew_name=crew)
		return member_list


    
       
    