# your_app/context_processors.py

from .models import Company

def company_logo(request):
    # Fetch company data for the logged-in user
    company = None
    if request.user.is_authenticated:
        try:
            company = request.user.company
        except AttributeError:
            company = None
    return {'company_data': company}
