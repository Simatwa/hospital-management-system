from django.contrib import admin
from staffing.models import Department, WorkingDay, Speciality, Doctor
from hospital.models import Appointment
from django.utils.translation import gettext_lazy as _
from hospital_ms.utils.admin import DevelopmentImportExportModelAdmin

# Register your models here.


@admin.register(Department)
class DepartmentAdmin(DevelopmentImportExportModelAdmin):
    search_fields = ("name", "lead__username")
    list_filter = ("created_at",)
    list_editable = ("lead",)

    def total_specialities(self, obj):
        return obj.specialities.count()

    total_specialities.short_description = _("Total Specialities")

    list_display = ("name", "lead", "total_specialities", "created_at")


@admin.register(WorkingDay)
class WorkingDayAdmin(DevelopmentImportExportModelAdmin):
    search_fields = ("name",)
    list_filter = ("created_at",)

    def total_doctors(self, obj: WorkingDay):
        return obj.doctors.count()

    total_doctors.short_description = _("Total Doctors")

    list_display = ("name", "total_doctors", "created_at")


@admin.register(Speciality)
class SpecialityAdmin(DevelopmentImportExportModelAdmin):
    search_fields = ("name", "department__name")
    list_filter = ("department", "updated_at", "created_at")
    list_display = (
        "name",
        "department",
        "appointment_charges",
        "treatment_charges",
        "updated_at",
    )


@admin.register(Doctor)
class DoctorAdmin(DevelopmentImportExportModelAdmin):
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
