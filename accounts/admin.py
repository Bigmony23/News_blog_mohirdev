from django.contrib import admin
from .models import Profile

class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ['user','date_of_birth','photo']

admin.site.register(Profile,ProfileUserAdmin)

# Register your models here.
