from django.contrib import admin
from .models import Project, Review, Tag
# Register your models here.


# admin.site.register(Project)


# admin.site.register(Review)
admin.site.register(Tag)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display=['title','owner']

    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['owner','project','value']