from django.http import  JsonResponse, HttpResponseRedirect
import pharmacy.DataBaseService.pharmacy_manager_service as pharmacy_manager_service
from django.views.decorators.csrf import csrf_exempt
from pharmacy.models import PharmacyManager, Admin
from django.shortcuts import render, redirect
import pharmacy.Utils.location_utils as location_utils



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
            address = request.POST.get('address')

            if not all([first_name, last_name, email, password, pharmacy_name, address]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            location_result = location_utils.verify_location(address)

            if not location_result['success']:
                return JsonResponse({
                    "error": f"Could not verify address: {location_result['error']}"
                }, status=400)

            new_manager = pharmacy_manager_service.create_pharmacy_manager(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                phone_number=phone_number,
                pharmacy_name=pharmacy_name,
                latitude=location_result['latitude'],
                longitude=location_result['longitude'],
                city=location_result['city'],
            )

            request.session['manager_id'] = new_manager.pharmacy_id
            return HttpResponseRedirect('/pharmacy_manager/dashboard/')

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "error": str(e)
            }, status=500)

    return render(request, 'signup.html')


@csrf_exempt
def delete_pharmacy_manager(request,manager_id):
    if request.method == 'POST':
        try:
            if not manager_id:
                return JsonResponse({"error": "manager_id is required."}, status=400)

            pharmacy_manager_service.delete_pharmacy_manager(manager_id)

            return redirect('admin_managers_dashboard')

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)


def update_pharmacy_manager(request):
    if request.method == 'POST':
        try:
            manager_id = request.session.get('manager_id')
            if not manager_id:
                return redirect('login')

            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            pharmacy_name = request.POST.get('pharmacy_name')
            pharmacy_address = request.POST.get('pharmacy_address')

            location_result = location_utils.verify_location(pharmacy_address)
            latitude = location_result['latitude']
            longitude = location_result['longitude']
            city = location_result['city']

            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')

            pharmacy_manager_service.update_pharmacy_manager(manager_id,first_name,last_name,email,pharmacy_name,phone_number,current_password,new_password,latitude,longitude,city)
            return redirect('pharmacy_manager_dashboard')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_pharmacy_manager(request):
    if request.method == 'GET':
        try:
            manager_id = request.GET.get('manager_id')
            address = request.GET.get('address')

            if address:
                if len(address.strip()) == 0:
                    return JsonResponse({
                        'success': False,
                        'error': 'address cannot be empty'
                    })
                address_data = location_utils.verify_location(address)
                if not address_data:
                    return JsonResponse({
                        'success': False,
                        'error': 'address cannot be empty'
                    })

                city = address_data['city']
                user_latitude = address_data['latitude']
                user_longitude = address_data['longitude']

                pharmacies = pharmacy_manager_service.get_pharmacy_by_city(city,user_latitude,user_longitude)
                return render(request, 'home_page.html', {
                    'pharmacies': pharmacies,
                    'searched_city': address
                })

            if manager_id:
                manager = pharmacy_manager_service.get_pharmacy_manager(manager_id)
                return JsonResponse({
                    'success': True,
                    'manager': manager
                })

            managers = pharmacy_manager_service.get_pharmacy_manager()
            return JsonResponse({
                'success': True,
                'managers': managers
            })

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

    return JsonResponse({
        "success": False,
        "error": "Method not allowed"
    }, status=405)


def login(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                return JsonResponse({"error": "Email and password are required."}, status=400)

            try:
                admin = Admin.objects.get(email=email)
                if password == admin.password:
                    request.session['admin_id'] = admin.id
                    request.session['user_type'] = 'admin'
                    return HttpResponseRedirect('/admin/dashboard/managers')
                else:
                    return render(request, 'login.html', {'error': 'Invalid password'})

            except Admin.DoesNotExist:
                try:
                    manager = PharmacyManager.objects.get(email=email)
                    if password == manager.password:
                        request.session['manager_id'] = manager.pharmacy.id
                        request.session['user_type'] = 'manager'
                        return HttpResponseRedirect('/pharmacy_manager/dashboard/')
                    else:
                        return render(request, 'login.html', {'error': 'Invalid password'})

                except PharmacyManager.DoesNotExist:
                    return render(request, 'login.html', {'error': 'Invalid email'})

        except Exception as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')




@csrf_exempt
def logout(request):
    try:
        request.session.flush()
        return redirect('homepage')
    except Exception as e:
        print(f"Error during logout: {e}")
        return redirect('homepage')



def get_all_pharmacy_managers(request):
    try:
        if request.session.get('user_type') != 'admin':
            return redirect('login')

        pharmacy_managers = pharmacy_manager_service.get_pharmacy_manager()
        return render(request, 'admin_managers_dashboard.html', {
            'pharmacy_managers': pharmacy_managers
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)