from django.contrib import admin

# Register your models here.

from homepage.models import User_Profile

class User_ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'duoshuo_id')

admin.site.register(User_Profile, User_ProfileAdmin)
