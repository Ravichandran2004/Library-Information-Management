from django.contrib import admin
from lims_app.models import APIRequestLog  # ✅ FIXED

admin.site.register(APIRequestLog)
