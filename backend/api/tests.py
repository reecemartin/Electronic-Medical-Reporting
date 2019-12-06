from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.test import TestCase, Client
from .serializers import UserSerializer
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import *
from .views import *
import json

# initialize the APIClient app
client = Client()

# Create your tests here.
class UserTestCase(APITestCase):

    def setUp(self):
        t1 = User.objects.create(username="test1@coolcats.com")
        t1.set_password("number1")
        t1.save()
        t2 = User.objects.create(username="test2@coolcats.com")
        t2.set_password("number2")
        t2.save()

    def test_get_all_users(self):
        response = client.get(reverse('get_users'))
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test1_successful_login(self):
        data = {'username': 'test1@coolcats.com',  'password': 'number1'}
        response = client.post(reverse('login'), data=data, content_type='application/json')
        self.assertTrue(authenticate(username="test1@coolcats.com", password="number1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["username"],"test1@coolcats.com")


    def test2_successful_login(self):
        data = {'username': 'test2@coolcats.com',  'password': 'number2'}
        response = client.post(reverse('login'), data=data, content_type='application/json')
        self.assertTrue(authenticate(username="test2@coolcats.com", password="number2"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["username"],"test2@coolcats.com")

    def test_unsuccessful_login_invalid_username(self):
        data = {'username': 'test3@coolcats.com',  'password': 'wrong'}
        response = client.post(reverse('login'), data=data, content_type='application/json')
        self.assertFalse(authenticate(username="test3@coolcats.com", password="wrong"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["username"], None)

    def test_unsuccessful_login_wrong_password(self):
        data = {'username': 'test1@coolcats.com',  'password': 'wrong'}
        response = client.post(reverse('login'), data=data, content_type='application/json')
        self.assertFalse(authenticate(username="test1@coolcats.com", password="wrong"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["username"], None)

    def test_successful_get_user_by_username(self):
        data = {'username': 'test1@coolcats.com'}
        response = client.post(reverse('get_user_by_username'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        receivedUser = response.data["user"]
        receivedProfile = response.data["profile"]
        self.assertIsNotNone(receivedUser)
        self.assertIsNotNone(receivedProfile)
        self.assertEqual(receivedUser["username"], "test1@coolcats.com")

    def test_unsuccessful_get_user_by_username(self):
        data = {'username': 'test3@coolcats.com'}
        response = client.post(reverse('get_user_by_username'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["success"])
        receivedUser = response.data["user"]
        receivedProfile = response.data["profile"]
        self.assertIsNone(receivedUser)
        self.assertIsNone(receivedProfile)


class ProfileTestCase(APITestCase):

    def setUp(self):
        t1 = User.objects.create(username="test1@coolcats.com")
        t1.set_password("number1")
        t1.save()
        profileObj = User.objects.get(username="test1@coolcats.com").profile
        profileObj.user_type = 'AD'
        profileObj.save()

        t2 = User.objects.create(username="test2@coolcats.com")
        t2.set_password("number2")
        t2.save()
        profileObj = User.objects.get(username="test2@coolcats.com").profile
        profileObj.user_type = 'CL'
        profileObj.save()

    def test_successful_get_user_by_username_admin(self):
        data = {'username': 'test1@coolcats.com'}
        response = client.post(reverse('get_user_by_username'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        receivedProfile = response.data["profile"]

        self.assertEqual(receivedProfile["user_type"], 'AD')
        self.assertNotEqual(receivedProfile["user_type"], 'CL')

    def test_successful_get_user_by_username_clinician(self):
        data = {'username': 'test2@coolcats.com'}
        response = client.post(reverse('get_user_by_username'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        receivedProfile = response.data["profile"]

        self.assertEqual(receivedProfile["user_type"], 'CL')
        self.assertNotEqual(receivedProfile["user_type"], 'AD')

class SubmitFormResponse(APITestCase):

    def setUp(self):
        form_xml = open('./Test_Files/Form_Response_Service/form_simple_response.xml', 'r')
        form_xml_data = form_xml.read()
        add_response = client.generic('POST', reverse('service_add_form'), data=form_xml_data)
        self.assertEqual(add_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(add_response.data, {})
        self.expected_form = add_response.data['form']
        self.assertEqual(self.expected_form['form_id'], 'test_simple')

    def test_convert_response_to_json(self):
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
