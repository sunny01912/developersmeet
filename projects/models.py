from django.db import models
import uuid
# Create your models here.
from users.models import Profile

class Project(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    title=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    featured_image=models.ImageField(null=True,blank=True,default='default.jpg')
    demo_link=models.CharField(max_length=2000,null=True,blank=True)
    source_link=models.CharField(max_length=2000,null=True,blank=True)
    tags=models.ManyToManyField('Tag',blank=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering=['-vote_ratio','-vote_total','title']
    @property
    def reviewers(self):
        queryset=self.review_set.all().values_list('owner__id',flat=True)
        return queryset
    def imageURL(self):
        try:
            url=self.featured_image.url
        except:
            url='http://127.0.0.1:8000/images/default.jpg'
        return url


    @property
    def getVoteCount(self):
         reviews=self.review_set.all()
         upVotes=reviews.filter(value='up').count()
         totalVotes=reviews.count()
         try:
            ratio=(upVotes/totalVotes)*100
            ratio=int(ratio)
         except:
            ratio=0
         self.vote_ratio=ratio
         self.vote_total=totalVotes
         self.save()



class Review(models.Model):
    VOTE_TYPE=(
        ('up','up Vote'),
        ('down','Down Vote'),
    )
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=100,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.value
    class Meta:
        unique_together=[['owner','project']]

class Tag(models.Model):
    name=models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name




