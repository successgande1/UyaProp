from django.db import models

# Create your models here.
class Contact(models.Model):
    SUBJECT_CHOICES = [
        ('Inquiry', 'Inquiry'),
    ]
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=35, blank=True, null=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    phone = models.CharField(max_length=11, blank=True, null=True)
    content = models.TextField(max_length=220, blank=True, null=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'