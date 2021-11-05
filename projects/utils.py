from django.db.models import Q

from .models import Project
from django.core.paginator import Paginator

def searchProjects(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    
    projects=Project.objects.distinct().filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(tags__name__icontains=search_query) |
    Q(owner__name__icontains=search_query))
    return projects,search_query


def paginationProjects(request,projects):
    paginator=Paginator(projects,6)
    page=request.GET.get('page',1)
    projects=paginator.get_page(page)
    leftIndex=int(page)-4
    if leftIndex<1:
        leftIndex=1
    
    rightIndex=int(page)+5
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages
    
    custom_range=range(leftIndex,rightIndex+1)
    return projects,page,custom_range