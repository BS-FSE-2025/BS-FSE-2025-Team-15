from django.shortcuts import render, redirect
from pharmacy.models import PharmacyDrug, PharmacyManager

def pharmacy_manager_dashboard(request):
    manager_id = request.session.get('manager_id')
    if not manager_id:
        return redirect('login_pharmacy_manager')

    manager = PharmacyManager.objects.get(pharmacy_id=manager_id)
    drugs = PharmacyDrug.objects.filter(pharmacy_id=manager.pharmacy_id)

    return render(request, 'pharmacy_manager_dashboard.html', {
        'manager_name': f"{manager.first_name} {manager.last_name}",
        'pharmacy_name': manager.pharmacy.name,
        'drugs': drugs
    })
