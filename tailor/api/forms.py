from django import forms
from django.forms import modelformset_factory
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'logo', 'name', 'email', 'phone', 'address', 'prefix', 'note', 'qr_code', 'signature', 'upi_id', 'brand_1', 'brand_2', 'brand_3']

        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note', 'rows': '4'}),
        }
    
    def clean_prefix(self):
        prefix = self.cleaned_data.get('prefix')
        if not prefix.isalpha():
            raise forms.ValidationError("Prefix must contain only alphabets.")
        if len(prefix) > 4:
            raise forms.ValidationError("Prefix cannot exceed 3 characters.")
        return prefix


class ClientCreation(forms.ModelForm):
    class Meta:
        model = ClientMaster
        fields= ['client_name','client_number','book_number','page_number','client_status','client_address']


# class MaapCreation(forms.ModelForm):
#     class Meta:
#         model = MaapMaster
#         fields = ['upper_maap','upper_length','upper_shoulder','upper_sleeve_length','upper_sleeve_bicep',
#                   'upper_sleeve_cuff','upper_chest_body','upper_chest_ready','upper_lowerchest_body',
#                   'upper_lowerchest_ready','upper_stomach_body','upper_stomach_ready','upper_hip_body',
#                   'upper_hip_ready','upper_neck','upper_other_remark',
#                   'lower_maap','lower_length','lower_waist','lower_hip','lower_thai','lower_knee','lower_bottom',
#                   'lower_jhola','lower_other_remark']


class UpperMaapForm(forms.ModelForm):
    class Meta:
        model = UpperMaap
        fields = [
            'upper_maap', 'upper_length', 'upper_shoulder', 'upper_sleeve_length', 'upper_sleeve_bicep',
            'upper_sleeve_cuff', 'upper_chest_body', 'upper_chest_ready', 'upper_lowerchest_body',
            'upper_lowerchest_ready', 'upper_stomach_body', 'upper_stomach_ready', 'upper_hip_body',
            'upper_hip_ready', 'upper_neck', 'upper_other_remark',
            'upper_design_image'  # ✅ ADD THIS
        ]
        widgets = {
            'upper_maap': forms.Select(attrs={'class': 'form-select'}),
            'upper_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length'}),
            'upper_shoulder': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Shoulder'}),
            'upper_sleeve_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length'}),
            'upper_sleeve_bicep': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bicep'}),
            'upper_sleeve_cuff': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cuff'}),
            'upper_chest_body': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Body'}),
            'upper_chest_ready': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ready'}),
            'upper_lowerchest_body': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Body'}),
            'upper_lowerchest_ready': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ready'}),
            'upper_stomach_body': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Body'}),
            'upper_stomach_ready': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ready'}),
            'upper_hip_body': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Body'}),
            'upper_hip_ready': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ready'}),
            'upper_neck': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Neck'}),
            'upper_other_remark': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Other Remark', 'rows': '4'}),

            # ✅ IMAGE WIDGET
            'upper_design_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

UpperMaapFormSet = modelformset_factory(UpperMaap, form=UpperMaapForm, extra=1)


class LowerMaapForm(forms.ModelForm):
    class Meta:
        model = LowerMaap
        fields = [
            'lower_maap', 'lower_length', 'lower_waist', 'lower_hip', 'lower_thai', 'lower_knee', 'lower_bottom',
            'lower_jhola', 'lower_other_remark',
            'lower_design_image'  # ✅ ADD THIS
        ]
        widgets = {
            'lower_maap': forms.Select(attrs={'class': 'form-select'}),
            'lower_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Length'}),
            'lower_waist': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Waist'}),
            'lower_hip': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Hip'}),
            'lower_thai': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Thai'}),
            'lower_knee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Knee'}),
            'lower_bottom': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bottom'}),
            'lower_jhola': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Jhola'}),
            'lower_other_remark': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Other Remark', 'rows': '1'}),

            # ✅ IMAGE WIDGET
            'lower_design_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

LowerMaapFormSet = modelformset_factory(LowerMaap, form=LowerMaapForm, extra=1)
class billForms(forms.ModelForm):
    class Meta:
        model = create_bill
        fields = ['bill_number','bill_date','delivery_date','total_amount','discount','total_bill','gst_amount','gst_rate','total_amount_received','amount_receivable']
                #   'adv_1_date','adv_2_date','adv_3_date','adv_1_amount','adv_2_amount','adv_3_amount']
                # 'product_name','product_remark','quantity','rate','amount',
        widgets = {
            'total_amount': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control two-decimal text-end'}),
            'total_amount_received': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
        }
BillFormSet = modelformset_factory(create_bill, form=billForms, extra=1)


class productForms(forms.ModelForm):
    class Meta:
        model = product_list
        fields = ['product_name', 'product_remark', 'quantity', 'rate', 'amount', 'product_assignedTo']

        widgets = {
            'product_name': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'product_remark': forms.Textarea(attrs={'class': 'form-control', 'rows': '1'}),
            'product_assignedTo': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control text-end'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control two-decimal text-end'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control text-end two-decimal'}),
        }
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)  # Get company from kwargs passed in the view
        super().__init__(*args, **kwargs)

        # Filter employees based on the logged-in company and only include active ones
        if company:
            self.fields['product_assignedTo'].queryset = User.objects.filter(
                company=company, employee_status='active',is_company_owner=False
            )


ProductFormSet = modelformset_factory(product_list, form=productForms, extra=1)


class advanceForms(forms.ModelForm):
    class Meta:
        model = advance_list
        fields = ['receipt_ref_no','receipt_type','receipt_date','amount_received']

        widgets = {
            'receipt_ref_no': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'receipt_type': forms.Select(attrs={'class': 'form-select'}),
            'receipt_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount_received': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control text-end two-decimal'}),
        }

AdvanceFormSet = modelformset_factory(advance_list, form=advanceForms, extra=1)



# Employee Creation Form
# class EmployeeCreation(forms.ModelForm):
#     class Meta:
#         model = EmployeeMaster
#         fields= ['employee_name','employee_number','employee_status','username','password','employee_right']



# class CompanyRegisterForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ['company_name', 'email', 'password', 'logo', 'number', 'address']
#         widgets = {
#             'password': forms.PasswordInput(),
        # }

# class UserRegisterForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'password', 'number', 'company']
#         widgets = {
#             'password': forms.PasswordInput(),
#         }

# class LoginForm(forms.Form):
#     email_or_username = forms.CharField(max_length=255)
#     password = forms.CharField(widget=forms.PasswordInput)




# class CompanyRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = Company
#         fields = ['company_name', 'email', 'password', 'logo', 'number', 'address']

#     def save(self, commit=True):
#         company = super().save(commit=False)
#         company.set_password(self.cleaned_data["password"])
#         if commit:
#             company.save()
#         return company



# class EmployeeRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = EmployeeMaster
#         fields = ['employee_name', 'username', 'password', 'employee_status', 'employee_right', 'company']

#     def save(self, commit=True):
#         employee = super().save(commit=False)
#         employee.set_password(self.cleaned_data["password"])
#         if commit:
#             employee.save()
#         return employee



# class CompanyRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Company
#         fields = ['company_name', 'email', 'password', 'logo', 'number', 'address']


# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=255, label="Username")
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     company = forms.ModelChoiceField(queryset=Company.objects.all(), label="Company")
#     employee_name = forms.CharField(max_length=100, label="Employee Name")
#     employee_number = forms.CharField(max_length=100, label="Employee Number")
#     employee_right = forms.ChoiceField(
#         choices=[('admin', 'Admin'), ('user', 'User')], label="Role"
#     )

# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeMaster
#         fields = ['employee_number', 'employee_name','employee_number','employee_right','username', 'password']

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = EmployeeMaster
#         fields = ['username', 'password', 'employee_name', 'employee_number', 'employee_status', 'employee_right']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match.")
#         return cleaned_data

# # Login Form (Using AuthenticationForm)
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=255)
#     password = forms.CharField(widget=forms.PasswordInput)



# class EmployeeRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = EmployeeMaster
#         fields = ['username', 'password', 'employee_name', 'employee_number', 'employee_status', 'employee_right']

#     def save(self, commit=True, company=None):
#         employee = super().save(commit=False)
#         employee.password = make_password(self.cleaned_data['password'])
#         if company:
#             employee.company = company
#         if commit:
#             employee.save()
#         return employee



# class EmployeeCreationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'employee_name', 'employee_number', 'is_company_owner','employee_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee_name'].required = True  # Make employee_name required
