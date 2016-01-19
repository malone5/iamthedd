from __future__ import unicode_literals

from django.utils import timezone
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here


class Crew(models.Model):
	crew_name = models.CharField(max_length=20)
	owner = models.ForeignKey(User, default=None)
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
	name = models.CharField(max_length=20)
	crew = models.ForeignKey(Crew)

	def __str__(self):
		return self.name

class CreateCrewMemberForm(forms.ModelForm):
    class Meta:
        model = CrewMember
        exclude = ('crew',)
        fields = ('name', 'crew')


class Story(models.Model):
	story_name = models.CharField(max_length=30)
	content = models.CharField(max_length=100)
	crew = models.ForeignKey(Crew)
	creator = models.ForeignKey(User)

	class Meta:
		verbose_name = "Story"
		verbose_name_plural = "Storys"
		
	def __str__(self):
		return self.story_name

	def get_member_dict(self, crew):
		member_list = CrewMember.objects.all().filter(crew_name=crew)
		return member_list

    

    
        
    