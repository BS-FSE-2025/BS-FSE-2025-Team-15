from django.urls import path
import pharmacy.Controller.pharmacy_manager_controller as pharmacy_manager_controller
import pharmacy.View.pharmacy_manager_views as pharmacy_manager_views
import pharmacy.Controller.request_controller as request_controller


urlpatterns = [
    path('create/', pharmacy_manager_controller.create_new_pharmacy_manager, name='create_pharmacy_manager'),
    path('delete/<int:manager_id>/', pharmacy_manager_controller.delete_pharmacy_manager, name='delete_pharmacy_manager'),
    path('update/', pharmacy_manager_controller.update_pharmacy_manager, name='update_pharmacy_manager'),
    path('get/', pharmacy_manager_controller.get_pharmacy_manager, name='get_pharmacy_manager'),
    path('login/', pharmacy_manager_controller.login, name='login'),
    path('logout/', pharmacy_manager_controller.logout, name='logout'),
    path('dashboard/<int:pharmacy_id>/', pharmacy_manager_views.pharmacy_dashboard_to_user, name='pharmacy_dashboard_to_user'),
    path('dashboard/', pharmacy_manager_views.pharmacy_manager_dashboard, name='pharmacy_manager_dashboard'),

    path('newRequest/', request_controller.create_request, name='create_new_request'),
    path('managerRequest/', request_controller.manager_requests, name='manager_requests'),
    path('editRequest/', request_controller.edit_request, name='manager_edit_request'),
    path('resetPasswordRequest/', request_controller.reset_password, name='reset_password_request'),

]