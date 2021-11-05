from api import serializers
from projects.models import Project, Review, Tag
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response

from .serializers import ProjectSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    return Response({'api':'devsearch'})


@api_view(['GET'])
def getProjects(request):
    print('USER:',request.user)
    projects=Project.objects.all()
    serializer=ProjectSerializer(projects,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request,pk):
    project=Project.objects.get(id=pk)
    serializer=ProjectSerializer(project,many=False)
    return Response(serializer.data)



@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def projectVote(request,pk):
    project=Project.objects.get(id=pk)
    profile=request.user.profile
    data=request.data
    
    if data:
        review,created=Review.objects.get_or_create(
            owner=profile,
            project=project
        )
        
        
        review.value=data['value']
        if data.get('body'):
            review.body=data.get('body')
        review.save()
        project.getVoteCount


        serializer=ProjectSerializer(project,many=False)
        return Response(serializer.data)
        
    else:
        return Response({'message':'please provide necessary data!!!'})

@api_view(['DELETE'])
def removeTag(request):
    tagID=request.data['tag']
    projectID=request.data['project']
    project=Project.objects.get(id=projectID)
    tag=Tag.objects.get(id=tagID)
    project.tags.remove(tag)
    return Response('Tag was removed!!!')