from django.contrib import admin
from .models import Crew, CrewMember, Story, MemberSubStory

# Register your models here.
admin.site.register(Crew)
admin.site.register(CrewMember)
admin.site.register(Story)
admin.site.register(MemberSubStory)
