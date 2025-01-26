from pharmacy.models import Drug


def create_new_drug(drug_name,official_price):
    try:
        new_drug = Drug.objects.create(
            name=drug_name,
            official_price=official_price,
        )
        new_drug.save()
        return "Drug created successfully."
    except Exception as e:
        raise e



def delete_drug_by_id(drug_id):
    try:
        drug = Drug.objects.get(id=drug_id)
        drug_name = drug.name
        drug.delete()
        return f"Drug '{drug_name}' deleted successfully."
    except Drug.DoesNotExist:
        raise Exception(f"Drug with ID {drug_id} does not exist.")
    except Exception as e:
        print(f"Error deleting drug: {e}")
        raise e


def edit_drug_by_id(drug_id, drug_name,drug_price):
    try:
        drug = Drug.objects.get(id=drug_id)
        if all([drug,drug_name,drug_price]):
            drug.name = drug_name
            drug.official_price = drug_price
            drug.save()
            return "Drug updated successfully."

    except Exception as e:
        print(f"Error: {e}")
        raise e


def get_drugs(drug_id=None):
    try:
        if drug_id:
            drug = Drug.objects.get(id=drug_id)
            if drug:
                return drug
        else:
            all_drugs = Drug.objects.all()
            return all_drugs
    except Exception as e:
        raise e
