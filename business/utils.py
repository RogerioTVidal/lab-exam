from random import choice, shuffle
from io import BytesIO
import string
import os


def fGeneratePassword(length):

    special_character = string.punctuation   
    character = string.ascii_letters
    list_numbers = string.digits

    
    rest = 0
    qtd = length // 3
    if not length % 3 == 0:
        rest = length - qtd

    chars = ''
    for i in range(0, qtd + rest):
        chars += choice(character)

    numbers = ''
    for i in range(0, qtd):
        numbers += choice(list_numbers)

    specials = ''
    for i in range(0, qtd):
        specials += choice(special_character)

    
    pwd = list(chars + numbers + specials)
    shuffle(pwd)

    return ''.join(pwd)

from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML


def fCreatePdfExam(exam, patient, pwd):

    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/exam-pwd.html')
    template_render = render_to_string(path_template, {'exam': exam, 'patient': patient, 'pwd': pwd})

    path_output = BytesIO()

    HTML(string=template_render).write_pdf(path_output)
    path_output.seek(0)
    
    return path_output