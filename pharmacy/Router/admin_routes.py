from django.urls import path
import pharmacy.Controller.drug_controller as drug_controller
import pharmacy.Controller.pharmacy_manager_controller as pharmacy_manager_controller
import pharmacy.Controller.request_controller as request_controller




urlpatterns = [
    path('newDrug/', drug_controller.create_drug, name='create_new_drug'),
    path('deleteDrug/<int:drug_id>/', drug_controller.delete_drug, name='delete_drug'),
    path('editDrug/', drug_controller.edit_drug, name='edit_drug'),
    path('dashboard/drugs', drug_controller.admin_dashboard, name='admin_drugs_dashboard'),
    path('dashboard/managers', pharmacy_manager_controller.get_all_pharmacy_managers, name='admin_managers_dashboard'),

    path('dashboard/requests', request_controller.admin_dashboard, name='admin_request_dashboard'),
    path('deleteRequest/<int:request_id>/', request_controller.delete_request, name='delete_request'),
    path('editRequest/', request_controller.edit_request, name='edit_request'),
]