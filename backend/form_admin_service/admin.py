from django.contrib import admin
from .models import *


# Register your models here.

# Define the admin class
class FormAdmin(admin.ModelAdmin):
    list_display = ( 'form_id', 'package_id', 'form_title') #add to this any other attributes we'd like to display

class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_id', 'title', 'parent_form') #add to this any other attributes we'd like to display

class QuestionAdmin(admin.ModelAdmin):
        list_display = ('question_id', 'title', 'parent_form', 'parent_section', 'state', 'question_type')

# Register the admin class with the associated model
admin.site.register(Form, FormAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Question, QuestionAdmin)
