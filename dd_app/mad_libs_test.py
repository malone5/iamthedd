

def tellStory(template, name, verb, noun, **kwargs):

	complete = template.format(name=name, verb=verb, noun=noun)
	print(complete)

story = "{name} Once upon there was a man name Tim. He loved to {verb}. {name} also loved to play with his {noun}"
verb = "run"
noun = "ball"
verb2 = "shoulf not see this"
name = "BoB"

tellStory(template=story,
			name=name,
			verb=verb,
			noun=noun,
			verb2=verb2)