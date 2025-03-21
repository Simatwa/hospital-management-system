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
    search_fields = ("name",)
    list_filter = ("created_at",)

    def total_doctors(self, obj: WorkingDay):
        return obj.doctors.count()

    total_doctors.short_description = "Total Doctors"

    list_display = ("name", "total_doctors", "created_at")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name", "lead__username")
    list_filter = ("created_at",)
    list_editable = ("lead",)

    def total_specialities(self, obj):
        return obj.specialities.count()

    total_specialities.short_description = "Total Specialities"

    list_display = ("name", "lead", "total_specialities", "created_at")


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    search_fields = ("name", "department__name")
    list_filter = ("updated_at", "created_at")
    list_display = ("name", "department", "updated_at", "created_at")


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "category",
        "expiry_date",
        "stock",
        "price",
        "updated_at",
    )
    search_fields = ("name", "short_name", "category")
    list_filter = ("category", "expiry_date", "updated_at", "created_at")
    list_editable = ("price", "stock")


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    search_fields = ("user__username", "specialty__name")
    list_filter = ("shift", "created_at")
    list_editable = ("shift",)

    def total_treatments(self, obj):
        return obj.treatments.count()

    total_treatments.short_description = "Total Treatments"

    def total_appointments(self, obj):
        return obj.appointments.count()

    total_appointments.short_description = "Total Appointments"
    list_display = (
        "user",
        "specialty",
        "shift",
        "total_treatments",
        "total_appointments",
        "created_at",
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ("user__username",)
    list_filter = ("created_at",)

    def total_treatments(self, obj):
        return obj.treatments.count()

    total_treatments.short_description = "Total Treatments"
    list_display = ("user", "total_treatments", "created_at")


@admin.register(TreatmentMedicine)
class TreatmentMedicineAdmin(admin.ModelAdmin):
    list_display = ("medicine", "quantity", "prescription", "updated_at", "created_at")
    search_fields = ("medicine__name",)
    list_filter = ("updated_at", "created_at")


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    def total_doctors(self, obj: Treatment):
        return obj.doctors.count()

    total_doctors.short_description = "Total Doctors"
    list_display = (
        "patient",
        "type",
        "diagnosis",
        "total_doctors",
        "is_complete",
        "updated_at",
    )
    search_fields = ("patient__user__username", "diagnosis")
    list_filter = ("type", "doctors", "is_complete", "updated_at", "created_at")
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
    list_filter = ("status", "appointment_date", "updated_at", "created_at")
    list_editable = ("status",)
