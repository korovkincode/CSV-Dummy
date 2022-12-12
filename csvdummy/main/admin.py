from django.contrib import admin
from .models import DataScheme, DataSchemeColumn, DataSet

admin.site.register(DataScheme)
admin.site.register(DataSchemeColumn)
admin.site.register(DataSet)