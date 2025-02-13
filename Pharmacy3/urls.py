"""
URL configuration for Pharmacy3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from pharmacy.Controller.home_page_controller import home_page
urlpatterns = [
   path('admin/', include('pharmacy.Router.admin_routes')),
    path('pharmacy_manager/', include('pharmacy.Router.pharmacy_manager_routes')),
    path('pharmacy_drug/', include('pharmacy.Router.pharmacy_drug_routes')),
    path('',home_page,name='homepage'),

]
