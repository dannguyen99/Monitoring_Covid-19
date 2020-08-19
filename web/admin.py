from django.contrib import admin
from .models import JhuData, VnData, EcdcData, WhoData
# Register your models here.
admin.site.register(EcdcData)
admin.site.register(JhuData)
admin.site.register(VnData)
admin.site.register(WhoData)