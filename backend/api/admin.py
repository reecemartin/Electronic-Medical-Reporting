from django.contrib import admin
from .models import Profile


# Register your models here.

# Define the admin class
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'displayname') #add to this any other attributes we'd like to display

# Register the admin class with the associated model
admin.site.register(Profile, ProfileAdmin)