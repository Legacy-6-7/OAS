from django.db import models


class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=12)
    course = models.CharField(max_length=30)
    message = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # was `_str_` (single underscores) — Django never called it
        return self.name


class Student(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Document Verified', 'Document Verified'),
        ('Fees Submitted', 'Fees Submitted'),
        ('Enrolled', 'Enrolled'),
        ('Rejected', 'Rejected'),
    ]

    PAYMENT_STATUS = [
        ('verified', 'verified'),
        ('pending', 'pending'),
        ('submitted', 'submitted'),
        ('rejected', 'rejected'),
    ]

    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    mobile = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)

    application_status = models.CharField(
        max_length=20, default='Pending', choices=STATUS_CHOICES
    )

    dob = models.DateField(null=True, blank=True)

    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    father_mobile = models.CharField(max_length=100, null=True, blank=True)
    class10 = models.FloatField(null=True, blank=True)
    class12 = models.FloatField(null=True, blank=True)
    course = models.CharField(max_length=100, null=True, blank=True)
    aadhaar = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    
    aadhaar_photo = models.ImageField(upload_to='applications/', blank=True, null=True)
    student_photo = models.ImageField(upload_to='applications/', blank=True, null=True)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_screenshot = models.ImageField(upload_to='paymentscreenshots/', blank=True, null=True)
    course_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    application_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name or f"Student #{self.student_id}"


class Courses(models.Model):
    courseimg = models.ImageField(upload_to='courses/', blank=True, null=True)
    course_id = models.AutoField(primary_key=True)
    coursename = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    fees = models.CharField(max_length=100)

    def __str__(self):  # was `_str_`
        return self.coursename