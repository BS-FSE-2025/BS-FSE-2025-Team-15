from django.db import models
from pharmacy.constants import Roles
from django.utils.timezone import now

class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class PharmacyManager(models.Model):
    first_name = models.CharField(max_length=150, unique=True)
    last_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=Roles, default='guest')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    pharmacy = models.OneToOneField(Pharmacy, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.first_name} owns {self.pharmacy.name}"



class Guest(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"your Location is {self.latitude,self.longitude}"



class Drug(models.Model):
    name = models.CharField(max_length=255)
    official_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class PharmacyDrug(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="drugs")
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.drug.name} in {self.pharmacy.name}"


