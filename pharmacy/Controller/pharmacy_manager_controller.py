from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
import pharmacy.DataBaseService.pharmacy_manager_service as pharmacy_manager_service
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from pharmacy.models import PharmacyManager
from django.shortcuts import render, redirect


@csrf_exempt
def create_new_pharmacy_manager(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            pharmacy_name = request.POST.get('pharmacy_name')
            phone_number = request.POST.get('phone_number')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')

            if not all([first_name, last_name, email, password, pharmacy_name]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            pharmacy_manager_service.create_pharmacy_manager(first_name, last_name, email, password, phone_number, pharmacy_name,latitude,longitude)

            return JsonResponse({"message": "Pharmacy Manager created successfully!"}, status=201)

        except Exception as e:
            print(f"Error: {e}")
            raise e
    return render(request, 'signup.html')


@csrf_exempt
def delete_pharmacy_manager(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            manager_id = request.DELETE.get('manager_id')

            if not manager_id:
                return JsonResponse({"error": "manager_id is required."}, status=400)

            pharmacy_manager_service.delete_pharmacy_manager(manager_id)

            return JsonResponse({"message": "Pharmacy Manager deleted successfully!"}, status=200)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def update_pharmacy_manager(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            manager_id = request.PUT.get('manager_id')
            manager_details = request.PUT.get('manager_details')
            pharmacy_details = request.PUT.get('pharmacy_details')

            if not manager_id or not manager_details or not pharmacy_details:
                return JsonResponse({"error": "manager_id, manager_details, and pharmacy_details are required."}, status=400)

            pharmacy_manager_service.update_pharmacy_manager(manager_id, manager_details, pharmacy_details)

            return JsonResponse({"message": "Pharmacy Manager updated successfully!"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_pharmacy_manager(request):
    if request.method == 'GET':
        try:
            manager_id = request.GET.get('manager_id')

            if manager_id:
                manager = pharmacy_manager_service.get_pharmacy_manager(manager_id)
                return JsonResponse(manager, safe=False, status=200)

            managers = pharmacy_manager_service.get_pharmacy_manager()
            return JsonResponse(managers, safe=False, status=200)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def login_pharmacy_manager(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            try:
                manager = PharmacyManager.objects.get(email=email)
            except PharmacyManager.DoesNotExist:
                return JsonResponse({"error": "Invalid email or password."}, status=401)

            if not check_password(password, manager.password):
                return JsonResponse({"error": "Invalid email or password."}, status=401)

            request.session['manager_id'] = manager.pharmacy_id
            return HttpResponseRedirect('/pharmacy_manager/dashboard/')

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    return render(request, 'login.html')


@csrf_exempt
def logout_pharmacy_manager(request):
    if request.method == 'POST':
        try:
            if 'manager_id' in request.session:
                del request.session['manager_id']
                return JsonResponse({"message": "Logout successful!"}, status=200)
            else:
                return JsonResponse({"error": "Not logged in."}, status=400)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)