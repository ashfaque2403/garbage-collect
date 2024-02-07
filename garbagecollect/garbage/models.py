from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _



class CustomUserManager(BaseUserManager):
    """Define a model manager for CustomUser model with both email and username authentication."""

    def _create_user(self, email, username, password=None, **extra_fields):
        """Create and save a CustomUser with the given email, username, and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a SuperUser with the given email, username, and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_driver = models.BooleanField('Is driver', default=False)
    is_garbagecollector = models.BooleanField('Is garbagecollector', default=False)
    is_companyadmin = models.BooleanField('Is companyadmin', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    


# Create your models here.
class CompanyAdministrator(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),('F', 'Female'),('O', 'Other'),
    ]
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    password = models.CharField(max_length=100)  
    email = models.EmailField(unique=True)
    dob = models.DateField()
    district = models.CharField(max_length=50)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    permanent_address = models.TextField()

    def __str__(self):
        return f"{self.firstname} - {self.lastname} - ({self.email})"
    
    
class Complaint(models.Model):
    # customer = models.ForeignKey('Customer', on_delete=models.CASCADE,null=True, blank=True)  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True, blank=True)  
    customer_name = models.CharField(max_length=100,null=True)
    complaint_text = models.TextField()
    garbage_collection_area = models.CharField(max_length=50)  
    complaint_date = models.DateField()

    def __str__(self):
        return f"Complaint - {self.user.username}"
    
class Customer(models.Model):
    customer_name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='customername')
    email = models.EmailField(unique=True)  
    address = models.TextField()
    garbage_collection_area = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer_name} - ({self.email})"
    
    
class Driver(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    driver_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    garbage_collection_area = models.CharField(max_length=50)
    vehicle_name = models.CharField(max_length=20)
    password=models.CharField(max_length=50,null=True)

    def __str__(self):
        return f"{self.driver_name} ({self.vehicle_name})"

class GarbageCollector(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    collector_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    address = models.TextField()
    garbage_collection_area = models.CharField(max_length=50)
    payment_text = models.TextField()

    def __str__(self):
        return f"{self.collector_name} ({self.email})"

class ReplyComplaint(models.Model):
    original_complaint  = models.ForeignKey('Complaint', on_delete=models.CASCADE,null=True, blank=True)
    # customer = models.ForeignKey('Customer', on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='replycomplaint')
    name=models.CharField(max_length=50)
    reply_complaint=models.TextField()
    reply_date = models.DateField()
    
    def __str__(self):
        return f"{self.original_complaint.user.username}"

class PaymentReport(models.Model): 
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='paymentreport')
    email = models.EmailField()
    garbage_collection_area = models.CharField(max_length=50)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    collector = models.ForeignKey('GarbageCollector', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"Payment Report - {self.customer.customer_name} - {self.amount}"
    

class GarbageCollectedReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='garbagereport')
    customer= models.ForeignKey('Customer', on_delete=models.CASCADE)  # Replace 'YourCustomerModel' with the actual customer model
    garbage_collection_area = models.CharField(max_length=50)
    date = models.DateField()
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)  # Replace 'YourDriverModel' with the actual driver model
    collector = models.ForeignKey('GarbageCollector', on_delete=models.CASCADE)  # Replace 'YourCollectorModel' with the actual collector model

    def __str__(self):
        return f"Garbage Collected Report for {self.customer.customer_name} on {self.date}"