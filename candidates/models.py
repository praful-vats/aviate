from django.db import models
from django.core.exceptions import ValidationError

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

    def clean(self):
        if self.expected_salary < self.current_salary:
            raise ValidationError('Expected salary cannot be less than current salary.')
        if self.age < 18 or self.age > 120:
            raise ValidationError('Age must be between 18 and 120.')
        if self.years_of_exp < 0:
            raise ValidationError('Years of experience cannot be negative.')

    def save(self, *args, **kwargs):
        self.clean() 
        super().save(*args, **kwargs)
