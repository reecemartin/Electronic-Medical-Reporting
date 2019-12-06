from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate
from .views import *
from .models import *
import json

# initialize the APIClient app
client = Client()

class SubmitResponseTestCase(APITestCase):

    def test_submit_response(self):
        simple_response = open('./Test_Files/Form_Response_Service/simple_response.json', 'r')
        simple_response_json = simple_response.read()
        response = client.post(reverse('service_submit_form_response'), data=simple_response_json, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})

        received_response = response.data['response']
        self.assertEqual(received_response['form_id'], 'test_simple')
        self.assertEqual(received_response['patient_id'], 'patient 1')
        self.assertEqual(received_response['filler_id'], 'clinician@coolcats.com')

class GetAnswerByQuestionIDResponseID(APITestCase):

    def setUp(self):
        simple_response = open('./Test_Files/Form_Response_Service/simple_response.json', 'r')
        simple_response_json = simple_response.read()
        response = client.post(reverse('service_submit_form_response'), data=simple_response_json,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})

        received_response = response.data['response']
        self.assertEqual(received_response['form_id'], 'test_simple')
        self.assertEqual(received_response['patient_id'], 'patient 1')
        self.assertEqual(received_response['filler_id'], 'clinician@coolcats.com')

    def test_succesfull_get_answer(self):
        body_data = {"form_id": "test_simple", "question_id": "77913.100004300", 'patient_id':'patient 1', 'filler_id':'clinician@coolcats.com'}
        actual_response = client.post(reverse('service_get_answer'), data=body_data, content_type='application/json')
        self.assertEqual(actual_response.data['sister_question_id'], "77913.100004300")
        self.assertEqual(actual_response.data['answer_content'], "yes")

# Create your tests here.
class GetAllFormResponsesTestCase(APITestCase):
    # TODO
    def setUp(self):
        simple_response = open('./Test_Files/Form_Response_Service/simple_response.json', 'r')
        simple_response_json = simple_response.read()
        response = client.post(reverse('service_submit_form_response'), data=simple_response_json,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})

        received_response = response.data['response']
        self.assertEqual(received_response['form_id'], 'test_simple')
        self.assertEqual(received_response['patient_id'], 'patient 1')
        self.assertEqual(received_response['filler_id'], 'clinician@coolcats.com')

    # TODO
    def test_get_all_form_responses(self):
        response = client.generic('GET', reverse('service_get_all_form_responses'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetFormResponseByIDTestCase(APITestCase):
    def setUp(self):
        simple_response = open('./Test_Files/Form_Response_Service/simple_response.json', 'r')
        simple_response_json = simple_response.read()
        response = client.post(reverse('service_submit_form_response'), data=simple_response_json,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        self.expected_response = response.data['response']

        received_response = response.data['response']
        self.assertEqual(received_response['form_id'], 'test_simple')
        self.assertEqual(received_response['patient_id'], 'patient 1')
        self.assertEqual(received_response['filler_id'], 'clinician@coolcats.com')

    # TODO
    def test_successful_get_response(self):
        body_data = {'form_id': 'test_simple', 'patient_id': 'patient 1', 'filler_id': 'clinician@coolcats.com'}
        response = client.post(reverse('service_get_form_response'), data=body_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})

        actual_response = response.data['response']
        self.assertEqual(actual_response['form_id'], 'test_simple')
        self.assertEqual(actual_response['patient_id'], 'patient 1')
        self.assertEqual(actual_response['filler_id'], 'clinician@coolcats.com')
        self.assertEqual(actual_response, self.expected_response)

    def test_unsuccessful_get_response(self):
        body_data = {"form_id": 'fail' ,"patient_id": 'fail', "filler_id": 'fail'}
        actual_response = client.post(reverse('service_get_form_response'), data=body_data, content_type='application/json')
        self.assertNotEqual(actual_response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual_response.data, {})


class DeleteFormResponse(APITestCase):
    def setUp(self):
        simple_response = open('./Test_Files/Form_Response_Service/simple_response.json', 'r')
        simple_response_json = simple_response.read()
        response = client.post(reverse('service_submit_form_response'), data=simple_response_json,
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        self.expected_response = response.data['response']

        received_response = response.data['response']
        self.assertEqual(received_response['form_id'], 'test_simple')
        self.assertEqual(received_response['patient_id'], 'patient 1')
        self.assertEqual(received_response['filler_id'], 'clinician@coolcats.com')

    def test_successful_delete_response(self):
        body_data = {"form_id": 'test_simple' ,"patient_id": 'patient 1', "filler_id": 'clinician@coolcats.com'}
        response = client.delete(reverse('service_delete_form_response'), data=body_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, None)

    def test_unsuccessful_delete_response(self):
        body_data = {"form_id": 'fail' ,"patient_id": 'fail', "filler_id": 'fail'}
        response = client.delete(reverse('service_delete_form_response'), data=body_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
