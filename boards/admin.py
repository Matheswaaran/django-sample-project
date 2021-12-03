from django.contrib import admin

from .models import Board, Topic, Post


# Register your models here.

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('subject', 'is_active', 'created_at', 'updated_at', 'board', 'starter', 'views')
    list_filter = ('is_active', 'starter',)
    search_fields = ('subject',)
    ordering = ('-created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'is_active', 'topic', 'created_at', 'updated_at', 'created_by', 'updated_by')
    list_filter = ('is_active', 'created_by', 'updated_by',)
    search_fields = ('message',)
    ordering = ('-created_at',)
