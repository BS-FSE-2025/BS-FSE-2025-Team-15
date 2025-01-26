from django.urls import path
import pharmacy.Controller.request_controller as request_controller



urlpatterns = [
    path('newRequest/', request_controller.Request, name='create_new_request'),
    path('deleteRequest/<int:Request>/', request_controller.Request, name='delete_request'),
    path('editRequest/', request_controller.Request, name='edit_request'),
    path('dashboard/requests', request_controller.Request, name='admin_requests_dashboard'),
]