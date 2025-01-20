from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    ClientMaster,
    UpperMaap,
    LowerMaap,
    BillNumberTracker,
    create_bill,
    product_list,
    advance_list,
    Company,
    User,
)

# Register other models
admin.site.register(ClientMaster)
admin.site.register(UpperMaap)
admin.site.register(LowerMaap)
admin.site.register(BillNumberTracker)
admin.site.register(create_bill)
admin.site.register(product_list)
admin.site.register(advance_list)

# Custom UserCreationForm for the admin panel
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_company_owner', 'company', 'employee_name', 'employee_number')

# Custom UserChangeForm for the admin panel
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_company_owner', 'company', 'employee_name', 'employee_number')

# Custom UserAdmin to manage the User model in the admin panel
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    # Configure what fields are displayed
    list_display = ['username', 'email', 'is_company_owner', 'company']
    search_fields = ['username', 'email', 'company__name']
    list_filter = ['is_company_owner', 'is_staff', 'is_active', 'company']
    
    fieldsets = DefaultUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('company', 'is_company_owner'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_company_owner', 'company'),
        }),
    )

# Custom CompanyAdmin (optional if additional customization is needed)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email', 'phone', 'address', 'created_at']
    search_fields = ['company_name', 'email', 'phone']
    list_filter = ['created_at']

# Register Company model
admin.site.register(Company, CompanyAdmin)
