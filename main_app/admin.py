from django.contrib import admin

from .models import Device, UsageSession, Accessory

# Register your models here
admin.site.register(Device)
admin.site.register(UsageSession)
admin.site.register(Accessory)