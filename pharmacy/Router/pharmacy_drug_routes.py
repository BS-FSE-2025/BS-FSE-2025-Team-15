from django.urls import path
import pharmacy.Controller.pharmacy_drug_controller as pharmacy_drug_controller


urlpatterns = [
    path('add_pharmacy_drug/', pharmacy_drug_controller.add_pharmacy_drug, name='add_pharmacy_drug'),
    path('delete/', pharmacy_drug_controller.delete_drug, name='delete_pharmacy_drug'),
    path('update/', pharmacy_drug_controller.update_drug, name='update_pharmacy_drug'),
    path('get/', pharmacy_drug_controller.get_drug, name='get_pharmacy_drug'),
    path('createDrug/', pharmacy_drug_controller.create_drug, name='create_drug'),

]