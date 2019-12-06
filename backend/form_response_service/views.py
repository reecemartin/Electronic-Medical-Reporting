from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import xml.etree.ElementTree as ET

from django.contrib.auth.models import User
from .serializers import *

import json
from django.contrib.auth import authenticate

# TODO: get all the form responses
@api_view(['GET'])
def get_all_form_responses(request):
    if request.method == "GET":
        responses = FormResponse.objects.all()
        response_serializer = FormResponseSerializer(responses, many=True)

        return Response(data=response_serializer.data)

# TODO: use form_id, patient_id and filler_id to get the correct Form
@api_view(['POST'])
def get_form_response(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        if len(FormResponse.objects.filter(form_id=json_body['form_id'], patient_id=json_body['patient_id'], filler_id=json_body['filler_id'])) > 0:
            response_obj = FormResponse.objects.filter(form_id=json_body['form_id'], patient_id=json_body['patient_id'], filler_id=json_body['filler_id'])[0]
            return Response(data=convert_form_response_to_json(response_obj))
        return Response(status=status.HTTP_204_NO_CONTENT, data={})

# TODO: use form_id, patient_id and filler_id to get the correct Form and delete it
@api_view(['DELETE'])
def delete_form_response(request):
    if request.method == "DELETE":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        if len(FormResponse.objects.filter(form_id=json_body['form_id'], patient_id=json_body['patient_id'], filler_id=json_body['filler_id'])) > 0:
            FormResponse.objects.filter(form_id=json_body['form_id'], patient_id=json_body['patient_id'], filler_id=json_body['filler_id'])[0].delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_answer(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        form_id = json_body['form_id']
        question_id = json_body['question_id']
        patient_id = json_body['patient_id']
        filler_id = json_body['filler_id']
        response = FormResponse.objects.filter(form_id=form_id, patient_id=patient_id, filler_id=filler_id)[0]
        if len(Answer.objects.filter(sister_question_id=question_id, parent_form_response=response)) == 0:
            return Response(data={})
        else:
            answer = Answer.objects.filter(sister_question_id=question_id, parent_form_response=response)[0]
            answer_serializer = AnswerSerializer(answer, many=False)
            return Response(data=answer_serializer.data)


@api_view(['POST'])
def submit_form_response(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        response_info = json_body['response']
        if len(FormResponse.objects.filter(form_id=response_info['form_id'], patient_id=response_info['patient_id'],
                                           filler_id=response_info['filler_id'])) > 0:
            existing_response = FormResponse.objects.filter(form_id=response_info['form_id'],
                                        patient_id=response_info['patient_id'], filler_id=response_info['filler_id'])[0]
            FormResponse.delete(existing_response)
        response = parse_json_to_response(json_body)
        return Response(data=convert_form_response_to_json(response))


# HELPERS
def parse_json_to_response(response_json):
    form_id = response_json['response']['form_id']
    patient_id = response_json['response']['patient_id']
    filler_id = response_json['response']['filler_id']
    existing_response = FormResponse.objects.filter(form_id=form_id, patient_id=patient_id, filler_id=filler_id)
    if len(existing_response) == 0:
        response = FormResponse.objects.create(form_id=form_id, patient_id=patient_id, filler_id=filler_id)
        for section in response_json['sections']:
            parse_section_json(section, response)
        for free_question_id in response_json['free_questions']:
            free_question = response_json['free_questions'][free_question_id]
            parse_question_json(free_question, response)
        return response
    else:
        # To ne changed when editing is implemented
        return existing_response[0]

def parse_section_json(section_json, response):
    questions = section_json['questions']
    for question_id in questions:
        question = questions[question_id]
        parse_question_json(question, response)
    subsections = section_json['subsections']
    for subsection in subsections:
        parse_section_json(subsection, response)


def parse_question_json(question_json, response):
    answer_content = question_json['answer_content']
    sister_question_id = question_json['question_id']
    answer = Answer.objects.create(answer_content=answer_content, parent_form_response=response, sister_question_id=sister_question_id)

def convert_form_response_to_json(response):
    response_serializer = FormResponseSerializer(response, many=False)
    response_json = {'response': response_serializer.data}
    return response_json
