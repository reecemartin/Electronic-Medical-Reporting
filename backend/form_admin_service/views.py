from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import xml.etree.ElementTree as ET

from django.contrib.auth.models import User
from .serializers import *

import json
from django.contrib.auth import authenticate


@api_view(['POST'])
def add_form(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        form = parse_xml_to_form(body_unicode)
        return Response(data=convert_form_obj_to_json(form))


@api_view(['DELETE'])
def delete_form(request):
    if request.method == "DELETE":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        form_id = json_body['form_id']
        if len(Form.objects.filter(form_id=form_id)) > 0:
            Form.objects.filter(form_id=form_id).delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_all_forms(request):
    if request.method == "GET":
        forms = Form.objects.all()
        form_serializer = FormSerializer(forms, many=True)
        return Response(data=form_serializer.data)


def parse_xml_to_form(xml):
    root = ET.fromstring(xml)
    if 'SDCPackage' in root.tag:
        package_id = root.attrib['packageID']
        form_design = root[0][0]
    else:
        package_id = ''
        form_design = root
    form_title = form_design.attrib['formTitle']
    form_id = form_design.attrib['ID']
    existing_form = Form.objects.filter(form_id=form_id)

    if len(existing_form) == 0:
        form = Form.objects.create(package_id=package_id, form_title=form_title, form_id=form_id)
        for child in form_design:
            handle_child(child, form)

        return form
    else:
        return existing_form[0]


def handle_child(child, form):
    tag = child.tag.split("}", 2)[1]
    if tag == "Property":
        handle_property(child, form)
    elif tag == "Body":
        handle_body(child, form)
    elif tag == "Footer":
        handle_footer(child, form)
    else:
        return

def handle_property(child, form):
    # property_name = child.attrib['name']
    # property_value = child.attrib['name']
    return

def get_index_of_full_tagged_element(tag, root):
    i = 0
    while tag not in root[i].tag.split("}", 2)[1]:
        i += 1
    return i
def get_index_of_short_tagged_element(tag, root):
    i = 0
    while tag not in root[i].tag:
        i += 1
    return i

def handle_body(child, form):
    i = get_index_of_full_tagged_element('ChildItems', child)
    root = child[i]

    for child in root:
        tag = child.tag.split("}", 2)[1]
        if 'Section' in tag:
            handle_section(child, form)
        elif 'Question' in tag:
            handle_question(child, form)
    return

def handle_section(root, form, parent_section=None):
    section = parse_section(root, form)
    i = get_index_of_full_tagged_element('ChildItems', root)
    for child in root[i]:
        if 'Question' in child.tag:
            question_obj = parse_question(child, form)
            if type(section) != Section:
                section = section[0]
            question_obj.parent_section = section
            question_obj.parent_form = form
            question_obj.save()
        elif 'Section' in child.tag:
            handle_section(child, form, section)
    section.parent_section = parent_section
    section.parent_form = form
    section.save()

    return

def handle_question(root, form):
    parsed_question = parse_question(root, form)
    parsed_question.parent_form = form
    parsed_question.save()
    return

def parse_section(root, form):
    section_id = root.attrib['ID']
    if 'title' in root.attrib:
        title = root.attrib['title']
    else:
        title = ''
    existing_section = Section.objects.filter(section_id=section_id, parent_form=form)
    if len(existing_section) == 0:
        section = Section.objects.create(section_id=section_id, title=title)
        section.save()
        return section
    else:
        return existing_section

def parse_question(root, form, parent_question=None, dependent_answer=''):
    i = 0
    while 'ListField' not in root[i].tag and 'ResponseField' not in root[i].tag:
        i += 1

    child = root[i]
    if 'ListField' in child.tag:
        return parse_mc_question(root, form, parent_question, dependent_answer)
    elif 'ResponseField' in child.tag:
        return parse_string_question(root, form, parent_question, dependent_answer)

def parse_string_question(root, form, parent_question=None, dependent_answer=''):
    question_id = root.attrib['ID']
    if 'title' in root.attrib:
        title = root.attrib['title']
    else:
        title = ''
    existing_question = Question.objects.filter(question_id=question_id, parent_form=form)
    if len(existing_question) == 0:
        question = Question.objects.create(question_id=question_id, title=title)
        question.question_type = 'ST'
        question.parent_question = parent_question
        question.dependent_answer = dependent_answer
        question.save()
        return question
    else:
        return existing_question

def parse_mc_question(root, form, parent_question=None,  dependent_answer=''):
    question_id = root.attrib['ID']
    existing_question = McQuestion.objects.filter(question_id=question_id, parent_form=form)
    if len(existing_question) == 0:
        question = McQuestion.objects.create(question_id=question_id)

        if 'title' in root.attrib:
            question.title = root.attrib['title']

        choices_string = ""
        i = get_index_of_short_tagged_element("List", root)
        choices = root[i][0]

        for choice in choices:
            if (len(choice) > 0 and 'ChildItems' in choice[0].tag):
                    answer = choice.attrib['title']
                    dependant_question = parse_question(choice[0][0], form, question, answer)
                    dependant_question.parent_form = form
                    dependant_question.state = False
                    dependant_question.save()
            value = choice.attrib['title']
            if 'selected' in choice.attrib and choice.attrib['selected'] == 'true':
                choices_string += '@' + value.strip() + '@|'
            else:
                choices_string += value.strip() + '|'
        choices_string = choices_string[0:-1]
        question.options = choices_string
        question.question_type = 'MC'
        question.parent_question = parent_question
        question.dependent_answer = dependent_answer
        question.save()
        return question
    else:
        return existing_question

def handle_footer(child, form):
    footer_prop = child[0]
    form.form_footer = footer_prop.attrib['val']
    form.save()
    return

@api_view(['POST'])
def get_form_by_id(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        form_id = json_body['form_id']
        if len(Form.objects.filter(form_id=form_id)) > 0:
            form = Form.objects.filter(form_id=form_id)[0]
            return Response(data=convert_form_obj_to_json(form))
        else:
            return Response(data={})

def convert_sections_objs_to_json(form_sections, form):
    sections = []
    for form_section in form_sections:
        section = convert_section_to_json(form_section, form)
        subsections = Section.objects.filter(parent_section=form_section)
        section['subsections'] = convert_sections_objs_to_json(subsections, form)
        sections.append(section)
    return sections

def convert_section_to_json(form_section, form):
    section_serializer = SectionSerializer(form_section, many=False)
    section_data = section_serializer.data
    section_questions = Question.objects.filter(parent_section=form_section, parent_form=form)
    section = section_data
    section['questions'] = []
    section['subsections'] = {}
    for question in section_questions:
        section['questions'].append(convert_question_obj_to_json(question, form))
    return section

def convert_question_obj_to_json(question, form):
    question_serializer_data_copy = {}
    if question.question_type == 'MC':
        mc_question = McQuestion.objects.filter(question_id=question.question_id, parent_form=form)[0]
        question_serializer = McQuestionSerializer(mc_question, many=False)
        question_serializer_data_copy = question_serializer.data

    elif question.question_type == 'ST':
        question_serializer = QuestionSerializer(question, many=False)
        question_serializer_data_copy = question_serializer.data

    question_serializer_data_copy['dependents'] = {}
    dependent_questions = Question.objects.filter(parent_question=question, parent_form=form)
    for dependent in dependent_questions:
        question_serializer_data_copy['dependents'][dependent.dependent_answer] = convert_question_obj_to_json(dependent, form)
    return question_serializer_data_copy


def convert_form_obj_to_json(form):
    form_serializer = FormSerializer(form, many=False)
    form_sections = Section.objects.filter(parent_form=form, parent_section=None)
    data = {'form': form_serializer.data, 'sections': convert_sections_objs_to_json(form_sections, form),
            'free_questions': []}

    free_questions = Question.objects.filter(parent_section=None, parent_form=form, parent_question=None)
    for free_question in free_questions:
        if free_question.question_type == 'MC':
            mc_question = McQuestion.objects.filter(question_id=free_question.question_id, parent_form=form)[0]
            question_serializer = McQuestionSerializer(mc_question, many=False)
            data['free_questions'][question_serializer.data['question_id']] = question_serializer.data
        elif free_question.question_type == 'ST':
            question_serializer = QuestionSerializer(free_question, many=False)
            data['free_questions'].append(question_serializer.data)

    return data
