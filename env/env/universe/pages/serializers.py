from rest_framework import serializers
from .models import (
    Page,
    Following,
    Liking,
    Blogs,
    BlogLiked,
    Comment,
    CommentLikes
    )
from django.contrib.auth import get_user_model

User = get_user_model()

ACTIONS = settings.ACTIONS

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        feilds = '__all__'

    def get_following(self, obj):
        return obj.following.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()

class CreatePageSerializer(serializers.Serializer):
    id = serializers.InterField(read_only = True)
    name = serializers.CharField()
    descriptions = serializers.TextField()
    photo = serializers.ImageField(required = False)
    created = serializers.DateTimeField(read_only = True)
    updated = serializers.DateTimeField(read_only = True)

    def create(self, validated_data):
        return Page.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'

class LikingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liking
        fields = '__all__'

class CreateBlogSerializer(serializers.Serializer):
    reference_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()
    picture = serializers.ImageField(required=False)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Blogs.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class BlogSerializer(serializers.ModelSerializer):
    reports = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    parent = CreateBlogSerializer(read_only=True)

    class Meta:
        model = Blogs
        fields = "__all__"

    def get_reports(self, obj):
        return obj.reports.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return obj.comments.count()

    def get_content(self, obj):
        content = obj.content
        if obj.is_reblog:
            content = obj.parent.content
            return content


class BlogLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogLiked
        fields = '__all__'


class CreateCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    blog_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True, max_length=9000)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.blog_id = validated_data.get('blog_id', instance.blog_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_like(self, obj):
        return obj.like.count()

    def get_comment(self, obj):
        return obj.comment.count()


class CommentLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentLikes
        fields = '__all__'


class ActionBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    add = serializers.CharField(required=False, allow_blank=True)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ACTIONS:
            raise serializers.ValidationError(status=400)
        return value

