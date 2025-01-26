from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
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
def delete_drug(request, drug_id):
    try:
        pharmacy_drug_service.delete_drug(drug_id)
        return HttpResponseRedirect('/pharmacy_manager/dashboard/')
    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def update_drug(request, drug_id):
    if request.method == 'POST':
        try:
            pharmacy_id = request.session.get('manager_id')
            price = request.POST.get('price')
            print(pharmacy_id,drug_id,price)
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
            search_query = request.GET.get('search', '')
            pharmacy_id = request.GET.get('pharmacy_id')
            manager_id = request.session.get('manager_id')

            # Get the pharmacy data
            pharmacy = PharmacyManager.objects.get(pharmacy_id=pharmacy_id)

            # Get drugs data
            if drug_id:
                drugs = [pharmacy_drug_service.get_drug_and_pharmacy_drug(drug_id)]
            else:
                drugs = pharmacy_drug_service.get_drug_and_pharmacy_drug(
                    pharmacy_id=pharmacy_id,
                    search_query=search_query
                )

            context = {
                'drugs': drugs,
                'pharmacy_id': pharmacy_id,
                'pharmacy_name': pharmacy.pharmacy.name,
                'first_name': {pharmacy.first_name},
                'last_name':  {pharmacy.last_name},
                "latitude":  pharmacy.pharmacy.latitude,
                "longitude": pharmacy.pharmacy.longitude,
            }

            return render(request, 'pharmacy_manager_dashboard.html', context)

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)





def drug_search(search_query,pharmacy_id):
    if search_query:
        drugs = pharmacy_drug_service.get_drugs_by_query_search(search_query,pharmacy_id)
        return drugs