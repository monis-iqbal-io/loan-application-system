from django.db import models
from django.core.validators import RegexValidator, MinValueValidator

class LoanApplication(models.Model):
    # personal Details
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone  = models.CharField(
        max_length = 10,
        unique = True,
        validators = [
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits.',
            )
        ]
    )

    # loan details
    loan_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2, 
        validators=[MinValueValidator(1)]
    )

    tenure = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # Address details
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    pincode = models.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Pincode must be exactly 6 digits.',
            )
        ]
    )

    # professional_details
    employment_type = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)

    monthly_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    work_experience = models.PositiveIntegerField()

    # documents
    profile_photo = models.ImageField(upload_to='profiles/')
    id_proof = models.FileField(upload_to='documents/')
    optional_doc = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True)
    

    # metadata
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

