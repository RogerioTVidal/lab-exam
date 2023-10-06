from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class exam_type(models.Model):
    type_choices = (
        ('I', 'Image Exam'),
        ('B', 'Blood Exam')
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=type_choices)
    price = models.FloatField()
    avaliable = models.BooleanField(default=True)
    initial_hour = models.IntegerField()
    final_hour = models.IntegerField()
def __str__(self):
    return self.name

class exam_request(models.Model):
    status_choices = (
        ('R', 'Review'),
        ('F', 'Finished')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(exam_type, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=status_choices)
    result = models.FileField(upload_to="result", null=True, blank=True)
    password_required = models.BooleanField(default=False)
    password = models.CharField(max_length=6, null=True, blank=True)
def __str__(self):
    return f'{self.user} | {self.exam.name}'

class exam_order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ManyToManyField(exam_request)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()
def __str__(self):
    return f'{self.user} | {self.date}'