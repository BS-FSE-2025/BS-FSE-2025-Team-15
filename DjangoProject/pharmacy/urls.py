from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pharmacy_manager/', include('pharmacy_manager.urls')),
    path('pharmacy_drug/', include('pharmacy_drug.urls')),
    
]
