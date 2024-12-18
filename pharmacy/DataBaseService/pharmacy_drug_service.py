from pharmacy.models import Drug, PharmacyDrug, Pharmacy


def create_drug(drug_details):
    try:
        new_drug = Drug.objects.create(
            name=drug_details['name'],
            official_price=drug_details['official_price'],
        )
        new_drug.save()
        return "Drug created successfully."
    except Exception as e:
        raise e

def add_pharmacy_drug(pharmacy_id, drug_name, price):
    try:
        drug = Drug.objects.get(name=drug_name)
        if not drug:
            return {"message": "drug does not exist, ask the admin to add it"}

        PharmacyDrug.objects.create(
            pharmacy_id=pharmacy_id,
            drug=drug,
            price=price
        )

    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_name} does not exist in ministry of health")
    except Exception as e:
        raise e

def delete_drug(drug_id):
    try:
        drug = Drug.objects.get(id=drug_id)
        drug.delete()
        return f"Drug with ID {drug_id} deleted successfully."
    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_id} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        raise e


def update_drug_and_pharmacy_drug(drug_id, price, pharmacy_id):
    try:
        pharmacy_drug = PharmacyDrug.objects.get(drug_id=drug_id, pharmacy_id=pharmacy_id)
        if pharmacy_drug:
            if price:
                pharmacy_drug.price = price
            pharmacy_drug.save()
            return "Drug and PharmacyDrug updated successfully."

    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_id} does not exist.")
    except PharmacyDrug.DoesNotExist:
        raise Exception("PharmacyDrug record does not exist for the specified Drug and Pharmacy.")
    except Exception as e:
        print(f"Error: {e}")
        raise e


def get_drug_and_pharmacy_drug(drug_id=None):
    try:
        if drug_id:
            drug = Drug.objects.get(id=drug_id)
            pharmacy_drugs = PharmacyDrug.objects.filter(drug=drug)

            return {
                "drug": {
                    "id": drug.id,
                    "name": drug.name,
                    "official_price": drug.official_price,
                },
                "pharmacy_drugs": [
                    {
                        "pharmacy_id": pd.pharmacy.id,
                        "pharmacy_name": pd.pharmacy.name,
                        "price": pd.price,
                        "updated_at": pd.updated_at,
                    }
                    for pd in pharmacy_drugs
                ],
            }
        else:
            drugs = Drug.objects.all()
            return [
                {
                    "id": drug.id,
                    "name": drug.name,
                    "official_price": drug.official_price,
                }
                for drug in drugs
            ]
    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_id} does not exist.")
    except Exception as e:
        print(f"Error: {e}")
        raise e
