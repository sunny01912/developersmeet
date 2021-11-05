from django import forms
from django.forms import fields, models
from .models import Project, Review
class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['title','featured_image' ,'description','demo_link','source_link']

        widgets={
            
            'title':forms.TextInput(attrs={'class':'input input--text','placeholder':'Enter title'}),
            'featured_image':forms.FileInput(attrs={'class':'input input--text','placeholder':'Select an Image'}),
            'description':forms.Textarea(attrs={'class':'input input--text','placeholder':'Enter Description'}),
            'demo_link':forms.TextInput(attrs={'class':'input input--text','placeholder':'Enter demo link'}),
            'source_link':forms.TextInput(attrs={'class':'input input--text','placeholder':'Enter Source Link'}),
            'tags':forms.CheckboxSelectMultiple(attrs={'class':'input input--text','placeholder':'Select Tags'}),
        }


    # def __int__(self,*args,**kwargs):
    #     super(ProjectForm,self).__init__(*args,**kwargs)

    #     for name,field in self.fields.items():
    #         field.widget.attrs.update({'class':'input input--text'})

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['value','body']

        labels={
            'value':'Place your vote',
            'body':'Add a comment with your vote'
        }

    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input input--text'})