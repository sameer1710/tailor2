from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.safestring import mark_safe
from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError




def validate_prefix(value):
    if len(value) < 1 or len(value) > 5 or not value.isalpha():
        raise ValidationError('Prefix must be between 1 and 4 alphabetic characters.')

# class Company(models.Model):
#     company_name = models.CharField(max_length=255)
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     qr_code = models.ImageField(upload_to='qrcode/', blank=True, null=True)
#     signature = models.ImageField(upload_to='signature/', blank=True, null=True)
#     note = models.TextField(null=True, blank=True, help_text="Enter notes as separate lines.")
#     prefix = models.CharField(max_length=4, validators=[validate_prefix], blank=True, null=True)  # New field for prefix

#     def get_notes(self, obj):
#     # """Display the note field with line breaks."""
#         if obj.note:
#             return mark_safe(obj.note.replace("\n", "<br>"))
#         return "No notes available"

#     formatted_notes.short_description = "Notes"

#     def __str__(self):
#         return self.company_name

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.ImageField(upload_to='qrcode/', blank=True, null=True)
    brand_1 = models.ImageField(upload_to='brand_logo/', blank=True, null=True)
    brand_2 = models.ImageField(upload_to='brand_logo/', blank=True, null=True)
    brand_3 = models.ImageField(upload_to='brand_logo/', blank=True, null=True)
    upi_id = models.CharField(max_length=255, null=True, blank=True)
    signature = models.ImageField(upload_to='signature/', blank=True, null=True)
    note = models.TextField(null=True, blank=True, help_text="Enter notes as separate lines.")
    prefix = models.CharField(max_length=4, validators=[validate_prefix], blank=True, null=True)

    def get_notes_as_list(self):
        """Convert the note field into a list of lines."""
        if self.note:
            return self.note.split("\n")
        return []

    def __str__(self):
        return self.company_name


# class Company(models.Model):
#     company_name = models.CharField(max_length=255)
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     note = models.TextField(null=True, blank=True, help_text="Enter notes as separate lines.")
#     prefix = models.CharField(max_length=4, validators=[validate_prefix], blank=True, null=True)

#     def get_notes_as_list(self):
#         """Convert the note field into a list of lines."""
#         if self.note:
#             return self.note.split("\n")
#         return []

#     def __str__(self):
#         return self.company_name



class User(AbstractUser):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    is_company_owner = models.BooleanField(default=False)  # To distinguish owners from regular employees
    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=255, null=True, blank=True)
    employee_status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Add a custom related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # Add a custom related_name
        blank=True,
    )

    def __str__(self):
        return self.employee_name




# Custom Manager for Company
# class CompanyManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         company = self.model(email=email, **extra_fields)
#         company.set_password(password)
#         company.save(using=self._db)
#         return company

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, password, **extra_fields)

# class Company(AbstractBaseUser, PermissionsMixin):
#     company_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)
#     number = models.CharField(max_length=15)
#     address = models.TextField()
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)  # Required by Django admin

#     objects = CompanyManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['company_name', 'number']

#     def __str__(self):
#         return self.company_name

# class Company(models.Model):
#     company_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     logo = models.ImageField(upload_to='logos/', blank=True, null=True)
#     number = models.CharField(max_length=15)
#     address = models.TextField()

#     superuser = models.OneToOneField(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE
#     )

#     def __str__(self):
#         return self.company_name




# class CustomUser(AbstractUser):
#     company = models.ForeignKey(
#         'Company',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name='users'  # Custom related name
#     )
#     employee_right = models.CharField(
#         max_length=10, 
#         choices=[('admin', 'Admin'), ('user', 'User')]
#     )

# class EmployeeManager(BaseUserManager):
#     def create_user(self, username, password, company, employee_name, employee_right='user', **extra_fields):
#         if not username:
#             raise ValueError("The Username field is required")
#         if employee_right not in ['admin', 'user']:
#             raise ValueError("Invalid role for employee_right")
        
#         user = self.model(
#             username=username,
#             company=company,
#             employee_name=employee_name,
#             employee_right=employee_right,
#             **extra_fields
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

    # def create_superuser(self, username, password, company, **extra_fields):
    #     extra_fields.setdefault('employee_right', 'admin')
    #     return self.create_user(username, password, company, **extra_fields)

# class EmployeeMaster(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')
#     employee_name = models.CharField(max_length=100)
#     employee_number = models.IntegerField()
#     employee_status = models.CharField(
#         max_length=10,
#         choices=[('active', 'Active'), ('inactive', 'Inactive')],
#         default='active'
#     )
#     EMPLOYEE_RIGHT_CHOICES = [
#         ('admin', 'Admin'),
#         ('user', 'User'),
#     ]
#     employee_right = models.CharField(max_length=10, choices=EMPLOYEE_RIGHT_CHOICES, default='user')
#     superuser = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='owned_company'  # Custom related name
#     )



#     # objects = EmployeeManager()

#     def __str__(self):
#         return f"{self.username} ({self.employee_right})"



# User Model
# class User(models.Model):
#     name = models.CharField(max_length=255)
#     number = models.CharField(max_length=15)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')

#     def __str__(self):
#         return self.name


# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=255)
#     contact_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?\d{1,4}?[ -]?\(?\d{1,3}\)?[ -]?\d{1,4}([ -]?\d{1,4})*$')])
#     address = models.TextField()
#     logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
#     prefix = models.CharField(max_length=50, null=True, blank=True)

#     def __str__(self):
#         return self.name

#     def save(self, *args, **kwargs):
#         if not self.pk:
#             self.password = self.set_password(self.password)
#         super().save(*args, **kwargs)

#     def set_password(self, raw_password):
#         # Here you would hash the password
#         return raw_password  # Use a hashing mechanism (like bcrypt) in a real app


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         return self.create_user(username, email, password, **extra_fields)


# class User(AbstractBaseUser):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='users')
#     username = models.CharField(max_length=255, unique=True)
#     email = models.EmailField(unique=True)
#     contact_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?\d{1,4}?[ -]?\(?\d{1,3}\)?[ -]?\d{1,4}([ -]?\d{1,4})*$')])
#     password = models.CharField(max_length=255)
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)  # Determines if user can access admin
#     date_joined = models.DateTimeField(default=timezone.now)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return self.username

#     def set_password(self, raw_password):
#         # Here you would hash the password
#         return raw_password  # Use a hashing mechanism (like bcrypt) in a real app























class ClientMaster(models.Model):
    TYPE_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'In-Active'),
    ]
    client_name = models.CharField(max_length=100)
    client_number = models.IntegerField()
    book_number = models.IntegerField()
    page_number = models.IntegerField()
    client_address = models.TextField()    
    client_status = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)
    company = models.ForeignKey("Company", null=True,blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.client_name}"
    

# UPPER_MAAP_CHOICES = [
#     ('', 'Select Type'),  # Empty option, shown as default
#     ('zubba', 'Zubba'),
#     ('kurta', 'Kurta'),
#     ('shirt', 'Shirt'),
#     ('blazer', 'Blazer'),
#     ('koty', 'Koty'),
#     ('others', 'Others'),
# ]

# LOWER_MAAP_CHOICES = [
#     ('', 'Select Type'), 
#     ('pathani_salwar', 'Pathani Salwaar'),
#     ('aligari', 'Aligari'),
#     ('payjama', 'Payjama'),
#     ('chudidar', 'Chudidar'),
#     ('pant', 'Pant'),
#     ('others', 'Others'),
# ]

# class MaapMaster(models.Model):
#     client = models.ForeignKey(ClientMaster, on_delete=models.CASCADE,null=True,blank=True)

#     upper_maap = models.CharField(
#         max_length=100,
#         choices=UPPER_MAAP_CHOICES,
#         blank=True,
#         null=True,  
#     )
#     upper_length = models.FloatField(null=True, blank=True)
#     upper_shoulder = models.FloatField(null=True, blank=True)
#     upper_sleeve_length = models.FloatField(null=True, blank=True)
#     upper_sleeve_bicep = models.FloatField(null=True, blank=True)
#     upper_sleeve_cuff = models.FloatField(null=True, blank=True)
#     upper_chest_body = models.FloatField(null=True, blank=True)
#     upper_chest_ready = models.FloatField(null=True, blank=True)
#     upper_lowerchest_body = models.FloatField(null=True, blank=True)
#     upper_lowerchest_ready = models.FloatField(null=True, blank=True)
#     upper_stomach_body = models.FloatField(null=True, blank=True)
#     upper_stomach_ready = models.FloatField(null=True, blank=True)
#     upper_hip_body = models.FloatField(null=True, blank=True)
#     upper_hip_ready = models.FloatField(null=True, blank=True)
#     upper_neck = models.FloatField(null=True, blank=True)
#     upper_other_remark = models.TextField(null=True, blank=True)


#     lower_maap = models.CharField(
#         max_length=100,
#         choices=LOWER_MAAP_CHOICES,
#         blank=True,
#         null=True,  
#     )
#     lower_length = models.FloatField(null=True, blank=True)
#     lower_waist = models.FloatField(null=True, blank=True)
#     lower_hip = models.FloatField(null=True, blank=True)
#     lower_thai = models.FloatField(null=True, blank=True)
#     lower_knee = models.FloatField(null=True, blank=True)
#     lower_bottom = models.FloatField(null=True, blank=True)
#     lower_jhola = models.FloatField(null=True, blank=True)
#     lower_other_remark = models.TextField(null=True, blank=True)




#     def __str__(self):
#         # return self.client if self.client else "Not Selected"
#         return f"Maap for {self.client.client_name}"







# ===============================================================================
class UpperMaap(models.Model):
    client = models.ForeignKey(ClientMaster, on_delete=models.CASCADE, related_name='upper_maaps')
    TYPE_CHOICES = [
        ('zubba', 'Zubba'),
        ('kurta', 'Kurta'),
        ('shirt', 'Shirt'),
        ('blazer', 'Blazer'),
        ('koty', 'Koty'),
        ('others', 'Others'),
    ]
    upper_maap = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)
    upper_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_shoulder = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_sleeve_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_sleeve_bicep = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_sleeve_cuff = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_chest_body = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_chest_ready = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_lowerchest_body = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_lowerchest_ready = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_stomach_body = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_stomach_ready = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_hip_body = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_hip_ready = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_neck = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    upper_other_remark = models.TextField(null=True, blank=True)


class LowerMaap(models.Model):
    client = models.ForeignKey(ClientMaster, on_delete=models.CASCADE, related_name='lower_maaps')
    TYPE_CHOICES = [
        ('pathani_salwar', 'Pathani Salwaar'),
        ('aligari', 'Aligari'),
        ('payjama', 'Payjama'),
        ('chudidar', 'Chudidaar'),
        ('pant', 'Pant'),
        ('others', 'Others'),
    ]
    lower_maap = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)
    lower_length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_waist = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_hip = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_thai = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_knee = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_bottom = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_jhola = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lower_other_remark = models.TextField(null=True, blank=True)
# ===============================================================================

# class EmployeeManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError("The Username field must be set")
#         extra_fields.setdefault('is_active', True)
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(username, password, **extra_fields)

#     def get_by_natural_key(self, username):
#         return self.get(username=username)



# Employee Creation Model
# class EmployeeMaster(models.Model):
#     employee_name = models.CharField(max_length=100)
#     employee_number = models.IntegerField()
#     employee_status = models.CharField(
#         max_length=10,
#         choices=[('active', 'Active'), ('inactive', 'Inactive')],
#         default='active'
#     )
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=255)
#     employee_right = models.CharField(
#         max_length=10,
#         choices=[('admin', 'Admin'), ('user', 'User')],
#         default='user'
#     )
#     company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)


# class EmployeeMaster(AbstractBaseUser):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     employee_name = models.CharField(max_length=100)
#     employee_number = models.IntegerField()
#     employee_status = models.CharField(
#         max_length=10,
#         choices=[('active', 'Active'), ('inactive', 'Inactive')],
#         default='active'
#     )
#     employee_right = models.CharField(
#         max_length=10,
#         choices=[('admin', 'Admin'), ('user', 'User')],
#         default='user'
#     )
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['password']

#     def __str__(self):
#         return self.username


    # objects = EmployeeManager()  # Link the custom manager

    # def __str__(self):
    #     return self.employee_name
# ---------------------------------------------------------------------
class BillNumberTracker(models.Model):
    bill_number = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)


class create_bill(models.Model):
    company =models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    client = models.ForeignKey(ClientMaster, on_delete=models.CASCADE, related_name='bills')

    bill_number = models.CharField(max_length=20, unique=True, blank=True)
    bill_date = models.DateField(null=True,blank=True)
    delivery_date = models.DateField(null=True,blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gst_rate = models.CharField(max_length=100, null=True, blank=True)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    amount_receivable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)



class product_list(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='product_list_company')  # Changed related_name
    invoice = models.ForeignKey(create_bill, on_delete=models.CASCADE, related_name='products')

    product_name = models.CharField(max_length=1000, null=True, blank=True)
    product_remark = models.CharField(max_length=1000, null=True, blank=True)
    # product_assignedTo = models.CharField(max_length=1000, null=True, blank=True)
    product_assignedTo = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'employee_status': 'active','is_company_owner':False},  # Limit to active employees
        related_name='assigned_products'
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    



class advance_list(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='advance_list_company')  # Changed related_name
    invoice = models.ForeignKey(create_bill, on_delete=models.CASCADE, related_name='advance')

    TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('upi', 'UPI'),
    ]
    receipt_ref_no = models.CharField(max_length=100, null=True, blank=True)
    receipt_type = models.CharField(max_length=50, choices=TYPE_CHOICES, null=True, blank=True)
    receipt_date = models.DateField(null=True, blank=True)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


