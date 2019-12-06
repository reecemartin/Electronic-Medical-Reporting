from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponse
        fields = ('patient_id', 'filler_id', 'form_id')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answer_content', 'sister_question_id')

