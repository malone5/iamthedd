from __future__ import unicode_literals

from django.utils import timezone
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
class Crew(models.Model):
	crew_name = models.CharField(max_length=20)
	owner = models.ForeignKey(User, default=None)
	date_created = models.DateTimeField('date created', default=timezone.now())

	def __str__(self):
		return self.crew_name

	def get_members(self):
		pass


class CreateCrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        exclude = ('owner', 'date_created',)
        fields = ('crew_name', 'owner', 'date_created')
    


class CrewMember(models.Model):
	name = models.CharField(max_length=20)
	crew_name = models.ForeignKey(Crew)

	def __str__(self):
		return self.name

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

    

    
        
    