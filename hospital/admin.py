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

# Register your models here.


@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "lead", "created_at")
    search_fields = ("name", "lead__username")
    list_filter = ("created_at",)
    list_editable = ("lead",)


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "created_at", "updated_at")
    search_fields = ("name", "department__name")
    list_filter = ("created_at", "updated_at")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "category",
        "expiry_date",
        "price",
        "stock",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "short_name", "category")
    list_filter = ("category", "expiry_date", "created_at", "updated_at")
    list_editable = ("price", "stock")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user", "specialty", "shift", "salary", "created_at")
    search_fields = ("user__username", "specialty__name")
    list_filter = ("shift", "created_at")
    list_editable = ("shift", "salary")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("user__username",)
    list_filter = ("created_at",)


@admin.register(TreatmentMedicine)
class TreatmentMedicineAdmin(admin.ModelAdmin):
    list_display = ("medicine", "quantity", "prescription", "created_at", "updated_at")
    search_fields = ("medicine__name",)
    list_filter = ("created_at", "updated_at")


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "type",
        "diagnosis",
        "is_complete",
        "created_at",
        "updated_at",
    )
    search_fields = ("patient__user__username", "diagnosis")
    list_filter = ("type", "is_complete", "created_at", "updated_at")
    list_editable = ("is_complete",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "appointment_date",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("patient__user__username", "doctor__user__username")
    list_filter = ("status", "appointment_date", "created_at", "updated_at")
    list_editable = ("status",)
