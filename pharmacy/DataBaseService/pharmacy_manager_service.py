from django.http import JsonResponse

from pharmacy.models import PharmacyManager, PharmacyDrug
from pharmacy.models import Pharmacy
from pharmacy.constants import ROLE_PHARMACY_MANAGER
import pharmacy.Utils.location_utils as location_utils

def create_pharmacy_manager(first_name, last_name, email, password, phone_number, pharmacy_name,latitude,longitude,city):
    try:
        new_pharmacy = Pharmacy(
            name=pharmacy_name,
            latitude=latitude,
            longitude=longitude,
            city=city,
        )
        new_pharmacy.save()

        new_manager = PharmacyManager.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=ROLE_PHARMACY_MANAGER,
            phone_number=phone_number,
            password=password,
            pharmacy=new_pharmacy,
        )

        new_manager.save()

        return new_manager
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


def update_pharmacy_manager(manager_id,first_name,last_name,email,pharmacy_name,phone_number,current_password,new_password,latitude,longitude,city):

    manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
    pharmacy = manager.pharmacy

    manager.first_name = first_name
    manager.last_name = last_name
    manager.email = email
    manager.phone_number = phone_number

    if current_password and new_password:
        if current_password == manager.password:
            manager.password = new_password
        else:
            return JsonResponse({"error": "Current password is incorrect"}, status=400)

    pharmacy.name = pharmacy_name
    pharmacy.latitude = latitude
    pharmacy.longitude = longitude
    pharmacy.city = city

    pharmacy.name = pharmacy_name

    pharmacy.save()
    manager.save()


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
                    "pharmacy_id": manager.pharmacy_id,
                    "drugs_count": PharmacyDrug.objects.filter(id=manager.pharmacy_id).count()
                }
                for manager in managers
            ]
    except PharmacyManager.DoesNotExist:
        raise Exception(f"Pharmacy Manager with ID {manager_id} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        raise e




def get_pharmacy_by_city(city,user_latitude,user_longitude):
    try:
        pharmacy_managers = PharmacyManager.objects.select_related('pharmacy').filter(
            pharmacy__city__iexact=city
        )

        if not pharmacy_managers:
            return JsonResponse({
                'success': False,
                'message': f'No pharmacies found in {city}'
            })

        pharmacy_list = []
        for manager in pharmacy_managers:
            distance = location_utils.calculate_street_distance(manager.pharmacy.latitude,manager.pharmacy.longitude , user_latitude, user_longitude)
            pharmacy_list.append({
                'pharmacy_id': manager.pharmacy.id,
                'pharmacy_name': manager.pharmacy.name,
                'pharmacy_city': manager.pharmacy.city,
                'distance': distance,
                'manager_name': f"{manager.first_name} {manager.last_name}",
                'manager_phone': manager.phone_number,
                'manager_email': manager.email
            })
        pharmacy_list = location_utils.sort_pharmacies_by_distance(pharmacy_list)
        return pharmacy_list

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

