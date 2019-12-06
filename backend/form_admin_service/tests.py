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


# Create your tests here.
class AddFormTestCase(APITestCase):

    def test_simple_form_parsing(self):
        simple_form_xml = open('./Test_Files/Form_Admin_Service/Simple_Form.xml', 'r')
        simple_form_xml_data = simple_form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=simple_form_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], 'PKG_ACR_CT_STROKE')
        self.assertEqual(received_form['form_title'], 'CCO Synoptic Template for  Stroke')
        self.assertEqual(received_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')
        self.assertEqual(received_form['form_footer'], '(c) 2018 College of American Pathologists.  All rights '
                                                          'reserved.  License required for use.')

        received_sections = response.data['sections']
        self.assertEqual(type(received_sections), type([]))
        self.assertEqual(received_sections[0]['section_id'], '76242.100004300')
        self.assertEqual(received_sections[0]['title'], '#This template describes a Common Data Element for CT Stroke '
                                                        'by the American College of Radiologists')

        received_questions = received_sections[0]['questions']
        self.assertEqual(type(received_questions), type([]))
        self.assertEqual(received_questions[0]['question_id'], '76234.100004300')
        self.assertEqual(received_questions[0]['question_type'], 'MC')
        self.assertEqual(received_questions[0]['title'], '')
        self.assertEqual(received_questions[0]['options'], '@Adrenocortical neoplasm@')
        self.assertEqual(1, len(received_questions))

        received_free_questions = response.data['free_questions']
        self.assertEqual(received_free_questions, [])


    def test_medium_form_parsing(self):
        medium_form_xml = open('./Test_Files/Form_Admin_Service/Medium_Form.xml', 'r')
        medium_form_xml_data = medium_form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=medium_form_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], 'PKG_ACR_CT_STROKE')
        self.assertEqual(received_form['form_title'], 'CCO Synoptic Template for  Stroke')
        self.assertEqual(received_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')
        self.assertEqual(received_form['form_footer'], '(c) 2018 College of American Pathologists.  All rights '
                                                          'reserved.  License required for use.')
        received_sections = response.data['sections']
        self.assertEqual(received_sections[0]['section_id'], '76221.100004300')
        self.assertEqual(received_sections[0]['title'], 'Administrative & Identification Data')

        received_questions = received_sections[0]['questions']
        self.assertEqual(len(received_questions), 3)

        self.assertEqual(received_questions[0]['question_id'], '76219.100004300')
        self.assertEqual(received_questions[0]['question_type'], 'ST')
        self.assertEqual(received_questions[0]['title'], 'Report Date')

        self.assertEqual(received_questions[1]['question_id'], '76413.100004300')
        self.assertEqual(received_questions[1]['question_type'], 'ST')
        self.assertEqual(received_questions[1]['title'], 'Report completed by ')

        self.assertEqual(received_questions[2]['question_id'], '76325.100004300')
        self.assertEqual(received_questions[2]['question_type'], 'MC')
        self.assertEqual(received_questions[2]['title'], 'Procedure')
        self.assertEqual(received_questions[2]['options'], 'LDCT|Other (specify)')

        received_free_questions = response.data['free_questions']
        self.assertEqual(received_free_questions, [])

    def test_complex_form_parsing(self):
        complex_form_xml = open('./Test_Files/Form_Admin_Service/Complex_Form.xml', 'r')
        complex_form_xml_data = complex_form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=complex_form_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], 'PKG_ACR_CT_STROKE')
        self.assertEqual(received_form['form_title'], 'CCO Synoptic Template for  Stroke')
        self.assertEqual(received_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')
        self.assertEqual(received_form['form_footer'], '(c) 2018 College of American Pathologists.  All rights '
                                                          'reserved.  License required for use.')

        received_sections = response.data['sections']
        self.assertEqual(1, len(received_sections))
        self.assertEqual(received_sections[0]['section_id'], '77659.100004300')
        self.assertEqual(received_sections[0]['title'], 'Findings')
        self.assertEqual(len(received_sections[0]['questions']), 15)

        received_free_questions = response.data['free_questions']
        self.assertEqual(1, len(received_free_questions))
        self.assertEqual(received_free_questions[0]['question_id'], '76386.100004300')
        self.assertEqual(received_free_questions[0]['title'], 'Comment(s)')
        self.assertEqual(received_free_questions[0]['question_type'], 'ST')

    def test_form_with_subsections_parsing(self):
        subsection_xml = open('./Test_Files/Form_Admin_Service/Section_with_subsection.xml', 'r')
        subsection_form_xml_data = subsection_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=subsection_form_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})

        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], 'PKG_ACR_CT_STROKE')
        self.assertEqual(received_form['form_title'], 'CCO Synoptic Template for  Stroke')
        self.assertEqual(received_form['form_id'], "Subsection")
        self.assertEqual(received_form['form_footer'], '(c) 2018 College of American Pathologists.  All rights '
                                                          'reserved.  License required for use.')

        received_sections = response.data['sections']
        self.assertEqual(1, len(received_sections))

        self.assertEqual(received_sections[0]['section_id'], '000131')
        self.assertEqual(received_sections[0]['title'], 'IMPRESSIONS')
        self.assertEqual(len(received_sections[0]['questions']), 2)

        received_subsections = received_sections[0]['subsections']
        self.assertEqual(type(received_subsections), type([]))
        self.assertEqual(len(received_sections), 1)
        self.assertEqual(received_subsections[0]['section_id'], '000114')
        self.assertEqual(received_subsections[0]['title'], 'Lung-Rads Version 1.1 Assessment Category:')
        self.assertEqual(len(received_subsections[0]['questions']), 1)

    def test_form_with_dependant_questions_parsing(self):
        dependant_xml = open('./Test_Files/Form_Admin_Service/Adrenal.Bx.Res.129_3.003.001.REL_sdcFDF.xml')
        dependant_xml_data = dependant_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=dependant_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})

        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], '')
        self.assertEqual(received_form['form_title'], 'ADRENAL GLAND')
        self.assertEqual(received_form['form_id'], "Adrenal.Bx.Res.129_3.003.001.REL_sdcFDF")
        self.assertEqual(received_form['form_footer'], '(c) 2019 College of American Pathologists.  All rights '
                                                       'reserved.  License required for use.')

        received_sections = response.data['sections']
        self.assertEqual(9, len(received_sections))

        self.assertEqual(received_sections[0]['section_id'], '4257.100004300')
        self.assertEqual(received_sections[0]['title'], '')
        self.assertEqual(len(received_sections[0]['questions']), 1)

        section_with_dependent_questions = received_sections[3]
        self.assertEqual(section_with_dependent_questions['section_id'], '17876.100004300')
        self.assertEqual(section_with_dependent_questions['title'], 'TUMOR')
        self.assertEqual(len(section_with_dependent_questions['questions']), 7)

        question_with_dependents = section_with_dependent_questions['questions'][4]
        self.assertEqual(question_with_dependents['question_id'], '51265.100004300')
        self.assertEqual(question_with_dependents['title'], 'Tumor Extension')
        self.assertEqual(len(question_with_dependents['dependents']), 1)
        self.assertIsNotNone(question_with_dependents['dependents']['Tumor invades into other adjacent organ(s)'])

        dependant = question_with_dependents['dependents']['Tumor invades into other adjacent organ(s)']
        self.assertEqual(dependant['question_id'], '53526.100004300')
        self.assertFalse(dependant['state'])
        
    def test_PKG_ACR_CT_STROKE_parsing(self):
        form_xml = open('./Test_Files/Form_Admin_Service/PKG_ACR_CT_STROKE.xml', 'r')
        form_xml_data = form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=form_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], 'PKG_ACR_CT_STROKE')
        self.assertEqual(received_form['form_title'], 'CCO Synoptic Template for  Stroke')
        self.assertEqual(received_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')
        self.assertEqual(received_form['form_footer'], '(c) 2018 College of American Pathologists.  All rights '
                                                          'reserved.  License required for use.')

        received_sections = response.data['sections']
        self.assertEqual(len(received_sections), 3)

        self.assertEqual(len(received_sections[0]['questions']), 1)
        self.assertEqual(len(received_sections[1]['questions']), 3)
        self.assertEqual(len(received_sections[2]['questions']), 15)

        received_free_questions = response.data['free_questions']
        self.assertEqual(received_free_questions[0]['question_id'], '76386.100004300')
        self.assertEqual(received_free_questions[0]['title'], 'Comment(s)')
        self.assertEqual(received_free_questions[0]['question_type'], 'ST')

    def test_PKG_LDCT_LUNG_parsing(self):
        form_xml = open('./Test_Files/Form_Admin_Service/PKG_LDCT_LUNG_forStudents.xml', 'r')
        form_xml_data = form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=form_xml_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['package_id'], 'PKG_LDCT_Lung')
        self.assertEqual(received_form['form_title'], 'Lung Cancer Screening Template')
        self.assertEqual(received_form['form_id'], 'FORM_LDCT_Lung')
        self.assertEqual(received_form['form_footer'], '+ Data elements preceded with this symbol are optional')

        received_sections = response.data['sections']
        self.assertEqual(len(received_sections), 4)

        self.assertEqual(len(received_sections[0]['questions']), 2)
        self.assertEqual(len(received_sections[1]['questions']), 1)
        self.assertEqual(len(received_sections[2]['questions']), 7)
        self.assertEqual(len(received_sections[3]['questions']), 2)

        # Subsections
        received_subsections_000131 = received_sections[3]['subsections']
        self.assertEqual(len(received_subsections_000131), 2)
        self.assertEqual(len(received_subsections_000131[0]['questions']), 1)
        self.assertEqual(len(received_subsections_000131[1]['questions']), 1)

        received_free_questions = response.data['free_questions']
        self.assertEqual(len(received_free_questions), 0)

    def test_section_parsing(self):
        section_xml = open('./Test_Files/Form_Admin_Service/Section.xml', 'r')
        section_xml_data = section_xml.read()
        section = ET.fromstring(section_xml_data)
        form = Form.objects.create()

        result = parse_section(section, form)

        self.assertEqual(type(result), Section)
        self.assertEqual(result.section_id, "76242.100004300")
        self.assertEqual(result.title, "#This template describes a Common Data Element for CT Stroke by the American "
                                       "College of Radiologists")


    def test_question_parsing_simple_mc(self):
        mc_quesiton_xml = open('./Test_Files/Form_Admin_Service/Simple_MC_Question.xml', 'r')
        mc_quesiton_xml_data = mc_quesiton_xml.read()
        mc_question = ET.fromstring(mc_quesiton_xml_data)
        form = Form.objects.create()

        result = parse_question(mc_question, form)

        self.assertEqual(type(result), McQuestion)
        self.assertEqual(result.question_id, "77913.100004300")
        self.assertEqual(result.title, "Hyperacute signs")
        self.assertEqual(result.question_type, "MC")
        self.assertEqual(result.options, "Yes|No")

    def test_question_parsing_medium_mc(self):
        mc_quesiton_xml = open('./Test_Files/Form_Admin_Service/Medium_MC_Question.xml', 'r')
        mc_quesiton_xml_data = mc_quesiton_xml.read()
        mc_question = ET.fromstring(mc_quesiton_xml_data)
        form = Form.objects.create()

        result = parse_question(mc_question, form)

        self.assertEqual(type(result), McQuestion)
        self.assertEqual(result.question_id, "77920.100004300")
        self.assertEqual(result.title, "Vascular Territory")
        self.assertEqual(result.question_type, "MC")
        self.assertEqual(result.options, "ACA|MCA|PCA|SCA|AICA|PICA|Basil perforator|Thalamoperforator|AntChoroidal")

    def test_question_parsing_complex_mc(self):
        mc_quesiton_xml = open('./Test_Files/Form_Admin_Service/Complex_MC_Question.xml', 'r')
        mc_quesiton_xml_data = mc_quesiton_xml.read()
        mc_question = ET.fromstring(mc_quesiton_xml_data)
        form = Form.objects.create()

        result = parse_question(mc_question, form)

        self.assertEqual(type(result), McQuestion)
        self.assertEqual(result.question_id, "76325.100004300")
        self.assertEqual(result.title, "Procedure")
        self.assertEqual(result.question_type, "MC")
        self.assertEqual(result.options, "LDCT|Other (specify)")

    def test_question_parsing_simple_string(self):
        string_quesiton_xml = open('./Test_Files/Form_Admin_Service/String_Question.xml', 'r')
        string_quesiton_xml_data = string_quesiton_xml.read()
        string_question = ET.fromstring(string_quesiton_xml_data)
        form = Form.objects.create()

        result = parse_question(string_question, form)

        self.assertEqual(type(result), Question)
        self.assertEqual(result.question_id, "77940.100004300")
        self.assertEqual(result.title, "Midlineshift in mm")
        self.assertEqual(result.question_type, "ST")


class GetFormByIDTestCase(APITestCase):

    def setUp(self):
        form_xml = open('./Test_Files/Form_Admin_Service/PKG_ACR_CT_STROKE.xml', 'r')
        form_xml_data = form_xml.read()
        add_response = client.generic('POST', reverse('service_add_form'), data=form_xml_data)
        self.assertEqual(add_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(add_response.data, {})
        self.expected_form = add_response.data['form']
        self.assertEqual(self.expected_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')

        sample_form_xml = open('./Test_Files/Form_Admin_Service/Sample.xml', 'r')
        sample_form_xml_data = sample_form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=sample_form_xml_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['form_id'], 'SAMPLE')

    def test_successful_get_form_by_id(self):
        body_data = {"form_id": "CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF"}
        actual_response = client.post(reverse('service_get_form'), data=body_data, content_type='application/json')
        self.assertEqual(actual_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(actual_response.data, {})
        actual_form = actual_response.data['form']

        self.assertEqual(actual_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')
        self.assertEqual(actual_form['package_id'], 'PKG_ACR_CT_STROKE')
        self.assertEqual(actual_form['form_title'], 'CCO Synoptic Template for  Stroke')
        self.assertEqual(actual_form['form_footer'], '(c) 2018 College of American Pathologists.  All rights '
                                                          'reserved.  License required for use.')
        self.assertEqual(actual_form, self.expected_form)
        received_sections = actual_response.data['sections']
        self.assertEqual(len(received_sections), 3)

        self.assertEqual(len(received_sections[0]['questions']), 1)
        self.assertEqual(len(received_sections[1]['questions']), 3)
        self.assertEqual(len(received_sections[2]['questions']), 15)

        received_free_questions = actual_response.data['free_questions']
        self.assertEqual(received_free_questions[0]['question_id'], '76386.100004300')
        self.assertEqual(received_free_questions[0]['title'], 'Comment(s)')
        self.assertEqual(received_free_questions[0]['question_type'], 'ST')

    def test_unsuccessful_get_form_by_id(self):
        body_data = {"form_id": "fail"}
        actual_response = client.post(reverse('service_get_form'), data=body_data, content_type='application/json')
        self.assertEqual(actual_response.status_code, status.HTTP_200_OK)
        self.assertEqual(actual_response.data, {})


class DeleteForm(APITestCase):
    def setUp(self):
        form_xml = open('./Test_Files/Form_Admin_Service/PKG_ACR_CT_STROKE.xml', 'r')
        form_xml_data = form_xml.read()
        add_response = client.generic('POST', reverse('service_add_form'), data=form_xml_data)
        self.assertEqual(add_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(add_response.data, {})
        self.expected_form = add_response.data['form']
        self.assertEqual(self.expected_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')

        sample_form_xml = open('./Test_Files/Form_Admin_Service/Sample.xml', 'r')
        sample_form_xml_data = sample_form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=sample_form_xml_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['form_id'], 'SAMPLE')

    def test_successful_delete_form(self):
        body_data = {"form_id": "CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF"}
        actual_response = client.delete(reverse('service_delete_form'), data=body_data, content_type='application/json')
        self.assertEqual(actual_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(actual_response.data, {})
        status_code = actual_response.status_code
        self.assertEqual(actual_response.status_code, status.HTTP_200_OK)



    def test_unsuccessful_delete_form(self):
        body_data = {"form_id": "fail"}
        actual_response = client.post(reverse('service_delete_form'), data=body_data, content_type='application/json')
        self.assertEqual(actual_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GetAllForms(APITestCase):
    def setUp(self):
        form_xml = open('./Test_Files/Form_Admin_Service/PKG_ACR_CT_STROKE.xml', 'r')
        form_xml_data = form_xml.read()
        add_response = client.generic('POST', reverse('service_add_form'), data=form_xml_data)
        self.assertEqual(add_response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(add_response.data, {})
        self.expected_form = add_response.data['form']
        self.assertEqual(self.expected_form['form_id'], 'CT_Stroke_CCO.358_1.0.0.DRAFT_sdcFDF')

        sample_form_xml = open('./Test_Files/Form_Admin_Service/Sample.xml', 'r')
        sample_form_xml_data = sample_form_xml.read()
        response = client.generic('POST', reverse('service_add_form'), data=sample_form_xml_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, {})
        received_form = response.data['form']
        self.assertEqual(received_form['form_id'], 'SAMPLE')

    def test_successfull_get_all_forms(self):
        response = client.get(reverse('service_get_all_forms'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
