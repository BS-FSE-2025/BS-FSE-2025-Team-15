from django.shortcuts import render, redirect
from pharmacy.models import PharmacyDrug, PharmacyManager
from pharmacy.Controller.pharmacy_drug_controller import drug_search

def pharmacy_manager_dashboard(request):
    if request.session.get('user_type') != 'manager':
        return redirect('login')
    manager_id = request.session.get('manager_id')
    if manager_id:
        manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
        drugs = PharmacyDrug.objects.filter(pharmacy_id=manager.pharmacy_id)
        return render(request, 'pharmacy_manager_dashboard.html', {
            'manager_name': f"{manager.first_name} {manager.last_name}",
            'first_name': manager.first_name,
            'last_name': manager.last_name,
            'email': manager.email,
            'pharmacy_address': manager.pharmacy.city,
            'pharmacy_name': manager.pharmacy.name,
            'drugs': drugs,
            'role': manager.role,
            "latitude": manager.pharmacy.latitude,
            "longitude": manager.pharmacy.longitude,
            "phone": manager.phone_number
        })



def pharmacy_dashboard_to_user(request, pharmacy_id):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        print(search_query)
        if pharmacy_id:
            manager = PharmacyManager.objects.get(pharmacy_id=pharmacy_id)
            if search_query:
                drugs = drug_search(search_query,pharmacy_id)
                print(drugs)
            else:
                drugs = PharmacyDrug.objects.filter(pharmacy_id=manager.pharmacy_id)
                print(drugs)

            return render(request, 'pharmacy_manager_dashboard.html', {
                'manager_name': f"{manager.first_name} {manager.last_name}",
                'pharmacy_name': manager.pharmacy.name,
                'drugs': drugs,
                'pharmacy_id': manager.pharmacy_id,
                "latitude": manager.pharmacy.latitude,
                "longitude": manager.pharmacy.longitude,
            })


