from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from .models import Crew, CrewMember
from .generator import StoryGenerator
# Create your tests here.


class StroyGeneratorTests(TestCase):

	def test_create_user(self):
		user = User.objects.create_user(username='guy', password='pass')
		if user is not None:
			userexists = True
			print(user)
		else:
			userexists = False

		self.assertEqual(userexists, True)

	def test_create_Crew(self):
		user = User.objects.create_user(username='guy', password='pass')
		user.save()
		crew = Crew.objects.create(crew_name="My Crew", owner=user)


		if crew is not None:
			crewexists = True
			print(crew)
		else:
			crewexists = False

		self.assertEqual(crewexists, True)

	def test_story_was_created_and_formatted(self):
		user = User.objects.create_user(username='guy', password='pass')
		crew = Crew.objects.create(crew_name="My Crew", owner=user)
		member = CrewMember.objects.create(name="crewguy", crew=crew, personality="Angry")

		story = StoryGenerator('Bar')
		substory = story.createSubStory(member)

		if substory is not None:
			substoryexists = True
			print(substory)
		else:
			substoryexists = False

		self.assertEqual(substoryexists, True)


