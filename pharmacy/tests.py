from django.test import TestCase

from .Utils.location_utils import calculate_street_distance
from .models import Drug, PharmacyDrug, PharmacyManager, Pharmacy
from pharmacy.DataBaseService.pharmacy_drug_service import add_pharmacy_drug,delete_drug,update_drug_and_pharmacy_drug
from pharmacy.DataBaseService.pharmacy_manager_service import get_pharmacy_manager, delete_pharmacy_manager, \
    get_pharmacy_by_city


class PharmacyServiceTests(TestCase):

    def setUp(self):
        self.drug = Drug.objects.create(name="TestDrug2",official_price=20)
        self.pharmacy = Pharmacy.objects.create(name="TestPharmacy", latitude=0.0, longitude=0.0)
        self.pharmacy_manager = PharmacyManager.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            role="Manager",
            phone_number="1234567890",
            pharmacy=self.pharmacy,
        )
        self.pharmacy_drug = PharmacyDrug.objects.create(
            pharmacy_id=self.pharmacy.id,
            drug=self.drug,
            price=100.0
        )
        self.success_response_data = {
            "features": [{
                "properties": {
                    "city": "כסיפה",
                    "lat": 31.2465374,
                    "lon": 35.0930574,
                    "formatted": "כסיפה, South District, Israel",
                    "country_code": "il"
                }
            }]
        }

    def test_successful_address_lookup(self):
        distance = calculate_street_distance(32.0853,34.7818,31.2521,34.7868)
        print(distance)

    def test_add_pharmacy_drug_success(self):
        response = add_pharmacy_drug(self.pharmacy.id, self.drug.name, 150.0)
        pharmacy_drug = PharmacyDrug.objects.get(pharmacy_id=self.pharmacy.id, drug_id=self.drug.id)
        self.assertEqual(pharmacy_drug.price, 150.0)
        self.assertIsNone(response)

    def test_add_pharmacy_drug_drug_does_not_exist(self):
        with self.assertRaises(Exception) as context:
            add_pharmacy_drug(self.pharmacy.id, "NonExistentDrug", 150.0)
        self.assertIn("Drug with ID NonExistentDrug does not exist", str(context.exception))

    def test_delete_drug_success(self):
        response = delete_drug(self.drug.id)
        self.assertEqual(response, f"Drug with ID {self.drug.id} deleted successfully.")
        with self.assertRaises(Drug.DoesNotExist):
            Drug.objects.get(id=self.drug.id)

    def test_delete_drug_does_not_exist(self):
        with self.assertRaises(Exception) as context:
            delete_drug(9999)
        self.assertIn("Drug with ID 9999 does not exist", str(context.exception))

    def test_update_drug_and_pharmacy_drug_success(self):
        response = update_drug_and_pharmacy_drug(self.drug.id, 200.0, self.pharmacy.id)
        pharmacy_drug = PharmacyDrug.objects.get(drug_id=self.drug.id, pharmacy_id=self.pharmacy.id)
        self.assertEqual(pharmacy_drug.price, 200.0)
        self.assertEqual(response, "Drug and PharmacyDrug updated successfully.")

    def test_get_pharmacy_manager_single(self):
        response = get_pharmacy_manager(self.pharmacy.id)
        self.assertEqual(response["first_name"], self.pharmacy_manager.first_name)
        self.assertEqual(response["last_name"], self.pharmacy_manager.last_name)

    def test_get_pharmacy_manager_all(self):
        response = get_pharmacy_manager()
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["first_name"], self.pharmacy_manager.first_name)

    def test_delete_pharmacy_manager_success(self):
        response = delete_pharmacy_manager(self.pharmacy.id)
        self.assertEqual(response, f"Pharmacy Manager with ID {self.pharmacy.id} deleted successfully.")
        with self.assertRaises(PharmacyManager.DoesNotExist):
            PharmacyManager.objects.get(pharmacy_id=self.pharmacy.id)
        with self.assertRaises(Pharmacy.DoesNotExist):
            Pharmacy.objects.get(id=self.pharmacy.id)

    def test_delete_pharmacy_manager_does_not_exist(self):
        with self.assertRaises(Exception) as context:
            delete_pharmacy_manager(9999)
        self.assertIn("Pharmacy Manager with ID 9999 does not exist", str(context.exception))
