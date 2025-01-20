
from django.urls import path
from api import views
urlpatterns = [
    path('', views.home, name='Home'),
    path('client-master/', views.client_creation, name='client_creation'),
    path('maap-creation/<int:client_id>/', views.maap_view, name='maap_creation'),
    path('client/<int:client_id>/edit/', views.maap_edit_view, name='maap_edit_view'),
    path('create-bill/<int:client_id>/', views.create_bill_view, name='create_bill_view'),
    path('update-advance/<int:bill_id>/', views.edit_advance_form, name='edit_advance_form'),
    path('bill-detail/<int:bill_id>/', views.bill_detail_view, name='bill_detail_view'),
    path('maap-detail/<int:bill_id>/', views.maap_detail_view, name='maap_detail_view'),
    path('bill-master/', views.bill_list, name='bill_list'),
    path('employee-master/', views.employee_creation, name='employee_creation'),
    path('employee-report/', views.product_list_view, name='product_list_view'),
    path('advance-report/', views.advance_list_view, name='advance_list_view'),
    path('edit-company-profile/', views.update_company, name='update_company'),
    path('company-profile/', views.company_detail, name='company_detail'),
    # path('employee-login/', views.employee_login, name='employee_login'),
    # path('submit/upper/<int:client_id>/', views.upper_maap_submit, name='upper_maap_submit'),
    # path('submit/lower/<int:client_id>/', views.lower_maap_submit, name='lower_maap_submit'),
    path('register/company/', views.company_register, name='register_company'),
    # path('register/user/', views.register_user, name='register_user'),
    # path('accounts/login/', views.company_login, name='company_login'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # path('logout/company/', views.company_logout, name='company_logout'),

]
