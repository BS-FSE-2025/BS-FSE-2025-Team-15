from django.http import JsonResponse
from django.shortcuts import redirect, render

import pharmacy.DataBaseService.drug_service as drug_service

def create_drug(request):
    if request.method == 'POST':
        try:
            drug_name = request.POST.get('drug_name')
            official_price = request.POST.get('official_price')

            if not all([drug_name, official_price]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            drug_service.create_new_drug(drug_name, official_price)
            return redirect('admin_drugs_dashboard')

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


def delete_drug(request,drug_id):
    if request.method == 'POST':
        try:
            if not drug_id:
                return JsonResponse({"error": "Drug ID is required."}, status=400)

            drug_service.delete_drug_by_id(drug_id)
            return redirect('admin_drugs_dashboard')

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)



def edit_drug(request):
    if request.method == 'POST':
        try:
            drug_id = request.POST.get('drug_id')
            drug_name = request.POST.get('drug_name')
            drug_price = request.POST.get('drug_price')

            print(drug_price,drug_name,drug_id)
            if not all([drug_id, drug_name, drug_price]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            drug_service.edit_drug_by_id(drug_id, drug_name, drug_price)
            return redirect('admin_drugs_dashboard')

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




def admin_dashboard(request):
    try:
        if request.session.get('user_type') != 'admin':
            return redirect('login')

        drugs = drug_service.get_drugs()
        return render(request, 'admin_drug_dashboard.html', {
            'drugs': drugs
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
