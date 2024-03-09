from django.db import models

# Create your models here.
from django.db import models

class ExcelData(models.Model):
    data = models.JSONField()