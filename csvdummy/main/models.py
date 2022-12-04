from django.db import models
from users.models import Users

class DataScheme(models.Model):
    scheme_id = models.AutoField(primary_key=True)
    modified = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DataSchemeColumn(models.Model):
    TYPES = (('Full name', 'Full name'), ('Job', 'Job'), ('Domain name', 'Domain name'), ('Company name', 'Company name'), ('Address', 'Address'))
    
    name = models.CharField(max_length=70)
    datatype = models.CharField(max_length=15, choices=TYPES)
    datascheme = models.ForeignKey(DataScheme, on_delete=models.CASCADE)

    def __str__(self):
        return self.name