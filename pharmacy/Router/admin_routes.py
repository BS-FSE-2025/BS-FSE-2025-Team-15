from django.urls import path
import pharmacy.Controller.pharmacy_drug_controller as pharmacy_drug_controller


urlpatterns = [
    path('createDrug/', pharmacy_drug_controller.create_drug, name='create_drug'),
]