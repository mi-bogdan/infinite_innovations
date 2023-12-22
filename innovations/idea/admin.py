from django.contrib import admin
from .models import Ip, Topic, Pin, Board, BoardPin, Comments, Like


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')
    list_display_links = ('id', 'ip')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_at')
    list_display_links = ('id', 'title')


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'create_at', 'update_at')
    list_display_links = ('id', 'title')
   


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description',
                    'user', 'create_at', 'update_at')
    list_display_links = ('id', 'title')


@admin.register(BoardPin)
class BoardPinAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'pin',
                    'user_by', 'create_at')
    list_display_links = ('id', 'board', 'pin')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'pin', 'text', 'user', 'create_at')
    list_display_links = ('id', 'pin')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'pin', 'user', 'created_at')
    list_display_links = ('id', 'pin')
