
from django.shortcuts import render,redirect
from .models import Profile, Skill,Message
from django.http import HttpResponseRedirect, request
#import for authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreation,ProfileForm,SkillForrm,MessageForm,CustomPasswordChangeForm
from .utils import searProfiles,paginationProfiles
from django.db.models import Q


# Create your views here.

def profiles(request):
    profiles,search_query=searProfiles(request)
    profiles,page,custom_range=paginationProfiles(request,profiles)


    context={'profiles':profiles,'search_query':search_query,'page':page,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile=Profile.objects.get(id=pk)
    context={'profile':profile}
    return render(request,'users/user_profile.html',context)


def userLogin(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method=='POST':
        username=request.POST.get('username')
        username=username.lower()
        password=request.POST.get('password')
        
        try:
            user=User.objects.get(username=username)
        except:
            
            messages.error(request,'username does not exist')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET.get('next','account'))
            
        else:

            messages.error(request,'username or password is incorrect')
        

    return render(request,'users/login-register.html',{'page':page})

@login_required(login_url="login")
def userLogout(request):
    logout(request)
    messages.info(request,'User was successfully logout')

    return redirect('login')

def userRegistration(request):
    page='register'
    form=CustomUserCreation()
    if request.method=="POST":
        form=CustomUserCreation(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'user has been created')
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,'something went wrong')

    context={'form':form,'page':page}
    return render(request,'users/login-register.html',context)

@login_required(login_url='login')
def userAccount(request):
    profile=request.user.profile
    projects=profile.project_set.all()
    context={'profile':profile,'projects':projects}
    return render(request,'users/account.html',context)


@login_required(login_url="login")
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)


@login_required(login_url="login")
def createSkill(request):
    page='create'
    
    if request.method=="POST":
        form=SkillForrm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=request.user.profile
            skill.save()
            messages.success(request,'skill was added successfully!')
            return redirect('account')
        else:
            messages.error(request,'Please Enter Correctly!!!')
    else:
        form=SkillForrm()
    context={'form':form,'page':page}
    return render(request,'users/skill_form.html',context)
@login_required(login_url='login')
def updateSkill(request,pk):
    page='update'
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForrm(instance=skill)
    if request.method=='POST':
        form=SkillForrm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,'skill was updated successfully!')
            return redirect('account')
    context={"form":form,'page':page}
    return render(request,'users/skill_form.html',context)
@login_required(login_url='login')
def deleteSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method=='POST':
        skill.delete()
        messages.error(request,'skill was deleted successfully!')
        return redirect('account')
    return render(request,'delete_template.html',{'object':skill})

@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    inboxMessages= profile.messages.all()
    unreadCount=inboxMessages.filter(is_read=False).count()

    context={'inboxMessages':inboxMessages,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)

@login_required(login_url='login')
def viewMessage(request,pk):
    msg=Message.objects.get(id=pk)
    if msg.is_read==False:
        msg.is_read=True
        msg.save()
    context={'message':msg}
    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient=Profile.objects.get(id=pk)
    form=MessageForm()
    try:
        sender=request.user.profile
    except:
        sender=None
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            msg=form.save(commit=False)
            msg.sender=sender
            msg.recipient=recipient

            if sender:
                msg.name=sender.name
                msg.email=sender.email
            msg.save()

            messages.success(request,'Your message was sent!')

            return redirect('user-profile',pk=pk)



    context={'recipient':recipient,'form':form}
    return render(request,'users/message_form.html',context)


def passwordChange(request):
    profile=request.user.profile
    
    if request.method=='POST':
        form=CustomPasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            old_password=form.cleaned_data['old_password']
            new_password1=form.cleaned_data['new_password1']
            new_password2=form.cleaned_data['new_password2']
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'Password has been successfully changed!')
            return redirect('account')
        else:
            messages.error(request,'Please fill the  form correctly!!')
    else:
        form=CustomPasswordChangeForm(user=request.user)
    
    context={'form':form,'profile':profile}
    return render(request,'users/password-change.html',context)


