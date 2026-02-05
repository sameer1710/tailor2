# importer/views/step_clients.py
from django.http import HttpResponse

def client_template(request):
    headers = [
        'client_name',
        'client_number',
        'book_number',
        'page_number',
        'client_address',
        'client_status'
    ]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=clients.csv'
    response.write(','.join(headers))
    return response


# importer/views/step_clients.py
import csv
from django.db import transaction
from django.shortcuts import redirect, render
from importer.models import ImportSession
from api.models import ClientMaster

def import_clients(request):
    session = ImportSession.objects.get(company=request.user.company)

    if request.method == 'POST':
        file = request.FILES['file']

        reader = csv.DictReader(file.read().decode('utf-8').splitlines())

        required = {
            'client_name', 'client_number',
            'book_number', 'page_number',
            'client_address', 'client_status'
        }

        if not required.issubset(reader.fieldnames):
            session.last_error = "Invalid CSV columns"
            session.save()
            return render(request, 'importer/error.html')

        try:
            with transaction.atomic():
                for row in reader:
                    ClientMaster.objects.create(
                        company=request.user.company,
                        client_name=row['client_name'].strip(),
                        client_number=row['client_number'],
                        book_number=row['book_number'],
                        page_number=row['page_number'],
                        client_address=row['client_address'],
                        client_status=row['client_status']
                    )

                session.current_step = 'maap'
                session.save()

        except Exception as e:
            session.last_error = str(e)
            session.save()
            raise

        return redirect('import_wizard')

    return render(request, 'importer/step_clients.html')
