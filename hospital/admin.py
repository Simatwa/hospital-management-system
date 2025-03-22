from django.contrib import admin
from hospital.models import (
    WorkingDay,
    Department,
    Speciality,
    Medicine,
    Doctor,
    Patient,
    TreatmentMedicine,
    Treatment,
    Appointment,
)

from django.utils.translation import gettext_lazy as _

# Register your models here.


@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("created_at",)

    def total_doctors(self, obj: WorkingDay):
        return obj.doctors.count()

    total_doctors.short_description = _("Total Doctors")

    list_display = ("name", "total_doctors", "created_at")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name", "lead__username")
    list_filter = ("created_at",)
    list_editable = ("lead",)

    def total_specialities(self, obj):
        return obj.specialities.count()

    total_specialities.short_description = _("Total Specialities")

    list_display = ("name", "lead", "total_specialities", "created_at")


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    search_fields = ("name", "department__name")
    list_filter = ("updated_at", "created_at")
    list_display = (
        "name",
        "department",
        "appointment_charges",
        "treatment_charges",
        "updated_at",
    )


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
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


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "speciality__name")
    list_filter = ("shift", "speciality", "speciality__department", "created_at")
    list_editable = ("shift",)

    def active_treatments(self, obj):
        return obj.treatments.count()

    active_treatments.short_description = _("Active Treatments")

    def active_appointments(self, obj):
        return obj.appointments.filter(
            status=Appointment.AppointmentStatus.SCHEDULED.value,
        ).count()

    active_appointments.short_description = _("Active Appointments")
    list_display = (
        "user",
        "speciality",
        "shift",
        "active_treatments",
        "active_appointments",
        "created_at",
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
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
class TreatmentMedicineAdmin(admin.ModelAdmin):
    list_display = ("medicine", "quantity", "prescription", "updated_at", "created_at")
    search_fields = ("medicine__name",)
    list_filter = ("updated_at", "created_at")


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
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
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
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
