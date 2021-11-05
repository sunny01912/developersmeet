from django.db.models import Q
from .models import Profile
from django.core.paginator import Paginator
def searProfiles(request):
    search_query=''

    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')



    profiles=Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__name__icontains=search_query))
    return profiles,search_query

def paginationProfiles(request,profiles):
    paginator=Paginator(profiles,3)
    page=request.GET.get('page',1)
    profiles=paginator.get_page(page)
    leftIndex=int(page)-4
    if leftIndex<1:
        leftIndex=1
    
    rightIndex=int(page)+5
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages
    
    custom_range=range(leftIndex,rightIndex+1)
    return profiles,page,custom_range