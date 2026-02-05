# importer/urls.py
from django.urls import path
from importer.views import wizard, step_clients, step_maap

urlpatterns = [
    path('', wizard.import_wizard, name='import_wizard'),

    path('clients/', step_clients.import_clients, name='import_clients'),
    path('clients/template/', step_clients.client_template, name='client_template'),

    path('maap/', step_maap.import_maap, name='import_maap'),
    path('maap/upper-template/', step_maap.upper_maap_template, name='upper_maap_template'),
    path('maap/lower-template/', step_maap.lower_maap_template, name='lower_maap_template'),
]
