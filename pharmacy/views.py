
# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


import os
import numpy as np
from django.conf import settings
import pandas as pd
from django.http import HttpResponse
from pharmacy.models import Drug

def import_drugs_from_excel(request):
    if request.method == "POST":
        # Path to the uploaded file (adjust path using BASE_DIR)
        file_path = os.path.join(settings.BASE_DIR, 'Drugs.xlsx')

        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            df = df.fillna(10)

            # Assuming the Excel file has columns: 'name' and 'official_price'
            for _, row in df.iterrows():
                # Create a new Drug object for each row
                drug = Drug(
                    name=row['שם תכשיר'],
                    official_price=row['אחוז מרווח לקמעונאי']
                )
                # Save the object to the database
                drug.save()

            # Return success message
            return HttpResponse("Data imported successfully!")

        except Exception as e:
            return HttpResponse(f"Error importing data: {e}")
    else:
        return HttpResponse("Invalid request method.")
