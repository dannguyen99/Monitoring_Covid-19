from django.contrib import admin
from .models import JhuData, VnData, EcdcData
# Register your models here.
admin.site.register(EcdcData)
admin.site.register(JhuData)
admin.site.register(VnData)