import csv
from io import TextIOWrapper

from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from api.models import ClientMaster, UpperMaap, LowerMaap



def normalize_choice(value, choices):
    """
    Accepts either choice KEY or LABEL from CSV and returns KEY.
    Example: 'Zubba' or 'zubba' → 'zubba'
    """
    if not value:
        return None

    value = value.strip().lower()
    for key, label in choices:
        if value == key.lower() or value == label.lower():
            return key
    return None


@login_required
def import_maap(request):

    # 🔐 Ensure clients exist
    if not ClientMaster.objects.filter(company=request.user.company).exists():
        messages.error(request, "Please import clients before importing MAAP.")
        return redirect("import_wizard")

    if request.method == "POST":
        maap_type = request.POST.get("maap_type")
        file = request.FILES.get("file")

        if maap_type not in ("upper", "lower") or not file:
            messages.error(request, "MAAP type and CSV file are required.")
            return redirect("import_maap")

        try:
            reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))

            if "client_name" not in reader.fieldnames:
                messages.error(request, "CSV must contain 'client_name' column.")
                return redirect("import_maap")

            with transaction.atomic():
                for row_no, row in enumerate(reader, start=2):
                    client_name = row.get("client_name", "").strip()

                    if not client_name:
                        raise ValueError(f"Missing client_name at row {row_no}")

                    try:
                        client = ClientMaster.objects.get(
                            client_name=client_name,
                            company=request.user.company
                        )
                    except ClientMaster.DoesNotExist:
                        raise ValueError(
                            f"Client '{client_name}' not found (row {row_no})"
                        )

                    # 🔼 UPPER MAAP
                    if maap_type == "upper":
                        data = {}

                        for field in UpperMaap._meta.fields:
                            fname = field.name
                            if fname in ("id", "client", "upper_design_image"):
                                continue

                            value = row.get(fname)
                            data[fname] = value if value not in ("", None) else None

                        data["upper_maap"] = normalize_choice(
                            row.get("upper_maap"),
                            UpperMaap.TYPE_CHOICES
                        )

                        UpperMaap.objects.create(client=client, **data)

                    # 🔽 LOWER MAAP
                    else:
                        data = {}

                        for field in LowerMaap._meta.fields:
                            fname = field.name
                            if fname in ("id", "client", "lower_design_image"):
                                continue

                            value = row.get(fname)
                            data[fname] = value if value not in ("", None) else None

                        data["lower_maap"] = normalize_choice(
                            row.get("lower_maap"),
                            LowerMaap.TYPE_CHOICES
                        )

                        LowerMaap.objects.create(client=client, **data)

            messages.success(request, "MAAP data imported successfully.")
            return redirect("import_maap")

        except Exception as e:
            messages.error(request, f"Import failed: {e}")
            return redirect("import_maap")

    return render(request, "importer/step_maap.html")


@login_required
def upper_maap_template(request):
    headers = [
        "client_name",
        "upper_maap",
        "upper_length",
        "upper_shoulder",
        "upper_sleeve_length",
        "upper_sleeve_bicep",
        "upper_sleeve_cuff",
        "upper_chest_body",
        "upper_chest_ready",
        "upper_lowerchest_body",
        "upper_lowerchest_ready",
        "upper_stomach_body",
        "upper_stomach_ready",
        "upper_hip_body",
        "upper_hip_ready",
        "upper_neck",
        "upper_other_remark",
    ]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=upper_maap_template.csv"
    response.write(",".join(headers))
    return response


@login_required
def lower_maap_template(request):
    headers = [
        "client_name",
        "lower_maap",
        "lower_length",
        "lower_waist",
        "lower_hip",
        "lower_thai",
        "lower_knee",
        "lower_bottom",
        "lower_jhola",
        "lower_other_remark",
    ]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=lower_maap_template.csv"
    response.write(",".join(headers))
    return response
