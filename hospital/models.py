from django.db import models
from decimal import Decimal


class Doctor(models.Model):
    doctor_id = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    qualification = models.CharField(max_length=50, default="Not Available") 
    department = models.CharField(max_length=50)
    special = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Patient(models.Model):
    ROOM_TYPES = [
        ('General Ward', 'General Ward'),
        ('Emergency', 'Emergency'),
        ('Super Speciality', 'Super Speciality'),
        ('Luxury', 'Luxury'),
    ]

    patient_id = models.PositiveIntegerField(unique=True, editable=False, null=True, blank=True)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=18)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    issue = models.CharField(max_length=255)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES, default='General Ward')
    room_number = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField()
    time1 = models.TimeField()

    def __str__(self):
        return self.doctor.name + "--" + self.patient.name
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    wait_time = models.IntegerField(default=0)
    facility_quality = models.IntegerField(default=0)
    treatment_quality = models.IntegerField(default=0)
    staff_behavior = models.IntegerField(default=0)
    additional_feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    shift = models.CharField(max_length=100)
    availability = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Busy', 'Busy')], default='Available')

    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    occupation = models.CharField(max_length=100)
    shift = models.CharField(max_length=50)
    availability = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Busy', 'Busy')])

    def __str__(self):
        return self.name

class Bill(models.Model):
    patient = models.OneToOneField("Patient", on_delete=models.CASCADE)
    diagnosis_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('2000.00'))
    scan_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1500.00'))
    medicine_charge = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    gst = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    ROOM_PRICING = {
        "General Ward": Decimal('1000.00'),
        "Emergency": Decimal('8000.00'),
        "Super Speciality": Decimal('3000.00'),
        "Luxury": Decimal('5000.00'),
    }

    def get_room_charge(self):
        return self.ROOM_PRICING.get(self.patient.room_type, Decimal('1000.00'))

    def calculate_total(self):
        room_charge = self.get_room_charge()
        base_total = room_charge + self.diagnosis_charge + self.scan_charge + self.medicine_charge
        tax = base_total * (self.gst / Decimal('100'))
        return base_total + tax

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for {self.patient.name} - ₹{self.total_amount}"
