from django.http import JsonResponse
from django.shortcuts import redirect, render
import pharmacy.DataBaseService.request_service as request_service
from django.contrib import messages

def create_request(request):
    if request.method == 'POST':
        try:
            content = request.POST.get('content')
            manager_id = request.session.get('manager_id')
            print(manager_id,content)
            if not content or not manager_id:
                return JsonResponse({"error": "Content and manager ID required"}, status=400)
            request_service.create_new_request(content, manager_id)
            return redirect('pharmacy_manager_dashboard')
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



def reset_password(request):
    if request.method == 'GET':
        return render(request, 'reset_password.html')

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            temporary_password = request_service.reset_password_request(email)
            messages.success(request, f"has been reset successfully , Your Temporary Password {temporary_password} ")
            return redirect('login')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('reset_password_request')


def delete_request(request,request_id):
    if request.method == 'POST':
        try:
            request_service.delete_request_by_id(request_id)
            return redirect('admin_request_dashboard')

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



def edit_request(request):
    if request.method == 'POST':
        try:
            request_id = request.POST.get('request_id')
            content = request.POST.get('content')
            status = request.POST.get('status')

            request_service.edit_request_by_id(request_id, content, status)
            if status:
                return redirect('admin_request_dashboard')
            if content:
                return redirect('manager_requests')

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




def admin_dashboard(request):
    try:
        if request.session.get('user_type') != 'admin':
            return redirect('login')

        requests = request_service.get_requests()

        return render(request, 'admin_request_dashboard.html', {
            'requests': requests
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def manager_requests(request):
    try:

        manager_id = request.session.get('manager_id')
        requests = request_service.get_requests_by_manager(manager_id)

        return render(request, 'manager_request_dashboard.html', {
            'requests': requests
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
