from django.contrib import admin
from .models import Form, Response, ChartsSettings
# Register your models here.
admin.site.register(Form)
admin.site.register(Response)
admin.site.register(ChartsSettings)
