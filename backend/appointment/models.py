from django.db import models

# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.PROTECT, related_name='appointments')
    patient = models.ForeignKey('patient.Patient', on_delete=models.PROTECT, related_name='appointments')
    date = models.DateField()
    time_slot=models.CharField(max_length=10)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return self
    class Meta:
        ordering = ['-date']
        unique_together = ['doctor', 'date', 'time_slot']
