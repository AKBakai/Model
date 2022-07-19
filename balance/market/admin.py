from django.contrib import admin
from .models import User, Post, Like, Ban

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'get_full_name',
        'user_post_count',
        'user_ban_count',
        'black_list',
        'email'
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'post',
        'like_count',
        'user_like_post'
    )

admin.site.register(Like)
admin.site.register(Ban)