import random
import itertools
from .story_resources.venue_templates import VENUE_TEMPLATES
from .story_resources.personality_actions import PERSONALITY_ACTIONS
from .models import StoryTemplate


class StoryGenerator(object):
	"""docstring for StoryGenerator"""
	def __init__(self, venue):
		super(StoryGenerator, self).__init__()
		self.venue = venue


	def createSubStory(self, member):
		"""Returns a substory and a string"""
		substory_template = ""
		obj_pronoun = ""
		subj_pronoun = ""
		actions = []
		name = member.name
		personality = member.personality

		# Pick random venue template
		venue_templates = StoryTemplate.objects.filter(venue__exact=self.venue)
		substory_template = random.choice([tmp.template for tmp in venue_templates])


		if member.gender == "Male":
			obj_pronoun = "him"
			subj_pronoun = "he"
			poss_pronoun = "his"
		elif member.gender == "Female":
			obj_pronoun = "her"
			subj_pronoun = "she"
			poss_pronoun = "her"
		else:
			obj_pronoun = "them"
			subj_pronoun = "they"
			poss_pronoun = "their"


		placeholder_count = substory_template.count('{}')
		available_actions = list(PERSONALITY_ACTIONS[personality].values())
		random.shuffle(available_actions)

		# We will get an Index Error if our template has more placeholders than actions
		# We solve this by sprinkling in a default actions to backfill placholders.
		if placeholder_count > len(available_actions):
			default_action = "winked at me"
			for _ in range(placeholder_count-len(available_actions)):
				available_actions.append(default_action)
			# Shuffle the winks in
			random.shuffle(available_actions)


		formatted_story = substory_template.format(*available_actions, 
													name=name, 
													obj_pronoun=obj_pronoun, 
													subj_pronoun=subj_pronoun,
													poss_pronoun=poss_pronoun )
		return formatted_story




