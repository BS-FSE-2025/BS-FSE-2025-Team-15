from django.contrib.auth.hashers import make_password

from pharmacy.models import PharmacyManager
from pharmacy.models import Pharmacy
from pharmacy.constants import ROLE_PHARMACY_MANAGER


def create_pharmacy_manager(first_name, last_name, email, password, phone_number, pharmacy_name,latitude,longitude):
    try:
        new_pharmacy = Pharmacy(
            name=pharmacy_name,
            latitude=latitude,
            longitude=longitude,
        )
        new_pharmacy.save()

        new_manager = PharmacyManager.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=ROLE_PHARMACY_MANAGER,
            phone_number=phone_number,
            password=make_password(password),
            pharmacy=new_pharmacy,
        )

        new_manager.save()
    except Exception as e:
        print(f"Error: {e}")
        raise e



def delete_pharmacy_manager(manager_id):
    try:
        manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
        pharmacy = manager.pharmacy
        manager.delete()
        pharmacy.delete()
        return f"Pharmacy Manager with ID {manager_id} deleted successfully."
    except PharmacyManager.DoesNotExist:
        raise Exception(f"Pharmacy Manager with ID {manager_id} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        raise e


def update_pharmacy_manager(manager_id, updated_manager_details, updated_pharmacy_details):
    try:
        manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
        if not manager:
            return {"error": "manager not found"}

        for key, value in updated_manager_details.items():
            if hasattr(manager, key):
                setattr(manager, key, value)

        pharmacy = manager.pharmacy
        for key, value in updated_pharmacy_details.items():
            if hasattr(pharmacy, key):
                setattr(pharmacy, key, value)

        pharmacy.save()
        manager.save()

        return manager
    except PharmacyManager.DoesNotExist:
        raise Exception(f"Pharmacy Manager with ID {manager_id} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        raise e



def get_pharmacy_manager(manager_id=None):
    try:
        if manager_id:
            manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
            return {
                "first_name": manager.first_name,
                "last_name": manager.last_name,
                "email": manager.email,
                "role": manager.role,
                "phone_number": manager.phone_number,
                "pharmacy": {
                    "name": manager.pharmacy.name,
                    "latitude": manager.pharmacy.latitude,
                    "longitude": manager.pharmacy.longitude,
                },
            }
        else:
            managers = PharmacyManager.objects.all()
            return [
                {
                    "first_name": manager.first_name,
                    "last_name": manager.last_name,
                    "email": manager.email,
                    "role": manager.role,
                    "phone_number": manager.phone_number,
                    "pharmacy": {
                        "name": manager.pharmacy.name,
                        "latitude": manager.pharmacy.latitude,
                        "longitude": manager.pharmacy.longitude,
                    },
                }
                for manager in managers
            ]
    except PharmacyManager.DoesNotExist:
        raise Exception(f"Pharmacy Manager with ID {manager_id} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        raise e
