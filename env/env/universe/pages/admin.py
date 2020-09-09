from django.contrib import admin
from .models import (
    Blogs,
    BlogLiked,
    Comment,
    CommentLikes,
    Page,
    Following,
    Liking
)

# Register your models here.


class PageFollowAdmin(admin.TabularInline):
    model = Following

class PageLikesAdmin(admin.TabularInline):
    model = Liking


class PageAdmin(admin.ModelAdmin):
    inlines = [PageFollowAdmin, PageLikesAdmin]
    list_display = ['name', 'user', 'created',  'user_info']

    search_feild = ['name']

    class Meta:
        model = Page


class CommentLikesAdmin(admin.TabularInline):
    model = CommentLikes


class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikesAdmin]
    list_display = ['text', 'blog', 'user',  'user_info']

    search_feild = ['blog']

    class Meta:
        model = Comment


class BlogLikesAdmin(admin.TabularInline):
    model = BlogLiked


class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikesAdmin]
    list_display = ['title', 'created', 'user',  'owner']

    search_feild = ['title']

    class Meta:
        model = Blogs

admin.site.register(Blogs, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Page, PageAdmin)
