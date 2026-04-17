from django import forms

# STEP 1 FORM

class Step1Form(forms.Form):

    name = forms.CharField(max_length=255, required=True)

    email = forms.EmailField(
        required=True,
        error_messages={
            'invalid': 'Enter a valid email address.'
        }
    )

    phone = forms.CharField(max_length=10, required=True)

    loan_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    tenure = forms.IntegerField(required=True)


    # Phone validation
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not phone:
            raise forms.ValidationError('Phone number is required.')

        if not phone.isdigit():
            raise forms.ValidationError('Phone must contain only digits.')

        if len(phone) != 10:
            raise forms.ValidationError('Phone must be exactly 10 digits.')

        return phone


    # Loan amount validation
    def clean_loan_amount(self):
        amount = self.cleaned_data.get('loan_amount')

        if amount is None:
            raise forms.ValidationError('Loan amount is required.')

        if amount <= 0:
            raise forms.ValidationError('Loan amount must be greater than zero.')

        return amount


    # Tenure validation
    def clean_tenure(self):
        tenure = self.cleaned_data.get('tenure')

        if tenure is None:
            raise forms.ValidationError('Tenure is required.')

        if tenure <= 0:
            raise forms.ValidationError('Tenure must be greater than zero.')

        return tenure




# STEP 2 FORM

class Step2Form(forms.Form):

    address_line1 = forms.CharField(max_length=255, required=True)

    address_line2 = forms.CharField(
        max_length=255,
        required=False  
    )

    city = forms.CharField(max_length=100, required=True)

    state = forms.CharField(max_length=100, required=True)

    pincode = forms.CharField(max_length=6, required=True)


    # Pincode Validation
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')

        if not pincode:
            raise forms.ValidationError("Pincode is required.")

        if not pincode.isdigit():
            raise forms.ValidationError("Pincode must contain only digits.")

        if len(pincode) != 6:
            raise forms.ValidationError("Pincode must be exactly 6 digits.")

        return pincode




# STEP 3 FORM

class Step3Form(forms.Form):

    EMPLOYMENT_CHOICES = [
        ('salaried', 'Salaried'),
        ('self_employed', 'Self Employed'),
    ]

    employment_type = forms.ChoiceField(choices=EMPLOYMENT_CHOICES, required=True)

    company_name = forms.CharField(max_length=255, required=True)

    monthly_income = forms.DecimalField(max_digits=10, decimal_places=2, required=True)

    work_experience = forms.IntegerField(required=True)


    # Monthly Income Validation
    def clean_monthly_income(self):
        income = self.cleaned_data.get('monthly_income')

        if income is None:
            raise forms.ValidationError("Monthly income is required.")

        if income <= 0:
            raise forms.ValidationError("Monthly income must be greater than 0.")

        return income


    # Work Experience Validation
    def clean_work_experience(self):
        experience = self.cleaned_data.get('work_experience')

        if experience is None:
            raise forms.ValidationError("Work experience is required.")

        if experience < 0:
            raise forms.ValidationError("Work experience cannot be negative.")

        return experience



# STEP 4 FORM

class Step4Form(forms.Form):

    profile_photo = forms.ImageField(required=True)

    id_proof = forms.FileField(required=True)

    optional_doc = forms.FileField(required=False)


    # Profile Photo Validation
    def clean_profile_photo(self):
        file = self.cleaned_data.get('profile_photo')

        if not file:
            raise forms.ValidationError("Profile photo is required.")

        if file.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Image size must be under 2MB.")

        if not file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
            raise forms.ValidationError("Only JPG, JPEG, PNG allowed.")

        return file


    # ID Proof Validation
    def clean_id_proof(self):
        file = self.cleaned_data.get('id_proof')

        if not file:
            raise forms.ValidationError("ID proof is required.")

        if file.size > 2 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 2MB.")

        if not file.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            raise forms.ValidationError("Only PDF, JPG, JPEG, PNG allowed.")

        return file


    # Optional Document Validation
    def clean_optional_doc(self):
        file = self.cleaned_data.get('optional_doc')

        if file:
            if file.size > 2 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 2MB.")

            if not file.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Only PDF, JPG, JPEG, PNG allowed.")

        return file