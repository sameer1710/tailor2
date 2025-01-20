from django.core.exceptions import PermissionDenied

def company_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_company:
            raise PermissionDenied("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def employee_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_employee:
            raise PermissionDenied("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
