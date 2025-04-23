from django.contrib import admin
from hospital.models import (
    Medicine,
    Patient,
    TreatmentMedicine,
    Treatment,
    Appointment,
)

from django.utils.translation import gettext_lazy as _
from hospital_ms.utils.admin import DevelopmentImportExportModelAdmin

# Register your models here.


@admin.register(Medicine)
class MedicineAdmin(DevelopmentImportExportModelAdmin):
    list_display = (
        "name",
        "short_name",
        "category",
        "stock",
        "price",
        "expiry_date",
        "created_at",
    )
    search_fields = ("name", "short_name", "category")
    list_filter = ("category", "expiry_date", "created_at")
    list_editable = ("price", "stock")


@admin.register(Patient)
class PatientAdmin(DevelopmentImportExportModelAdmin):
    search_fields = ("user__username",)
    list_filter = ("created_at",)

    def active_treatments(self, obj) -> int:
        return obj.treatments.count()

    def pending_bill(self, obj: Patient) -> float:
        if obj.user.account.balance < 0:
            return abs(obj.user.account.balance)
        else:
            return 0

    active_treatments.short_description = _("Active Treatments")
    list_display = ("user", "active_treatments", "pending_bill", "created_at")


@admin.register(TreatmentMedicine)
class TreatmentMedicineAdmin(DevelopmentImportExportModelAdmin):
    list_display = ("medicine", "quantity", "prescription", "updated_at", "created_at")
    search_fields = ("medicine__name",)
    list_filter = ("updated_at", "created_at")


@admin.register(Treatment)
class TreatmentAdmin(DevelopmentImportExportModelAdmin):
    def active_doctors(self, obj: Treatment):
        return obj.doctors.count()

    active_doctors.short_description = _("Active Doctors")

    def total_billed(self, obj: Treatment):
        return obj.total_bill

    total_billed.short_description = _("Total billed")
    list_display = (
        "patient",
        "patient_type",
        "diagnosis",
        "treatment_status",
        "active_doctors",
        "total_billed",
        "updated_at",
    )
    search_fields = ("patient__user__username", "diagnosis")
    list_filter = (
        "patient_type",
        "doctors",
        "treatment_status",
        "updated_at",
        "created_at",
    )
    fieldsets = (
        (None, {"fields": ("patient", "patient_type", "doctors")}),
        (
            _("Treatment"),
            {"fields": ("diagnosis", "details", "medicines", "treatment_status")},
        ),
        (_("Fees"), {"fields": ("extra_fees",)}),
    )


@admin.register(Appointment)
class AppointmentAdmin(DevelopmentImportExportModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "appointment_datetime",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("patient__user__username", "doctor__user__username")
    list_filter = ("status", "appointment_datetime", "updated_at", "created_at")
    list_editable = ("status",)
