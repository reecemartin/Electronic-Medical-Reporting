from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import reverse

import xml.etree.ElementTree as ET
import requests

from django.contrib.auth.models import User
from .serializers import *

import json
from django.contrib.auth import authenticate


@api_view(['GET'])
def get_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def get_user_by_username(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        username = json_body['username']
        try:
            user = User.objects.get(username=username)
            profile = user.profile
            user_serializer = UserSerializer(user, many=False)
            profile_serializer = ProfileSerializer(profile, many=False)
            return Response(data={'success': True, 'user': user_serializer.data, 'profile': profile_serializer.data})
        except:
            return Response(data={'success': False, 'user': None, 'profile': None})

@api_view(['POST'])
# Create your views here.
def login(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        username = json_body["username"]
        password = json_body["password"]


        user = authenticate(username=username, password=password)

        if user is not None:
            return Response(data={'success': True, 'username': user.username})
        else:
            return Response(data={'success': False, 'username': None})

@api_view(['POST'])
def add_form(request):
    if request.method == "POST":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_add_form')
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        form_data = json_body["form"]
        encoded_data = form_data.encode(encoding='UTF-8')
        service_response = requests.post(url=request_url, data=encoded_data)
        json_body = json.loads(service_response.text)
        return Response(data=json_body)

@api_view(['POST'])
def get_form_by_id(request):
    if request.method == "POST":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_get_form')
        service_response = requests.post(url=request_url, data=request.body)
        json_body = json.loads(service_response.text)
        return Response(data=json_body)


@api_view(['GET'])
def get_all_forms(request):
    if request.method == "GET":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_get_all_forms')
        service_response = requests.get(url=request_url)
        json_body = json.loads(service_response.text)
        return Response(data=json_body)


@api_view(['DELETE'])
def delete_form(request):
    if request.method == "DELETE":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('delete_form')
        service_response = requests.delete(url=request_url, data=request.body)
        json_body = json.loads(json.dumps({"status_code": service_response.status_code}))
        return Response(data=json_body)


@api_view(['POST'])
def submit_form_response(request):
    if request.method == "POST":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_submit_form_response')
        service_response = requests.post(url=request_url, data=request.body)
        json_body = json.loads(service_response.text)
        form_id = json_body['response']['form_id']
        patient_id = json_body['response']['patient_id']
        filler_id = json_body['response']['filler_id']
        response_json = convert_response_to_json(patient_id, form_id, filler_id, root_path)
        return Response(data=response_json)


def convert_response_to_json(patient_id, form_id, filler_id, root_path):
    response_json = {'response': {
        'patient_id': patient_id,
        'form_id': form_id,
        'filler_id': filler_id
    }, 'sections':[], 'free_questions':{}}
    request_url = root_path + reverse('service_get_form')
    data = {"form_id": form_id}
    service_response = requests.post(url=request_url, data=json.dumps(data))
    json_body = json.loads(service_response.text)
    sections = json_body['sections']
    for section in sections:
        response_json['sections'].append(convert_response_section_to_json(patient_id, form_id, filler_id, root_path, section))
    free_questions = json_body['free_questions']
    for free_question in free_questions:
        free_question_id = free_question['question_id']
        response_json['free_questions'][free_question_id] = convert_response_question_to_json(patient_id, form_id, filler_id, root_path, free_question)
    return response_json

def convert_response_section_to_json(patient_id, form_id, filler_id, root_path, section):
    section_json = {'section_id': section['section_id'], 'questions': {}, "subsections": []}
    questions = section['questions']
    for question in questions:
        question_id = question['question_id']
        section_json['questions'][question_id] = convert_response_question_to_json(patient_id, form_id, filler_id, root_path, question)
        dependents = question['dependents']
        for dependent in dependents:
            dependent_id = dependents[dependent]['question_id']
            dependent_question_json = convert_response_question_to_json(patient_id, form_id, filler_id, root_path, dependents[dependent])
            if dependent_question_json is not None:
                section_json['questions'][dependent_id] = dependent_question_json
    subsections = section['subsections']
    for subsection in subsections:
        section_json['subsections'].append(convert_response_section_to_json(patient_id, form_id, filler_id, root_path, subsection))
    return section_json

def convert_response_question_to_json(patient_id, form_id, filler_id, root_path, question):
    question_json = {'question_id': question['question_id'], 'state': question['state']}
    query_data = {'patient_id': patient_id, 'form_id': form_id, 'filler_id': filler_id,
                  'question_id': question['question_id']}
    answer = requests.post(url=root_path + reverse('service_get_answer'), data=json.dumps(query_data))
    answer_json_body = json.loads(answer.text)
    if answer_json_body != {}:
        question_json['answer_content'] = answer_json_body['answer_content']
        return question_json
    return None


@api_view(['POST'])
def get_form_response(request):
    if request.method == "POST":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_get_form_response')
        service_response = requests.post(url=request_url, data=request.body)
        json_body = json.loads(service_response.text)
        form_id = json_body['response']['form_id']
        patient_id = json_body['response']['patient_id']
        filler_id = json_body['response']['filler_id']
        response_json = convert_response_to_json(patient_id, form_id, filler_id, root_path)
        return Response(data=response_json)


@api_view(['GET'])
def get_all_form_responses(request):
    if request.method == "GET":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_get_all_form_responses')
        service_response = requests.get(url=request_url)
        json_body = json.loads(service_response.text)
        return Response(data=json_body)


@api_view(['DELETE'])
def delete_form_response(request):
    if request.method == "DELETE":
        root_path = request.build_absolute_uri('/')[:-1].strip("/")
        request_url = root_path + reverse('service_delete_form_response')
        service_response = requests.delete(url=request_url, data=request.body)
        json_body = json.loads(json.dumps({"status_code": service_response.status_code}))
        return Response(data=json_body)
