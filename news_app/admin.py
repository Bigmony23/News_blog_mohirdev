from django.contrib import admin
from pip._vendor.rich.markup import Tag

from .models import Category, News, Contact,Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','slug','publish_time','status','body']
    list_filter = ['status','created_time','publish_time']
    prepopulated_fields = {'slug':('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title','body']
    ordering = ['publish_time','status']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','message']
    list_filter = ['name','email','message']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','body','created_time','active']
    list_filter = ['active','created_time']
    search_fields = ['user','body']
    actions = ['disable_comments','enable_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)

    def enable_comments(self, request, queryset):
        queryset.update(active=True)

#admin.site.register(Comment,CommentAdmin)