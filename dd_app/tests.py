from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from .models import Crew, CrewMember, StoryTemplate
from .generator import StoryGenerator
# Create your tests here.


class StoryGeneratorTests(TestCase):
	fixtures = ["test_fixture_valid.json"]

	def test_create_user(self):
		user = User.objects.create_user(username='guy', password='pass')
		if user is not None:
			userexists = True
		else:
			userexists = False

		self.assertEqual(userexists, True)

	def test_create_Crew(self):
		user = User.objects.create_user(username='guy', password='pass')
		user.save()
		crew = Crew.objects.create(crew_name="My Crew", owner=user)

		if crew is not None:
			crewexists = True
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
		else:
			substoryexists = False

		self.assertEqual(substoryexists, True)

	

class StoryTemplateTests(TestCase):
	def test_create_template(self):

		form = {
			'venue': 'Bar', 
			'template': 'Testing is {name} was at the bar and {action}',
			'creator': 'tester'
		}

		st = StoryTemplate.objects.create(**form)
		self.assertEqual(st.template, 'Testing is {name} was at the bar and {action}')

	def test_named_placeholder_to_blank_placeholder(self):
		""" 'action_event' placeholders should convert to blank placeholders """
		
		form = {
			'venue': 'Bar', 
			'template': '{name} arrived at the venue and {action_event}. Then the owner {action_event}',
			'creator': 'tester'
		}

		st = StoryTemplate.objects.create(**form)
		st.convert_to_empty_curlybraces('{action_event}')
		expected = '{name} arrived at the venue and {}. Then the owner {}'
		self.assertEqual(st.template, expected)
	

class BadTemplateTests(TestCase):
	fixtures = ["test_fixture_bad_template.json"]

	# Edge case
	def test_too_many_action_placeholders(self):
		""" When there are more placeholders than available action events, backfill with default action"""
		user = User.objects.create_user(username='tester', password='pass')
		crew = Crew.objects.create(crew_name="My Crew", owner=user)
		member = CrewMember.objects.create(name="crewman", crew=crew, personality="Angry")
		story = StoryGenerator('BadVenue')
		substory = story.createSubStory(member)
		self.assertIn('winked at me', substory)

	# Edge case
	def test_no_templates_exist(self):
		""" When no templates exist for the venue"""
		user = User.objects.create_user(username='tester', password='pass')
		crew = Crew.objects.create(crew_name="My Crew", owner=user)
		member = CrewMember.objects.create(name="crewman", crew=crew, personality="Angry")
		story = StoryGenerator('NonExistingVenue')
		substory = story.createSubStory(member)
		expected = """crewman got lost on their way to the NonExistingVenue 
					because No story templates exists for the NonExistingVenue venue yet!"""
		self.assertEquals(expected, substory)


