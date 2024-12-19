from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
import pharmacy.DataBaseService.pharmacy_drug_service as pharmacy_drug_service
from pharmacy.models import PharmacyManager


@csrf_exempt
def add_pharmacy_drug(request):
    if request.method == 'POST':
        try:
            manager_id = request.session.get('manager_id')
            if not manager_id:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
            drug_name = request.POST.get('drug_name')
            price = request.POST.get('price')
            print(drug_name, price)
            if not drug_name or not price:
                return JsonResponse({'error': 'Drug name and price are required'}, status=400)

            pharmacy_drug_service.add_pharmacy_drug(manager.pharmacy_id, drug_name, price)
            return HttpResponseRedirect('/pharmacy_manager/dashboard/')
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Failed to add drug'}, status=500)


@csrf_exempt
def create_drug(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            drug_details = data.get('drug_details')

            if not drug_details:
                return JsonResponse({"error": "drug_details and pharmacy_drug_details are required."}, status=400)

            pharmacy_drug_service.create_drug(drug_details)

            return JsonResponse({"message": "Drug created successfully!"}, status=201)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_drug(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            drug_id = data.get('drug_id')

            if not drug_id:
                return JsonResponse({"error": "drug_id is required."}, status=400)

            pharmacy_drug_service.delete_drug(drug_id)

            return JsonResponse({"message": "Drug and related PharmacyDrug deleted successfully!"}, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_drug(request):
    if request.method == 'PUT':
        try:
            pharmacy_id = request.session.get('manager_id')
            drug_id = request.PUT.get('id')
            price = request.PUT.get('price')
            pharmacy_drug_service.update_drug_and_pharmacy_drug(drug_id, price, pharmacy_id)
            return HttpResponseRedirect('/pharmacy_manager/dashboard/')

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_drug(request):
    if request.method == 'GET':
        try:
            drug_id = request.GET.get('drug_id')

            if drug_id:
                drug = pharmacy_drug_service.get_drug_and_pharmacy_drug(drug_id)
                return JsonResponse(drug, safe=False, status=200)

            drugs = pharmacy_drug_service.get_drug_and_pharmacy_drug()
            return JsonResponse(drugs, safe=False, status=200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)
