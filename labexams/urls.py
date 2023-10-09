
#labexams - main
#labexam - exam interfaces (oreder, request, type)
#labuser - user interfaces (register and login)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('labuser.urls')),
    path('exam/', include('labexam.urls')),
    path('business/', include('business.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
