from django.urls import path
import pharmacy.Controller.pharmacy_manager_controller as pharmacy_manager_controller
import pharmacy.View.pharmacy_manager_views as pharmacy_manager_views


urlpatterns = [
    path('create/', pharmacy_manager_controller.create_new_pharmacy_manager, name='create_pharmacy_manager'),
    path('delete/', pharmacy_manager_controller.delete_pharmacy_manager, name='delete_pharmacy_manager'),
    path('update/', pharmacy_manager_controller.update_pharmacy_manager, name='update_pharmacy_manager'),
    path('get/', pharmacy_manager_controller.get_pharmacy_manager, name='get_pharmacy_manager'),
    path('login/', pharmacy_manager_controller.login_pharmacy_manager, name='login_pharmacy_manager'),
    path('logout/', pharmacy_manager_controller.logout_pharmacy_manager, name='logout_pharmacy_manager'),
    path('dashboard/', pharmacy_manager_views.pharmacy_manager_dashboard, name='pharmacy_manager_dashboard'),
]