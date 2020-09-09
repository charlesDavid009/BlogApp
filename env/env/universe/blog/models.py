from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

USER = get_user_model()

# Create your models here.


class BlogQuerySet(models.QuerySet):
    def feed(self, user):

        profiles_exist = user.following.exists()
        followed_users = []
        if profiles_exist:
            followed_users = user.following.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users) |
            Q(user=user)
        ).distinct().order_by("-created")


class BlogManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BlogQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user)


class Blog(models.Model):
    """
    API FOR USER TO CREATE THEIR OWN BLOG POST
    """
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.CharField(max_length=8000, blank=False, null=True)
    picture = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(User, related_name='Blog_comments', blank=True, through='Comment')
    likes = models.ManyToManyField(User, related_name='Blog_likes', blank=True, through='BlogLikes')
    reports = models.ManyToManyField(User, related_name='Blog_reports', blank=True, through='Report')
    created = models.DateTimeField(auto_now_add=True)

    objects = BlogManager()

    class Meta:
        ordering = ['-id']

    @property
    def is_reblog(self):
        return self.parrent != None

    @property
    def owner(self):
        return self.user


class Report(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class BlogLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Comment(models.Model):
    """
    MODELS FOR COMMENTS 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(USER, blank=True, related_name='Commnets_likes', through="CommentLikes")
    comment = models.ManyToManyField(USER, blank=True,  related_name='Commnets_count', through="SubComment")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class CommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class SubComment(models.Model):
    """
    MODELS FOR SUB COMMENTS  
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(
        USER, blank=True, related_name='SubCommnets_likes', through="SubCommentLikes")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class SubCommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
