from django.contrib import admin
from .models import *


# # Register your models here.

class FormResponseAdmin(admin.ModelAdmin):
    list_display = ('form_id', 'filler_id', 'patient_id') #add to this any other attributes we'd like to display

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_content', 'sister_question_id', 'parent_form_response') #add to this any other attributes we'd like to display


# # Register the admin class with the associated model
admin.site.register(FormResponse, FormResponseAdmin)
admin.site.register(Answer, AnswerAdmin)
