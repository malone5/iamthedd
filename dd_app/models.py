from __future__ import unicode_literals

from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.
class Crew(models.Model):
	crew_name = models.CharField(max_length=20)
	owner = models.ForeignKey(User, default=None)
	date_created = models.DateTimeField('date published')

	def __str__(self):
		return self.crew_name

	def get_members(self):
		pass

class CreateCrewForm(forms.ModelForm):
    class Meta:
        model = Crew
        exclude = ['owner']
        fields = ('crew_name', 'owner', 'date_created')
    


class CrewMember(models.Model):
	name = models.CharField(max_length=20)
	crew_name = models.ForeignKey(Crew)

	def __str__(self):
		return self.name

    
        
    