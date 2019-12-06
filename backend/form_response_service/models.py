from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from form_admin_service.models import *
# from backend.form_admin_service.models import *

# # Create your models here.
class FormResponse(models.Model):
    patient_id = models.CharField(max_length=500, blank=True)
    filler_id = models.CharField(max_length=500, blank=True)
    form_id = models.CharField(max_length=500, blank=False)
    # If we want to add more fields add them here!

class Answer(models.Model):
    answer_content = models.CharField(max_length=1000, blank=True)
    parent_form_response = models.ForeignKey(FormResponse, on_delete=models.CASCADE, null=True)
    sister_question_id = models.CharField(max_length=500, blank=False, default="NO SISTER QUESTION")
