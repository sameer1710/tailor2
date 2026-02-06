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
    """
    Import Upper / Lower MAAP via CSV.

    Rules:
    - Client matching ONLY by client_name + company
    - If multiple clients match → MAAP created for ALL
    - Duplicate MAAP types are ALLOWED
    - Partial data allowed (empty fields → NULL)
    - Can be run multiple times
    """

    if not ClientMaster.objects.filter(company=request.user.company).exists():
        messages.error(
            request,
            "No clients found. Please import clients before importing MAAP."
        )
        return redirect("import_wizard")

    if request.method == "POST":
        maap_type = request.POST.get("maap_type")
        file = request.FILES.get("file")

        if not maap_type or not file:
            messages.error(request, "MAAP type and CSV file are required.")
            return redirect("import_maap")

        try:
            reader = csv.DictReader(TextIOWrapper(file, encoding="utf-8"))

            if "client_name" not in reader.fieldnames:
                messages.error(
                    request,
                    "CSV must contain a 'client_name' column."
                )
                return redirect("import_maap")

            created_count = 0

            with transaction.atomic():
                for row_no, row in enumerate(reader, start=2):

                    client_name = (row.get("client_name") or "").strip()
                    if not client_name:
                        raise ValueError(
                            f"Missing client_name at row {row_no}"
                        )

                    clients = ClientMaster.objects.filter(
                        client_name=client_name,
                        company=request.user.company
                    )

                    if not clients.exists():
                        raise ValueError(
                            f"No client found with name '{client_name}' (row {row_no})"
                        )

                    # 👉 Create MAAP for EACH matching client
                    for client in clients:

                        # 🔼 UPPER MAAP
                        if maap_type == "upper":
                            UpperMaap.objects.create(
                                client=client,
                                upper_maap=row.get("upper_maap") or None,
                                upper_length=row.get("upper_length") or None,
                                upper_shoulder=row.get("upper_shoulder") or None,
                                upper_sleeve_length=row.get("upper_sleeve_length") or None,
                                upper_sleeve_bicep=row.get("upper_sleeve_bicep") or None,
                                upper_sleeve_cuff=row.get("upper_sleeve_cuff") or None,
                                upper_chest_body=row.get("upper_chest_body") or None,
                                upper_chest_ready=row.get("upper_chest_ready") or None,
                                upper_lowerchest_body=row.get("upper_lowerchest_body") or None,
                                upper_lowerchest_ready=row.get("upper_lowerchest_ready") or None,
                                upper_stomach_body=row.get("upper_stomach_body") or None,
                                upper_stomach_ready=row.get("upper_stomach_ready") or None,
                                upper_hip_body=row.get("upper_hip_body") or None,
                                upper_hip_ready=row.get("upper_hip_ready") or None,
                                upper_neck=row.get("upper_neck") or None,
                                upper_other_remark=row.get("upper_other_remark") or None,
                            )

                        # 🔽 LOWER MAAP
                        elif maap_type == "lower":
                            LowerMaap.objects.create(
                                client=client,
                                lower_maap=row.get("lower_maap") or None,
                                lower_length=row.get("lower_length") or None,
                                lower_waist=row.get("lower_waist") or None,
                                lower_hip=row.get("lower_hip") or None,
                                lower_thai=row.get("lower_thai") or None,
                                lower_knee=row.get("lower_knee") or None,
                                lower_bottom=row.get("lower_bottom") or None,
                                lower_jhola=row.get("lower_jhola") or None,
                                lower_other_remark=row.get("lower_other_remark") or None,
                            )

                        else:
                            raise ValueError("Invalid MAAP type selected.")

                        created_count += 1

            messages.success(
                request,
                f"MAAP imported successfully. {created_count} MAAP records created."
            )
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
