from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = ('package_id', 'form_id', 'form_title', 'form_footer')

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('section_id', 'title')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_id', 'title', 'question_type', 'state')

class McQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McQuestion
        fields = ('question_id', 'title', 'question_type', 'state', 'options')
