from django.contrib import admin
from .models import exam_type, exam_request, exam_order

admin.site.register(exam_type)
admin.site.register(exam_request)
admin.site.register(exam_order)
# Register your models here.
