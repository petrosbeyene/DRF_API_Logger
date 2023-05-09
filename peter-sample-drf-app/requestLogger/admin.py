from django.contrib import admin
from .models import APIRequestLog, ModelChangeLog

# Register your models here.
admin.site.register(APIRequestLog)
admin.site.register(ModelChangeLog)