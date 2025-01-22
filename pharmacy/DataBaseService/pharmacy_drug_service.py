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

        pharmacy_drug, created = PharmacyDrug.objects.get_or_create(
            pharmacy_id=pharmacy_id,
            drug=drug,
            defaults={"price": price}
        )

        if not created:
            pharmacy_drug.price = price
            pharmacy_drug.save()

    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_name} does not exist in ministry of health")
    except Exception as e:
        raise e


def delete_drug(drug_id):
    try:
        pharmacy_drug = PharmacyDrug.objects.get(id=drug_id)
        drug_name = pharmacy_drug.drug.name
        pharmacy_drug.delete()
        return f"Drug '{drug_name}' deleted successfully."
    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_id} does not exist.")
    except Exception as e:
        print(f"Error deleting drug: {e}")
        raise e


def update_drug_and_pharmacy_drug(drug_id, price, pharmacy_id):
    try:
        print("drug_id:", drug_id)
        print("pharmacy_id:", pharmacy_id)

        pharmacy_drug = PharmacyDrug.objects.get(
            id=drug_id,
            pharmacy_id=pharmacy_id
        )

        print(pharmacy_drug.drug.name)
        if pharmacy_drug:
            if price:
                pharmacy_drug.price = price
            pharmacy_drug.save()
            return "Drug and PharmacyDrug updated successfully."

    except PharmacyDrug.DoesNotExist:
        raise Exception("PharmacyDrug record does not exist for the specified Drug and Pharmacy.")
    except Exception as e:
        print(f"Error: {e}")
        raise e


def get_drug_and_pharmacy_drug(drug_id=None,pharmacy_id=None,search_query=None):
    try:
        if drug_id:
            # Single drug case
            pharmacy_drug = PharmacyDrug.objects.select_related('drug', 'pharmacy').get(id=drug_id)
            return {
                'id': pharmacy_drug.id,
                'drug': {
                    'id': pharmacy_drug.drug.id,
                    'name': pharmacy_drug.drug.name,
                    'official_price': pharmacy_drug.drug.official_price,
                },
                'price': pharmacy_drug.price,
                'updated_at': pharmacy_drug.updated_at
            }
        else:
            # Get all pharmacy drugs with related drug info
            query = PharmacyDrug.objects.select_related('drug', 'pharmacy')

            if pharmacy_id:
                query = query.filter(pharmacy_id=pharmacy_id)

            if search_query:
                query = query.filter(drug__name__icontains=search_query)

            return [
                {
                    'id': pd.id,
                    'drug': {
                        'id': pd.drug.id,
                        'name': pd.drug.name,
                        'official_price': pd.drug.official_price,
                    },
                    'price': pd.price,
                    'updated_at': pd.updated_at
                }
                for pd in query
            ]

    except PharmacyDrug.DoesNotExist:
        raise Exception(f"Drug not found.")
    except Exception as e:
        print(f"Error: {e}")
        raise e

def get_drugs_by_query_search(search_query, pharmacy_id):
    try:
        if pharmacy_id:
            pharmacy_drugs = PharmacyDrug.objects.filter(pharmacy_id=pharmacy_id)
            if search_query:
                drugs = pharmacy_drugs.filter(name__icontains=search_query)
                return drugs
            else:
                return pharmacy_drugs
    except Exception as e:
        print(f"Error: {e}")
        raise e



