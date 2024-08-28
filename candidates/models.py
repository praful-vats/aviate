from django.db import models

# Create your models here.

class Candidate(models.Model):
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    years_of_exp = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    current_salary = models.DecimalField(max_digits=10, decimal_places=2)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.name
