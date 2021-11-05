from django.contrib.auth.forms import  UserCreationForm,PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets

from .models import Profile,Skill,Message
from users import models


class CustomUserCreation(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','username','email','password1','password2']
        labels={'first_name':"Name"}
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreation,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields='__all__'
        exclude=['user']
        
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm,self).__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
     

class SkillForrm(forms.ModelForm):
    class Meta:
        model=Skill
        fields='__all__'
        exclude=['owner']
    
    def __init__(self,*args,**kwargs):
        super(SkillForrm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['name','email','subject','body']
    def __init__(self,*args,**kwargs):
        super(MessageForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class CustomPasswordChangeForm(PasswordChangeForm):
  
    # widgets={
    #     'old_password':forms.PasswordInput(attrs={'class':'input'}),
    #     'new_password1':forms.PasswordInput(attrs={'class':'input'}),
    #     'new_password2':forms.PasswordInput(attrs={'class':'input'}),

    # }
    def __init__(self,*args,**kwargs):
        super(CustomPasswordChangeForm,self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})







