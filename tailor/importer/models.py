from django.db import models

# Create your models here.
# importer/models.py
from django.db import models
from api.models import Company
from django.utils import timezone

class ImportSession(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    STEP_CHOICES = [
        ('clients', 'Clients'),
        ('maap', 'Maap'),
        ('bills', 'Bills'),
        ('products', 'Products'),
        ('done', 'Done'),
    ]

    current_step = models.CharField(
        max_length=20,
        choices=STEP_CHOICES,
        default='clients'
    )

    is_locked = models.BooleanField(default=False)  # prevents re-upload
    last_error = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.company} | {self.current_step}"
