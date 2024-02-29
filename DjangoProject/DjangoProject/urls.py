from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.urls import path

from main.views import page_not_found

urlpatterns = [

    path('admin/', admin.site.urls),
    path('',include('main.urls')),
    path('tinkoffapp/',include('tinkoffapp.urls')),
    path('users/',include('users.urls', namespace='users')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found