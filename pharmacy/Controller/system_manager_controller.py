import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_system_manager(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"error": "Username and password are required."}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return JsonResponse({"message": "System manager logged in successfully!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials or not a system manager."}, status=401)

# @csrf_exempt
# def logout_system_manager(request):
#     if request.method == 'POST':
#         try:
#             logout(request)
#             return JsonResponse({"message": "System manager logged out successfully!"}, status=200)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
