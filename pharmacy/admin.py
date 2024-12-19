from django.contrib import admin
from .models import PharmacyManager
from .models import Pharmacy
from .models import Drug
from .models import Guest
from .models import PharmacyDrug

admin.site.register(PharmacyManager)
admin.site.register(Pharmacy)
admin.site.register(Drug)
admin.site.register(Guest)
admin.site.register(PharmacyDrug)
