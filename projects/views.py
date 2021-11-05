from django.shortcuts import render,redirect
from django.contrib import messages
from users.views import profiles
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects,paginationProjects
from django.contrib import messages

# Create your views here.


def projects(request):
    projects,search_query=searchProjects(request)
    for project in projects:
        project.getVoteCount
    projects,page,custom_range=paginationProjects(request,projects)


    context={'projects':projects,'search_query':search_query,'page':page,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectObj=Project.objects.get(id=pk)
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            review=form.save(commit=False)
            review.project=projectObj
            review.owner=request.user.profile
            review.save()
            projectObj.getVoteCount
            messages.success(request,'Your review was successfullt submitted!')
            return redirect('project',pk=projectObj.id)
    context={'projectObj':projectObj,'form':form}
    return render(request,'projects/single-project.html',context)

    
@login_required(login_url="login")
def  createProject(request):
    form=ProjectForm()
    profile=request.user.profile

    if request.method=="POST":
        newtags=request.POST.get('newtags')
        if newtags:
            newtags=newtags.replace(',',' ')
            newtags=newtags.split()
        
        form=ProjectForm(request.POST,request.FILES)
        
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=request.user.profile
            project.save()
            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            messages.success(request,'Project was added successfully!')

            return redirect('account')


    context={'form':form,'profile':profile}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def  updateProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)
    if request.method=="POST":
        newtags=request.POST.get('newtags')
        if newtags:
            newtags=newtags.replace(',',' ')
            newtags=newtags.split()
            
        
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project=form.save()
            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            messages.success(request,'Project was updated successfully!')
            return redirect('account')
            

    context={'form':form,'project':project}
    return render(request,'projects/project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile=request.user.profile

    project=profile.project_set.get(id=pk)
    if request.method=="POST":
        project.delete()
        messages.success(request,'Project was deleted successfully!')
        return redirect('account')
    context={'object':project}
    return render(request,'delete_template.html',context)


