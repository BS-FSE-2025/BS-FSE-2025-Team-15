
from pharmacy.models import Request
from pharmacy.models import PharmacyManager
from random import choice
from string import ascii_uppercase, digits


def create_new_request(content,manager_id):
    try:
        new_request = Request.objects.create(
            content=content,
            manager_id=manager_id,
            status='PENDING'
        )
        new_request.save()
        return "Request created successfully."
    except Exception as e:
        raise e


def reset_password_request(email):
    try:
        manager = PharmacyManager.objects.get(email=email)
        content = (f"Password reset request from {manager.first_name} {manager.last_name}."
                   f" Manager ID: {manager.pharmacy_id}, Email: {email}. Please verify identity and process password reset.")

        temporary_password = ''.join(choice(ascii_uppercase + digits) for i in range(12))
        new_request = Request.objects.create(
            content=content,
            manager_id=manager.pharmacy_id,
            status='PENDING'
        )
        new_request.save()

        manager.password = temporary_password
        manager.save()
        return temporary_password
    except Exception as e:
        raise e



def delete_request_by_id(request_id):
    try:
        request = Request.objects.get(id=request_id)
        request.delete()
        return f"Drug request deleted successfully."
    except Request.DoesNotExist:
        raise Exception(f"request with ID {request_id} does not exist.")
    except Exception as e:
        print(f"Error deleting request: {e}")
        raise e


def edit_request_by_id(request_id, content ,status):
    try:
        request = Request.objects.get(id=request_id)
        if content:
            request.content = content
        if status:
            request.status = status

        request.save()
        return "Request updated successfully."

    except Exception as e:
        print(f"Error: {e}")
        raise e


def get_requests(request_id=None):
    try:
        if request_id:
            request = Request.objects.get(id=request_id)
            if request:
                return request
        else:
            all_requests = Request.objects.all()
            return all_requests
    except Exception as e:
        raise e



def get_requests_by_manager(manager_id=None):
    try:
        if manager_id:
            return Request.objects.filter(manager_id=manager_id).order_by('-created_at')

    except Exception as e:
        raise e
