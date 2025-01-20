from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
# from .models import FormData
from .models import *
from django.forms import modelformset_factory
from .forms import *
from datetime import datetime
from num2words import num2words
from django.db.models import Sum
# from django.forms import modelformset_factory
# from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from functools import wraps
from django.http import HttpResponseForbidden


# def custom_user_create(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # Optionally, log the user in after successful registration
#             login(request, user)
#             messages.success(request, "User successfully created and logged in.")
#             return redirect('home')  # Redirect to a home page or dashboard after successful registration
#         else:
#             messages.error(request, "Error creating user. Please check the form.")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/custom_user_create.html', {'form': form})


# This is the correct working code
# def employee_creation(request):
#     print(request.user.company.id,'llllllllll')
#     if not request.user.is_company_owner:
#         return HttpResponseForbidden("You do not have permission to add employees.")

#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             print('jjj')
#             employee = form.save(commit=False)  # Save instance without committing
#             employee.company = request.user.company  # Assign company
#             # Set and hash the password
#             # employee.set_password(form.cleaned_data['password'])
#             employee.save()  # Save the instance to the database
#             print('cc')
#             return redirect('employee_creation')  # Redirect to a success page
#             messages.success(request, 'Employee Created Successfully!')
#         else:
#             print(form.errors)  # Log any form validation errors for debugging
#     else:
#         form = CustomUserCreationForm()

#     employees = User.objects.filter(company=request.user.company)
    

#     return render(request, 'employee-master.html', {'form': form, 'employees': employees})

def employee_creation(request):
    if request.method == "POST":
        # Check if it's an update operation
        employee_id = request.POST.get("employee_id")

        if employee_id:
            # Update existing employee
            employee = get_object_or_404(User, id=employee_id)

            # Update fields
            employee.employee_name = request.POST.get("employee_name")
            employee.employee_number = request.POST.get("employee_number")  # Allow updating employee_number
            employee.username = request.POST.get("username")
            employee.employee_status = request.POST.get("employee_status")
            employee.is_company_owner = request.POST.get("is_company_owner") == "true"

            # Update password if provided and valid
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 and password1 == password2:
                employee.set_password(password1)
            elif password1 or password2:
                return render(request, 'employee-master.html', {
                    'form': request.POST,
                    'employees': User.objects.filter(company=request.user.company),
                    'error': "Passwords do not match or are invalid.",
                })

            # Save updated employee
            employee.save()
            return redirect('employee_creation')

        else:
            # Handle the creation logic
            employee_name = request.POST.get("employee_name")
            employee_number = request.POST.get("employee_number")
            username = request.POST.get("username")
            employee_status = request.POST.get("employee_status")
            is_company_owner = request.POST.get("is_company_owner") == "true"
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                return render(request, 'employee-master.html', {
                    'form': request.POST,
                    'employees': User.objects.filter(company=request.user.company),
                    'error': "Passwords do not match.",
                })

            # Create new employee
            employee = User.objects.create(
                employee_name=employee_name,
                employee_number=employee_number,  # No unique constraint here
                username=username,
                employee_status=employee_status,
                is_company_owner=is_company_owner,
                company=request.user.company,
            )
            employee.set_password(password1)
            employee.save()

            return redirect('employee_creation')

    # Render the page with the list of employees
    employees = User.objects.filter(company=request.user.company)
    return render(request, 'employee-master.html', {'employees': employees})








# def employee_creation(request):
#     company = Company.objects.get(superuser=request.user)

#     if request.method == 'POST':
#         form = EmployeeRegistrationForm(request.POST)
#         if form.is_valid():
#             employee = form.save(commit=False)
#             # Set password securely
#             # employee.password(form.cleaned_data['password'])
#             employee.company = company
#             employee.save()
#             messages.success(request, "Employee registered successfully!")
#             # Authenticate and log in the user
#             user = authenticate(username=employee.username, password=form.cleaned_data['password'])
#             if user:
#                 login(request, user)
#                 return redirect('employee_creation')  # Redirect to employee dashboard or any other page
#     else:
#         form = EmployeeRegistrationForm()
#     return render(request, 'new/register_employee.html', {'form': form})


def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Attempting login with username: {username}, password: {password}")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Login successful")
            if request.user.is_company_owner == True:
                return redirect('client_creation')  # Replace with your desired redirect
            else:
                return redirect('product_list_view')
        else:
            print("Invalid credentials")
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')


# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)

#             messages.success(request, f"Welcome back, {user.username}!")
#             if request.user.is_user == True:

#                 return redirect('client_creation')  # Redirect to a page after successful login
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})



# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             print('fffffff')
#             return redirect('client_creation')  # Redirect to the employee's dashboard or any other page
#         else:
#             print('aaaaaaaaaaa')
#             messages.error(request, "Invalid username or password")
#     return render(request, 'new/login_employee.html')

# def employee_creation(request):
#     # user = request.user
#     # company_id = user.id
#     company = Company.objects.get(superuser=request.user)
#     # company = Company.objects.get(id=company_id)
#     if request.method == 'POST':
    
#     # Access the company associated with the user and its ID

#         try:
#             company = Company.objects.get(superuser=request.user)
#         except Company.DoesNotExist:
#             messages.error(request, "Invalid company. Please try again.")

#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             # password = form.cleaned_data['password']
#             employee_name = form.cleaned_data['employee_name']
#             employee_right = form.cleaned_data['employee_right']
#             employee_number  = form.cleaned_data['employee_number']
#             password = make_password(form.cleaned_data['password'])  # Hash the password

#             # Create the user and associate it with the company from the session
#             user = EmployeeMaster.objects.create(
#                 employee_number=employee_number,
#                 username=username,
#                 password=password,
#                 company=company,  # Use the company from the session
#                 employee_name=employee_name,
#                 employee_right=employee_right,
#             )
#             messages.success(request, "Registration successful.")
#             return redirect('login')
#         else:
#             messages.error(request, "Please correct the errors below.")
#     else:
#         form = RegisterForm()
#     employees = EmployeeMaster.objects.filter(company=company).order_by('-id')

#     return render(request, 'employee-master.html', {'form': form,'employees':employees})




# def loin_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 messages.success(request, "Logged in successfully.")
#                 return redirect('client_creation')  # Change 'dashboard' to your preferred page
#             else:
#                 messages.error(request, "Invalid username or password.")
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')








# Register Company
# def register_company(request):
#     if request.method == 'POST':
#         form = CompanyRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             company = form.save(commit=False)
#             company.password = make_password(form.cleaned_data['password'])  # Hash the password
#             company.save()
#             # Send Email
#             send_mail(
#                 'Company Registration Successful',
#                 f'Your username is {company.email} and password is {form.cleaned_data["password"]}',
#                 's.shaikh7876@gmail.com',
#                 [company.email],
#             )
#             messages.success(request, 'Company registered successfully!')
#             return redirect('company_login')
#     else:
#         form = CompanyRegisterForm()
#     return render(request, 'register_company.html', {'form': form})

# Register User
# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = form.cleaned_data['password']
#             user.save()
#             messages.success(request, 'User registered successfully!')
#             return redirect('user_login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'register_user.html', {'form': form})

# Login
from django.contrib.auth.hashers import check_password

# def company_login(request):

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             try:
#                 company = Company.objects.get(email=email)
#                 if check_password(password, company.password):  # Validate the hashed password
#                     request.session['company_id'] = company.id
#                     request.session['role'] = 'company'

#                     messages.success(request, 'Login successful!')
#                     return redirect('client_creation') 
#                 else:
#                     messages.error(request, 'Invalid credentials.')
#             except Company.DoesNotExist:
#                 messages.error(request, 'Company does not exist.')
#     else:
#         form = LoginForm()
#     return render(request, 'company_login.html', {'form': form})



# ogg
# def company_register(request):
#     if request.method == 'POST':
#         form = CompanyRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             company = form.save()
#             # login(request, company)  # Log the company in after successful registration
#             return redirect('company_login')  # Redirect to home or dashboard page
#     else:
#         form = CompanyRegistrationForm()
#     return render(request, 'company_register.html', {'form': form})


# newly added ****************************
def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = CompanyRegistrationForm()
    return render(request, 'new/register_company.html', {'form': form})






# def company_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         company = authenticate(request, username=email, password=password)
#         if company:
#             login(request, company)  # Log in the company
#             messages.success(request, 'Company login successful!')
#             return redirect('client_creation', pk=company.id)  # Redirect to the client creation page with company ID

#             # login(request, company)
#             # return redirect('company_dashboard')  # Redirect to company dashboard
#         else:
#             return render(request, 'new/company_login.html', {'error': 'Invalid credentials'})
#     return render(request, 'new/company_login.html')






# newly added ****************************









# def company_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         # Check if the user is a company
#         try:
#             company = Company.objects.get(email=username)
#             if check_password(password, company.password):
#                 request.session['role'] = 'company'
#                 request.session['company_id'] = company.id
#                 login(request, company)
#                 return redirect('dashboard')  # Redirect to company's dashboard
#         except Company.DoesNotExist:
#             pass

#         # Check if the user is an employee
#         try:
#             employee = EmployeeMaster.objects.get(username=username)
#             if check_password(password, employee.password):
#                 request.session['role'] = 'employee'
#                 request.session['employee_id'] = employee.id
#                 request.session['company_id'] = employee.company.id
#                 login(request, employee)
#                 return redirect('employee_dashboard')  # Redirect to employee's dashboard
#         except EmployeeMaster.DoesNotExist:
#             pass

#         messages.error(request, 'Invalid username or password')
#     return render(request, 'login.html')
# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             # First, try authenticating as a company user
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)

#                 # Check if the user is a company and pass the company ID to the redirect
#                 if hasattr(user, 'company'):  # Ensure it's a company user
#                     company = user.company

#                     return redirect("client_creation" ,pk=company.id)

#                 return redirect("dashboard")

#             # Check for EmployeeMaster if not company
#             try:
#                 employee = EmployeeMaster.objects.get(username=username)
#                 if employee.password == password:  # Replace with a secure check
#                     request.session["is_employee"] = True
#                     request.session["employee_id"] = employee.id
#                     return redirect("dashboard")
#             except EmployeeMaster.DoesNotExist:
#                 pass

#             # If authentication fails
#             return render(request, "login.html", {"form": form, "error": "Invalid credentials"})

#     else:
#         form = LoginForm()

#     return render(request, "login.html", {"form": form})



def logout_user(request):
    logout(request)
    request.session.flush()
    return redirect("company_login")




# def company_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         company = authenticate(request, email=email, password=password)
#         if company is not None:
#             login(request, company)
#             return redirect('home')
#         else:
#             return render(request, 'company_login.html', {'error': 'Invalid credentials'})
#     return render(request, 'company_login.html')

# def employee_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         employee = authenticate(request, email=email, password=password)
#         if employee is not None:
#             login(request, employee)
#             return redirect('home')
#         else:
#             return render(request, 'company_login.html', {'error': 'Invalid credentials'})
#     return render(request, 'company_login.html')





# Logout
# def company_logout(request):
#     logout(request)
#     return redirect('company_login')

# # Dashboard
# def dashboard(request):
#     if 'company_id' in request.session:
#         company = Company.objects.get(id=request.session['company_id'])
#         users = company.users.all()
#         return render(request, 'dashboard.html', {'company': company, 'users': users})
#     return redirect('company_login')




# def home(request):
#     # # Check if the user is a Company
#     # if isinstance(request.user, Company):  # Company is logged in
#     #     employees = EmployeeMaster.objects.filter(company=request.user)
#     #     print('jjjjjjjj')
#     #     context = {'employees': employees, 'is_company': True}
    
#     # # Check if the user is an Employee
#     # elif isinstance(request.user, EmployeeMaster):  # Employee is logged in
#     #     print('qqqqqqqqqqqqq')
#     #     if request.user.employee_right == 'admin':
#     #         print('cccccccccccc')
#     #         employees = EmployeeMaster.objects.filter(company=request.user.company)
#     #     else:  # Regular employee
#     #         print('mmmmmmmmmmm')
#     #         employees = EmployeeMaster.objects.filter(pk=request.user.pk)
#     #     context = {'employees': employees, 'is_company': False}
    
#     # else:
#     #     print('zzzzzzzzzz')
#     #     context = {}
#     # employees = EmployeeMaster.objects.get(company=request.user)
#      context = {
#         'user': request.user,
#     }
     
#     return render(request, 'index.html',context)



def home(request):
    company_id = request.user.company.id
    company = Company.objects.get(id=company_id)
    print('sameer', company.logo.url)

    return render(request, 'index.html')

# def client_master(request):
#     return render(request, "client-master.html")

# def maap_creation_page(request):
#     return render(request, "client-creation.html")


# def maap_creation(request, client_id):
#     client = get_object_or_404(ClientMaster, id=client_id)

#     if request.method == 'POST':
#         # Get all the form data from the POST request
#         upper_maap_list = request.POST.getlist('upper_maap[]')
#         upper_length_list = request.POST.getlist('upper_length[]')
#         upper_shoulder_list = request.POST.getlist('upper_shoulder[]')
#         upper_sleeve_length_list = request.POST.getlist('upper_sleeve_length[]')
#         upper_sleeve_bicep_list = request.POST.getlist('upper_sleeve_bicep[]')
#         upper_sleeve_cuff_list = request.POST.getlist('upper_sleeve_cuff[]')
#         upper_chest_body_list = request.POST.getlist('upper_chest_body[]')
#         upper_chest_ready_list = request.POST.getlist('upper_chest_ready[]')
#         upper_lowerchest_body_list = request.POST.getlist('upper_lowerchest_body[]')
#         upper_lowerchest_ready_list = request.POST.getlist('upper_lowerchest_ready[]')
#         upper_stomach_body_list = request.POST.getlist('upper_stomach_body[]')
#         upper_stomach_ready_list = request.POST.getlist('upper_stomach_ready[]')
#         upper_hip_body_list = request.POST.getlist('upper_hip_body[]')
#         upper_hip_ready_list = request.POST.getlist('upper_hip_ready[]')
#         upper_neck_list = request.POST.getlist('upper_neck[]')
#         upper_other_remark_list = request.POST.getlist('upper_other_remark[]')

#         lower_maap_list = request.POST.getlist('lower_maap[]')
#         lower_length_list = request.POST.getlist('lower_length[]')
#         lower_waist_list = request.POST.getlist('lower_waist[]')
#         lower_hip_list = request.POST.getlist('lower_hip[]')
#         lower_thai_list = request.POST.getlist('lower_thai[]')
#         lower_knee_list = request.POST.getlist('lower_knee[]')
#         lower_bottom_list = request.POST.getlist('lower_bottom[]')
#         lower_jhola_list = request.POST.getlist('lower_jhola[]')
#         lower_remark_list = request.POST.getlist('lower_other_remark[]')

#         # Loop through the lists and save each row
#         max_length = max(len(upper_maap_list), len(lower_maap_list))  # Get the max length of both lists
#         for i in range(max_length):
#             # Create upper maap data if it's not empty
#             upper_data = {}
#             if i < len(upper_maap_list) and any([
#                 upper_maap_list[i], upper_length_list[i], upper_shoulder_list[i], upper_sleeve_length_list[i],
#                 upper_sleeve_bicep_list[i], upper_sleeve_cuff_list[i], upper_chest_body_list[i],
#                 upper_chest_ready_list[i], upper_lowerchest_body_list[i], upper_lowerchest_ready_list[i],
#                 upper_stomach_body_list[i], upper_stomach_ready_list[i], upper_hip_body_list[i],
#                 upper_hip_ready_list[i], upper_neck_list[i], upper_other_remark_list[i]
#             ]):
#                 upper_data = {
#                     'upper_maap': upper_maap_list[i] if upper_maap_list[i] else None,
#                     'upper_length': upper_length_list[i] if upper_length_list[i] else None,
#                     'upper_shoulder': upper_shoulder_list[i] if upper_shoulder_list[i] else None,
#                     'upper_sleeve_length': upper_sleeve_length_list[i] if upper_sleeve_length_list[i] else None,
#                     'upper_sleeve_bicep': upper_sleeve_bicep_list[i] if upper_sleeve_bicep_list[i] else None,
#                     'upper_sleeve_cuff': upper_sleeve_cuff_list[i] if upper_sleeve_cuff_list[i] else None,
#                     'upper_chest_body': upper_chest_body_list[i] if upper_chest_body_list[i] else None,
#                     'upper_chest_ready': upper_chest_ready_list[i] if upper_chest_ready_list[i] else None,
#                     'upper_lowerchest_body': upper_lowerchest_body_list[i] if upper_lowerchest_body_list[i] else None,
#                     'upper_lowerchest_ready': upper_lowerchest_ready_list[i] if upper_lowerchest_ready_list[i] else None,
#                     'upper_stomach_body': upper_stomach_body_list[i] if upper_stomach_body_list[i] else None,
#                     'upper_stomach_ready': upper_stomach_ready_list[i] if upper_stomach_ready_list[i] else None,
#                     'upper_hip_body': upper_hip_body_list[i] if upper_hip_body_list[i] else None,
#                     'upper_hip_ready': upper_hip_ready_list[i] if upper_hip_ready_list[i] else None,
#                     'upper_neck': upper_neck_list[i] if upper_neck_list[i] else None,
#                     'upper_other_remark': upper_other_remark_list[i] if upper_other_remark_list[i] else None,
#                 }

#             # Create lower maap data if it's not empty
#             lower_data = {}
#             if i < len(lower_maap_list) and any([
#                 lower_maap_list[i], lower_length_list[i], lower_waist_list[i], lower_hip_list[i],
#                 lower_thai_list[i], lower_knee_list[i], lower_bottom_list[i], lower_jhola_list[i],
#                 lower_remark_list[i]
#             ]):
#                 lower_data = {
#                     'lower_maap': lower_maap_list[i] if lower_maap_list[i] else None,
#                     'lower_length': lower_length_list[i] if lower_length_list[i] else None,
#                     'lower_waist': lower_waist_list[i] if lower_waist_list[i] else None,
#                     'lower_hip': lower_hip_list[i] if lower_hip_list[i] else None,
#                     'lower_thai': lower_thai_list[i] if lower_thai_list[i] else None,
#                     'lower_knee': lower_knee_list[i] if lower_knee_list[i] else None,
#                     'lower_bottom': lower_bottom_list[i] if lower_bottom_list[i] else None,
#                     'lower_jhola': lower_jhola_list[i] if lower_jhola_list[i] else None,
#                     'lower_other_remark': lower_remark_list[i] if lower_remark_list[i] else None,
#                 }

#             # Save only if there's data (upper or lower)
#             if upper_data:
#                 maap = MaapMaster(client=client, **upper_data)
#                 maap.save()
#             elif lower_data:
#                 maap = MaapMaster(client=client, **lower_data)
#                 maap.save()

#         # Redirect to another page after saving
#         return redirect('client_creation')  # Adjust to your desired redirect URL

#     else:
#         # Create an empty form instance to render for GET requests
#         maap_form = MaapCreation()

#     return render(request, 'client-creation.html', {
#         'maap_form': maap_form,  # This will render your form if needed
#     })



# def client_detail(request):
#     if request.method == 'POST':
#         maap_data = request.POST
#         maap_form = MaapCreation(request.POST)
#         if maap_form.is_valid():
#             maap = maap_form.save(commit=False)
#             maap.client = client
#             maap.save()
#         return redirect('client_detail', client.id)
#     return render(request, 'client-master.html', {'client': client})


# def client_creation(request,pk=None):
#     company_id = request.session.get('company_id')

#     # Get the logged-in company's object
#     # profile = user.userprofile  # Adjust based on your actual model
#     # company = profile.company  # Get the company linked to the user

#     company = Company.objects.get(id=company_id)

#     if request.method == 'POST':
#         form = ClientCreation(request.POST)
#         if form.is_valid():
#             new_client = form.save(commit=False)
#             new_client.company = company
#             new_client.save()
#             messages.success(request, 'Client Created Successfully!')
#             # return redirect('client_creation', pk=pk)  # Stay on the same page after saving
#     else:
#         form = ClientCreation()

#     # Fetch only the clients belonging to the logged-in company
#     clients = ClientMaster.objects.filter(company=company).prefetch_related('upper_maaps', 'lower_maaps').order_by('-id')

#     return render(request, 'client-master.html', {
#         'form': form,
#         'clients':clients,

#     })

from django.http import Http404
from django.contrib.auth.decorators import login_required


# @login_required  # Ensure that the user is logged in
# def client_creation(request, pk):
#     if request.user.is_authenticated:
#         if hasattr(request.user, 'company'):  # If the user is a company
#             try:
#                 company = Company.objects.get(id=pk)
#                 if request.user.id != company.id:  # Ensure the logged-in company matches the company ID
#                     raise Http404("You are not authorized to access this page.")

#                 # Continue with company-related logic here
#             except Company.DoesNotExist:
#                 raise Http404("Company not found")
#         elif hasattr(request.user, 'employee_master'):  # If the user is an employee
#             try:
#                 employee = EmployeeMaster.objects.get(id=request.user.id)
#                 company = employee.company  # Get the associated company
#                 # Continue with employee-related logic here
#             except EmployeeMaster.DoesNotExist:
#                 raise Http404("Employee not found")
#         else:
#             raise Http404("User is neither a company nor an employee")
#     else:
#         # Redirect to the login page if the user is not authenticated
#         return redirect('login')  # Adjust this to match your login URL

@login_required
def client_creation(request):
    if not request.user.is_company_owner:
        return HttpResponseForbidden("You do not have permission to add employees.")

    # company = Company.objects.get(superuser=request.user)
    if request.method == 'POST':
        form = ClientCreation(request.POST)
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.company = request.user.company
            new_client.save()
            messages.success(request, 'Client Created Successfully!')
#             # return redirect('client_creation', pk=pk)  # Stay on the same page after saving
    else:
        form = ClientCreation()
        messages.error(request, 'There was an error in creating Client!')

    # Fetch only the clients belonging to the logged-in company
    clients = ClientMaster.objects.filter(company=request.user.company).prefetch_related('upper_maaps', 'lower_maaps').order_by('-id')

    return render(request, 'client-master.html', {'form': form, 'clients': clients})
    # Access the company associated with the user and its ID

    # elif hasattr(request.user, 'employee_master'):  # Check if the logged-in user is an employee
    #     employee = get_object_or_404(EmployeeMaster, id=request.user.id)
    #     company = employee.company  # Get the company associated with the employee
    #     if company.id != pk:
    #         raise Http404("You are not authorized to access this page.")
    #     # Handle employee-specific logic here
    #     return render(request, 'client-creation.html', {'company': company, 'employee': employee})

    # else:
    #     raise Http404("User is neither a company nor an employee.")





def maap_view(request, client_id):

    # company_id = request.session.get('company_id')
    # company = Company.objects.get(id=company_id)
    client = get_object_or_404(ClientMaster, id=client_id)

    if request.method == 'POST':
        # Initialize formsets with POST data
        upper_formset = UpperMaapFormSet(request.POST, prefix='upper')
        lower_formset = LowerMaapFormSet(request.POST, prefix='lower')

        # Validate formsets
        upper_valid = upper_formset.is_valid()
        lower_valid = lower_formset.is_valid()

        if upper_valid:
            upper_instances = upper_formset.save(commit=False)
            for instance in upper_instances:
                instance.client = client
                instance.company = request.user.company
                instance.save()

        if lower_valid:
            lower_instances = lower_formset.save(commit=False)
            for instance in lower_instances:
                instance.client = client
                instance.company = request.user.company
                instance.save()

        # Redirect if both formsets are valid
        if upper_valid and lower_valid:

            return redirect('client_creation')  # Pass the company ID to the redirect

        # Log errors for invalid formsets
        if not upper_valid:
            print('Upper Formset Errors:', upper_formset.errors)
        if not lower_valid:
            print('Lower Formset Errors:', lower_formset.errors)

    else:
        # Empty formsets for initial render
        upper_formset = UpperMaapFormSet(queryset=UpperMaap.objects.none(), prefix='upper')
        lower_formset = LowerMaapFormSet(queryset=LowerMaap.objects.none(), prefix='lower')

    # Render formsets in the template
    return render(request, 'client-creation.html', {
        'client': client,
        'upper_formset': upper_formset,
        'lower_formset': lower_formset,
    })




def maap_edit_view(request, client_id):
    # company_id = request.session.get('company_id')
    # company = Company.objects.get(id=company_id)
    # Fetch the client instance
    client = get_object_or_404(ClientMaster, id=client_id)

    # Define formsets for UpperMaap and LowerMaap with the client's data
    UpperMaapFormSet = modelformset_factory(UpperMaap, form=UpperMaapForm, extra=0, can_delete=True)
    LowerMaapFormSet = modelformset_factory(LowerMaap, form=LowerMaapForm, extra=0, can_delete=True)

    if request.method == 'POST':
        # Instantiate all forms with POST data
        client_form = ClientCreation(request.POST, instance=client)
        upper_formset = UpperMaapFormSet(request.POST, queryset=UpperMaap.objects.filter(client=client), prefix='upper')
        lower_formset = LowerMaapFormSet(request.POST, queryset=LowerMaap.objects.filter(client=client), prefix='lower')

        # Validate all forms and formsets
        if client_form.is_valid() and upper_formset.is_valid() and lower_formset.is_valid():
            # Save client form
            client_form.save()

            # Save upper formset
            for upper_form in upper_formset:
                if upper_form.cleaned_data.get('DELETE'):
                    print("Deleting UpperMaap:", upper_form.instance.pk)
                    if upper_form.instance.pk:
                        upper_form.instance.delete()
                else:
                    upper_instance = upper_form.save(commit=False)
                    print("Saving UpperMaap:", upper_instance)
                    upper_instance.client = client
                    upper_instance.save()

            # Save lower formset
            for lower_form in lower_formset:
                if lower_form.cleaned_data.get('DELETE'):
                    print("Deleting UpperMaap:", lower_form.instance.pk)
                    if lower_form.instance.pk:
                        lower_form.instance.delete()
                else:
                    lower_instance = lower_form.save(commit=False)
                    print("Saving LowerMaap:", lower_instance)
                    lower_instance.client = client
                    lower_instance.save()

            messages.success(request, "Client details updated successfully!")
            print("Successful")
            return redirect('client_creation')  # Redirect to the list page or desired page

        else:
            print("Client Form Errors:", client_form.errors)
            print("UpperMaap Formset Errors:", upper_formset.errors)
            print("LowerMaap Formset Errors:", lower_formset.errors)
            messages.error(request, "Please correct the errors below.")

    else:
        # Instantiate forms with existing data
        client_form = ClientCreation(instance=client)
        upper_formset = UpperMaapFormSet(queryset=UpperMaap.objects.filter(client=client), prefix='upper')
        lower_formset = LowerMaapFormSet(queryset=LowerMaap.objects.filter(client=client), prefix='lower')

    return render(request, 'client-edit2.html', {
        'client_form': client_form,
        'upper_formset': upper_formset,
        'lower_formset': lower_formset,
        'client': client,
    })





# def generate_bill_number():
#     """Generates a dynamic bill number based on the financial year."""
#     current_year = datetime.now().year
#     next_year = current_year + 1 if datetime.now().month > 3 else current_year - 1
#     financial_year = f"{current_year % 100}/{next_year % 100}"
    
#     # Fetch the latest bill for the current financial year
#     last_bill = create_bill.objects.filter(
#         bill_number__contains=financial_year
#     ).order_by('-id').first()  # Using '-id' to fetch the most recent record

#     if last_bill:
#         try:
#             # Extract and increment the numeric part of the bill number
#             last_number = int(last_bill.bill_number.split('-')[-1])  # Get the last part
#             new_number = f"{last_number + 1:03d}"
#         except (ValueError, IndexError) as e:
#             # Log error and reset to 001 if parsing fails
#             print(f"Error parsing bill_number: {e}, resetting counter.")
#             new_number = "001"
#     else:
#         new_number = "001"  # Start from 001 if no bills exist for the financial year

#     return f"BILL-{financial_year}-{new_number}"


def generate_bill_number(company):
    """
    Generates a dynamic bill number based on the financial year and company.
    Each company will have its own sequence of bill numbers.
    """
    from datetime import datetime

    prefix = company.prefix

    current_month = datetime.now().month
    current_year = datetime.now().year

    # Determine the correct financial year
    if current_month >= 4:  # If the month is April or later, the financial year is current_year/current_year+1
        financial_year = f"{current_year % 100}/{(current_year + 1) % 100}"
    else:  # If the month is January to March, the financial year is previous_year/current_year
        financial_year = f"{(current_year - 1) % 100}/{current_year % 100}"

    # Fetch the latest bill for the company in the current financial year
    last_bill = create_bill.objects.filter(
        company=company,
        bill_number__contains=financial_year
    ).order_by('-id').first()  # Fetch the most recent bill for the company

    if last_bill:
        try:
            # Extract and increment the numeric part of the bill number
            last_number = int(last_bill.bill_number.split('-')[-1])  # Get the last part
            new_number = f"{last_number + 1:03d}"
        except (ValueError, IndexError) as e:
            # Log error and reset to 001 if parsing fails
            print(f"Error parsing bill_number: {e}, resetting counter.")
            new_number = "001"
    else:
        new_number = "001"  # Start from 001 if no bills exist for the company in the financial year

    return f"{prefix}-{financial_year}-{new_number}"



# =========================================================
def create_bill_view(request, client_id):
    client = get_object_or_404(ClientMaster, id=client_id)

    ProductFormSet = modelformset_factory(product_list, form=productForms, extra=1, can_delete=True)
    AdvanceFormSet = modelformset_factory(advance_list, form=advanceForms, extra=1, can_delete=True)
    company = request.user.company
    initial_bill_number = generate_bill_number(company)

    if request.method == "POST":
        bill_form = billForms(request.POST)
        product_formset = ProductFormSet(request.POST, queryset=product_list.objects.none(), prefix="product_form", form_kwargs={"company": company})
        advance_formset = AdvanceFormSet(request.POST, queryset=advance_list.objects.none(), prefix="advance_form")

        if bill_form.is_valid() and product_formset.is_valid() and advance_formset.is_valid():
            # Save bill instance
            bill_instance = bill_form.save(commit=False)
            bill_instance.client = client
            bill_instance.company = company  # Assign the company to the bill instance

            if not bill_instance.bill_number:
                bill_instance.bill_number = initial_bill_number

            bill_instance.save()

            # Save products
            for product_form in product_formset:
                if product_form.cleaned_data and not product_form.cleaned_data.get('DELETE', False):
                    product_instance = product_form.save(commit=False)
                    product_instance.invoice = bill_instance
                    product_instance.company = company  # Assign the company to the product instance
                    product_instance.save()

            # Save advances
            for advance_form in advance_formset:
                if advance_form.cleaned_data and not advance_form.cleaned_data.get('DELETE', False):
                    advance_instance = advance_form.save(commit=False)
                    advance_instance.invoice = bill_instance
                    advance_instance.company = company  # Ensure the company field is set
                    advance_instance.save()

            return redirect("bill_list")  # Redirect to the desired page after successful save
        else:
            print("Bill Form Errors:", bill_form.errors)
            print("Product Formset Errors:", product_formset.errors)
            print("Advance Formset Errors:", advance_formset.errors)
    else:
        bill_form = billForms(initial={"bill_number": initial_bill_number})
        product_formset = ProductFormSet(queryset=product_list.objects.none(), prefix="product_form", form_kwargs={"company": company})
        advance_formset = AdvanceFormSet(queryset=advance_list.objects.none(), prefix="advance_form")

    context = {
        "bill_form": bill_form,
        "bill_number": initial_bill_number,
        "product_formset": product_formset,
        "advance_formset": advance_formset,
        "client": client,
        'company': company,
    }
    return render(request, "create-bill.html", context)


# new
# def create_bill_view(request, client_id):
#     company_id = request.session.get('company_id')
#     company = Company.objects.get(id=company_id)
#     client = get_object_or_404(ClientMaster, id=client_id)

#     initial_bill_number = generate_bill_number(company)

#     if request.method == "POST":
#         bill_form = billForms(request.POST)
#         product_formset = ProductFormSet(
#             request.POST, queryset=product_list.objects.none(), prefix="product_form", form_kwargs={"company": company}
#         )
#         advance_formset = AdvanceFormSet(
#             request.POST, queryset=advance_list.objects.none(), prefix="advance_form"
#         )

#         if bill_form.is_valid() and product_formset.is_valid() and advance_formset.is_valid():
#             bill_instance = bill_form.save(commit=False)
#             bill_instance.client = client
#             bill_instance.company = company

#             if not bill_instance.bill_number:
#                 bill_instance.bill_number = initial_bill_number

#             bill_instance.save()

#             # Save products
#             for product_form in product_formset:
#                 if product_form.cleaned_data and not product_form.cleaned_data.get('DELETE', False):
#                     product_instance = product_form.save(commit=False)
#                     product_instance.invoice = bill_instance
#                     product_instance.company = company
#                     product_instance.save()

#             # Save advances
#             for advance_form in advance_formset:
#                 if advance_form.cleaned_data and not advance_form.cleaned_data.get('DELETE', False):
#                     advance_instance = advance_form.save(commit=False)
#                     advance_instance.invoice = bill_instance
#                     advance_instance.save()

#             return redirect("bill_list")
#         else:
#             print("Bill Form Errors:", bill_form.errors)
#             print("Product Formset Errors:", product_formset.errors)
#             print("Advance Formset Errors:", advance_formset.errors)
#     else:
#         bill_form = billForms(initial={"bill_number": initial_bill_number})
#         product_formset = ProductFormSet(
#             queryset=product_list.objects.none(), prefix="product_form", form_kwargs={"company": company}
#         )
#         advance_formset = AdvanceFormSet(queryset=advance_list.objects.none(), prefix="advance_form")

#     context = {
#         "bill_form": bill_form,
#         "bill_number": initial_bill_number,
#         "product_formset": product_formset,
#         "advance_formset": advance_formset,
#         "client": client,
#         'company': company,
#     }
#     return render(request, "create-bill.html", context)




# ---------------------------------------------


#This is working code-------------------
def edit_advance_form(request, bill_id):
    bill = get_object_or_404(create_bill, id=bill_id)
    client = bill.client
    company = bill.company  # Assuming the bill is associated with a company
    AdvanceFormSet = modelformset_factory(advance_list, form=advanceForms, extra=1, can_delete=True)
    formset = AdvanceFormSet(queryset=advance_list.objects.filter(invoice=bill))

    if request.method == 'POST':
        bill_form = billForms(request.POST, instance=bill)
        formset = AdvanceFormSet(request.POST, queryset=advance_list.objects.filter(invoice=bill))
        if formset.is_valid() and bill_form.is_valid():

            # Update bill fields
            bill.amount_receivable = bill_form.cleaned_data.get('amount_receivable', bill.amount_receivable)
            bill.total_amount_received = bill_form.cleaned_data.get('total_amount_received', bill.total_amount_received)
            bill.save(update_fields=['amount_receivable', 'total_amount_received'])

            # Save all valid forms (both existing and new)
            advances = formset.save(commit=False)
            for advance in advances:
                advance.invoice = bill  # Associate the advance with the correct bill
                advance.company = company  # Ensure the company field is set
                advance.save()

            # Handle deleted forms
            for deleted_form in formset.deleted_objects:
                deleted_form.delete()

            return redirect('bill_list')  # Redirect to another page after saving

    return render(request, 'bill-edit.html', {'formset': formset, 'bill': bill, 'client': client, 'bill_number': bill.bill_number})



# -----------------------------------------------



def bill_list(request,pk=None):
    # company_id = request.session.get('company_id')

    # company = Company.objects.get(id=company_id)
    company = request.user.company
    bills = create_bill.objects.filter(company=company).order_by('-id')

    total_bill_sum = bills.aggregate(Sum('total_bill'))['total_bill__sum'] or 0
    total_amount_received_sum = bills.aggregate(Sum('total_amount_received'))['total_amount_received__sum'] or 0
    balance_receivable_sum = bills.aggregate(Sum('amount_receivable'))['amount_receivable__sum'] or 0

    context = {
        "bills": bills,
        "total_bill_sum": total_bill_sum,
        "total_amount_received_sum": total_amount_received_sum,
        "balance_receivable_sum": balance_receivable_sum,
        'company': company,
    }
    return render(request, "bill-master.html", context)


#This is the code for bill's detail page
def bill_detail_view(request, bill_id):


    if not hasattr(request.user, 'company'):
        return render(request, 'bill-detail.html', {
            'error': 'You are not associated with any company.'
        })

    # Fetch the company associated with the user
    company = request.user.company


    # Fetch the bill instance
    bill = get_object_or_404(create_bill, id=bill_id)
    amount_in_words = num2words(bill.total_bill, lang='en').capitalize()

    # Fetch the associated client details
    client = bill.client

    # Fetch associated product and advance lists
    products = product_list.objects.filter(invoice=bill)
    advances = advance_list.objects.filter(invoice=bill)

    upper_maap_details = UpperMaap.objects.filter(client=client)
    lower_maap_details = LowerMaap.objects.filter(client=client)


    context = {
        "bill": bill,
        "client": client,
        "products": products,
        "advances": advances,
        "amount_in_words": amount_in_words,
        "upper_maap_details": upper_maap_details,
        "lower_maap_details": lower_maap_details,
        "company": company,
    }

    return render(request, "bill-detail.html", context)


def maap_detail_view(request, bill_id):

    bill = get_object_or_404(create_bill, id=bill_id)

    client = bill.client

    upper_maap_details = UpperMaap.objects.filter(client=client)
    lower_maap_details = LowerMaap.objects.filter(client=client)

    context = {
        "bill": bill,
        "client": client,
        "upper_maap_details": upper_maap_details,
        "lower_maap_details": lower_maap_details,
    }

    return render(request, "maap-detail.html", context)



# def employee_creation(request,pk=None):
#     company_id = request.session.get('company_id')

#     company = Company.objects.get(id=company_id)

#     if request.method == 'POST':
#         form = EmployeeRegistrationForm(request.POST)
#         if form.is_valid():
#             employee = form.save(commit=False)
#             employee.company = company
#             employee.save()
#             # login(request, employee)  # Log the employee in after successful registration
#             return redirect('employee_creation', pk=company.id)
#     else:
#         form = EmployeeRegistrationForm()
#     return render(request, 'employee_register.html', {'form': form}) 


# def employee_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         employee = authenticate(request, username=username, password=password)
#         if employee is not None:
#             login(request, employee)
#             return redirect('home')
#         else:
#             return render(request, 'employee_login.html', {'error': 'Invalid credentials'})
#     return render(request, 'employee_login.html')


# Employee Creation
# def employee_creation(request, pk=None):
#     company_id = request.session.get('company_id')

#     company = Company.objects.get(id=company_id)
#     if request.method == 'POST':

#         form = EmployeeCreation(request.POST)
#         if form.is_valid():
#             form2 = form.save(commit=False)
#             form2.password = make_password(form.cleaned_data['password'])  # Hash the password
#             form2.company = company # Hash the password

#             form2.save()  # Save the form to create a new EmployeeMaster object
#             messages.success(request, 'User registered successfully!')
#             return redirect('employee_creation', pk=company.id)
#     else:
#         form = EmployeeCreation()

#     # Fetch all employees from the EmployeeMaster model
#     employees = EmployeeMaster.objects.filter(company=company).order_by('-id')
#     print("Company ID from session:", company_id)
#     print("Employees:", employees)


#     # Render the template with the form and employee details
#     return render(request, 'employee-master.html', {'form': form,'employees':employees,'company':company})

# @login_required
# def employee_creation(request, pk=None):
#     if not isinstance(request.user, Company):
#         return redirect('company_login')

#     if request.method == 'POST':
#         print(request.user.id,'hhhhhhhhh')
#         form = EmployeeRegistrationForm(request.POST)
#         if form.is_valid():
#             company = request.user
#             form.save(company=company.id)  # Assign the logged-in company
#             return redirect('client_creation', pk=request.company.id)
#   # Redirect to company dashboard
#     else:
#         form = EmployeeRegistrationForm()
#     return render(request, 'new/register_employee.html', {'form': form})

# def employee_creation(request, pk=None):
#     if request.user.is_authenticated:
#         if hasattr(request.user, 'company'):
#             company = request.user  # Get the actual Company instance

#             form = EmployeeRegistrationForm(request.POST)  # Assuming you're using a form
#             if form.is_valid():
#                 employee = form.save(commit=False)
#                 employee.company = company  # Assign the Company instance to employee

#                 employee.save()  # Save the employee instance
#                 return redirect('client_creation', pk=company.id)  # Redirect to the company page
#             else:
#                 # Handle form errors
#                 pass
#         else:
#             # Handle the case where the user does not have a company
#             raise Http404("User does not belong to a company")
#     else:
#         # Handle case where the user is not authenticated
#         return redirect('login')

# Unified Login View for Company and User/Employee
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email_or_username = form.cleaned_data['email_or_username']
#             password = form.cleaned_data['password']

#             # Authenticate company using custom backend
#             company = authenticate(request, username=email_or_username, password=password)
#             if company is not None and isinstance(company, Company):
#                 request.session['company_id'] = company.id
#                 login(request, company)  # Log in the company
#                 messages.success(request, 'Company login successful!')
#                 return redirect('client_creation', pk=company.id)  # Redirect to the client creation page

#             # Authenticate employee using custom backend
#             employee = authenticate(request, username=email_or_username, password=password)
#             if employee is not None and isinstance(employee, EmployeeMaster):
#                 request.session['employee_id'] = employee.id
#                 login(request, employee)  # Log in the employee
#                 messages.success(request, 'Employee login successful!')
#                 return redirect('client_creation', pk=employee.company.id)  # Redirect with the company ID

#             # Invalid credentials
#             messages.error(request, 'Invalid credentials. Please try again.')
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})


# def register_user(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.password = form.cleaned_data['password']
#             user.save()
#             messages.success(request, 'User registered successfully!')
#             return redirect('user_login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'register_user.html', {'form': form})

# Login
from django.contrib.auth.hashers import check_password


# Employee Report
def product_list_view(request):
    # Check if the logged-in user has an associated company
    if not hasattr(request.user, 'company'):
        return render(request, 'employee-report.html', {
            'error': 'You are not associated with any company.'
        })

    # Get the logged-in user's company
    company = request.user.company

    # Determine filtering logic based on the user's role
    if request.user.is_company_owner:
        # If the user is a company owner, show all products in their company
        products = product_list.objects.select_related('invoice', 'product_assignedTo') \
            .filter(company=company)
    else:
        # If the user is an employee, show only products assigned to them
        products = product_list.objects.select_related('invoice', 'product_assignedTo') \
            .filter(company=company, product_assignedTo=request.user)

    # Prepare the data to pass to the template
    product_data = []
    for product in products:
        product_data.append({
            'product_name': product.product_name,
            'product_remark': product.product_remark,
            'quantity': product.quantity,
            'rate': product.rate,
            'amount': product.amount,
            'bill_number': product.invoice.bill_number,  # Assuming 'bill_number' is a field in 'create_bill' model
            'delivery_date': product.invoice.delivery_date,
            'assigned_to': product.product_assignedTo.employee_name if product.product_assignedTo else 'N/A',
        })

    # Render the template with the data
    return render(request, 'employee-report.html', {'product_data': product_data})


def company_detail(request):
    # Check if the logged-in user is associated with a company
    if not hasattr(request.user, 'company'):
        return render(request, 'company-detail.html', {
            'error': 'You are not associated with any company.'
        })

    # Fetch the company associated with the user
    company = request.user.company

    # Prepare the company data for the template
    company_data = {
        'company_name': company.company_name,
        'logo': company.logo.url if company.logo else None,
        'name': company.name,
        'email': company.email,
        'phone': company.phone,
        'address': company.address,
        'created_at': company.created_at,
        'updated_at': company.updated_at,
        'prefix': company.prefix,
    }

    return render(request, 'company-detail.html', {'company': company_data})


def update_company(request):
    # company = get_object_or_404(Company, id=company_id)  # Fetch the company to update
    company = request.user.company
    print(company,'uuuuuuuu')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()  # Save the updated company details
            return redirect('company_detail')  # Redirect to company detail view (modify as needed)
    else:
        form = CompanyForm(instance=company)  # Pre-fill form with current company data

    return render(request, 'edit-profile.html', {'form': form})




# All advances in one table
# from django.shortcuts import render, get_object_or_404

def advance_list_view(request):
    # Check if the logged-in user has an associated company
    if not hasattr(request.user, 'company'):
        return render(request, 'advance-report.html', {
            'error': 'You are not associated with any company.'
        })

    # Get the logged-in user's company
    company = request.user.company

    # Determine filtering logic based on the user's role
    if request.user.is_company_owner:
        # If the user is a company owner, fetch all advances for their company
        advances = advance_list.objects.select_related('invoice').filter(company=company)
    else:
        pass
        # If the user is an employee, limit the data they can see
        # advances = advance_list.objects.select_related('invoice').filter(
        #     company=company, invoice__assigned_to=request.user
        # )

    # Prepare the data to pass to the template
    advance_data = []
    for advance in advances:
        advance_data.append({
            'receipt_ref_no': advance.receipt_ref_no,
            'receipt_type': advance.receipt_type,
            'receipt_date': advance.receipt_date,
            'amount_received': advance.amount_received,
            'client_name': advance.invoice.client.client_name,  # Assuming 'client' is a ForeignKey in 'create_bill'
            'bill_date': advance.invoice.bill_date,
            'bill_number': advance.invoice.bill_number,  # Assuming 'bill_number' is a field in 'create_bill' model
        })

    # Render the template with the data
    return render(request, 'advance-report.html', {'advance_data': advance_data})
