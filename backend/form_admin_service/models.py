from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Form(models.Model):
    package_id = models.CharField(max_length=500, blank=True)
    form_id = models.CharField(max_length=500, blank=True)
    form_title = models.CharField(max_length=1000, blank=True)
    form_footer = models.CharField(max_length=1500, blank=True)
    # If we want to add more fields add them here!
    # Then go to accounts/views.py


class Section(models.Model):
    section_id = models.CharField(max_length=500, blank=True)
    title = models.CharField(max_length=1000, blank=True)
    parent_form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True)
    parent_section = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Question(models.Model):
    question_id = models.CharField(max_length=500, blank=True)
    title = models.CharField(max_length=1000, blank=True)
    parent_section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    parent_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    dependent_answer = models.CharField(max_length=500, blank=True)
    parent_form = models.ForeignKey(Form, on_delete=models.CASCADE, null=True)
    question_type = models.CharField(max_length=3, default='ST')
    state = models.BooleanField(default=True)


class McQuestion(Question):
    options = models.CharField(max_length=1000, blank=True)
