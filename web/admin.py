from django.contrib import admin
from .models import Table, JhuData, VnData
# Register your models here.
admin.site.register(Table)
admin.site.register(JhuData)
admin.site.register(VnData)