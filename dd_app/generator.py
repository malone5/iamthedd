import random
from .story_resources.venue_templates import VENUE_TEMPLATES
from .story_resources.personality_actions import PERSONALITY_ACTIONS


class StoryGenerator(object):
	"""docstring for StoryGenerator"""
	def __init__(self, venue):
		super(StoryGenerator, self).__init__()
		# self.story_variables = story_variables
		# seld.dd = story_variables['creator']
		# self.crew = story_variables['crew']
		self.venue = venue


	def createSubStory(self, member):
		"""Returns a substory and a string"""
		#what we nedd
		substory_template = ""
		obj_pronoun = ""
		subj_pronoun = ""
		actions = []
		name = member.name
		personality = member.personality

		substory_template = random.choice(list(VENUE_TEMPLATES[self.venue].values()))

		if member.gender == "Male":
			obj_pronoun = "him"
			subj_pronoun = "he"
			poss_pronoun = "his"
		else:
			obj_pronoun = "her"
			subj_pronoun = "she"
			poss_pronoun = "her"

		for i in range(5):
			#pick a random action based on personality and add it to the actions list
			action = random.choice(list(PERSONALITY_ACTIONS[self.venue][personality].values()))
			actions.append(action)


		formatted_story = substory_template.format(*actions, 
													name=name, 
													obj_pronoun=obj_pronoun, 
													subj_pronoun=subj_pronoun )
		return formatted_story




