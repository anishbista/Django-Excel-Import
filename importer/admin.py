from django.contrib import admin
from .models import ImportJob, ImportLog

admin.site.register([ImportJob, ImportLog])
