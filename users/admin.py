from django.contrib import admin
from .models import Profile,Skill,Message

# Register your models here.

admin.site.register(Message)
admin.site.register(Skill)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','name']
