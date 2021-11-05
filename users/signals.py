from django.contrib.auth.models import User

from django.db.models.signals import post_save,post_delete
from .models import Profile
from django.core.mail import message, send_mail
from django.conf import settings

def createProfile(sender,instance,created,**kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )
        subject='Welcome to DevSearch'
        message='We are glad to have you here.'
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],
                fail_silently=False,
            )
        except:
            pass


post_save.connect(createProfile,sender=User)

def deleteUser(sender,instance,**kwargs):
    try:
        user=instance.user
        user.delete()
    except:
        pass

post_delete.connect(deleteUser,sender=Profile)


def updateUser(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user
    if created == False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()
    
post_save.connect(updateUser,sender=Profile)







    



