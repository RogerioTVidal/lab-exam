from django.contrib import admin
from .models import exam_type, exam_request, exam_order, doctor_access

admin.site.register(exam_type)
admin.site.register(exam_request)
admin.site.register(exam_order)
admin.site.register(doctor_access)
# Register your models here.
