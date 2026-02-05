# importer/views/wizard.py
from django.shortcuts import render
from importer.models import ImportSession

def import_wizard(request):
    session, _ = ImportSession.objects.get_or_create(
        company=request.user.company
    )

    return render(request, 'importer/wizard.html', {
        'session': session
    })
