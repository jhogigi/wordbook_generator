from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('web.urls')),
    path('api/v1/', include('apiv1.urls')),
    path('admin/', admin.site.urls),
]
