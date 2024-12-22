from django.db import models

# Create your models here.
class PatientHistory(models.Model):
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.PROTECT, related_name='history')
    patient = models.ForeignKey('patient.Patient', on_delete=models.PROTECT, related_name='history')
    remarks = models.TextField()
    prescriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def _str_(self):
        return self
    class Meta:
        ordering = ['-created_at']