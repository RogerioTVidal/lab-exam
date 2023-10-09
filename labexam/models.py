# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from secrets import token_urlsafe


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
    return f'{self.name}'


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
    return f'{self.user} | {self.exam_type.name}'
def badge_template(self):
    if self.status == "R":
        classe = 'bg-warning text-dark'
        text = 'Review'
    if self.status == "F":
        classe = 'bg-success'
        text = 'Finished'

    return mark_safe(f'<span class="badge {classe}">{text}</span>')



class exam_order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ManyToManyField(exam_request)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()
def __str__(self):
    return f'{self.user} | {self.date}'


class doctor_access(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identification = models.CharField(max_length=50)
    access_time = models.IntegerField() # Em horas
    created = models.DateTimeField()
    inicial_exam_date = models.DateField()
    final_exam_date = models.DateField()
    token = models.CharField(max_length=20)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(doctor_access, self).save(*args, **kwargs)