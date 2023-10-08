
#labexams - main
#labexam - exam interfaces (oreder, request, type)
#labuser - user interfaces (register and login)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('labuser.urls')),
    path('exam/', include('labexam.urls')),
]
