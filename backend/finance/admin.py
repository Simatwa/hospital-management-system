from django.contrib import admin

# Register your models here.
from finance.models import Account, UserAccount, Payment, ExtraFee
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from hospital_ms.utils.admin import DevelopmentImportExportModelAdmin


@admin.register(Account)
class AccountAdmin(DevelopmentImportExportModelAdmin):
    list_display = (
        "name",
        "paybill_number",
        "account_number",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "paybill_number")
    list_filter = ("is_active", "created_at", "updated_at")


@admin.register(UserAccount)
class UserAccountAdmin(DevelopmentImportExportModelAdmin):
    list_display = ("user", "balance", "created_at", "updated_at")
    search_fields = (
        "user",
        "balance",
    )
    list_filter = ("user", "updated_at", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False

    def has_change_permission(self, request, obj=...):
        return False


@admin.register(Payment)
class PaymentAdmin(DevelopmentImportExportModelAdmin):
    list_display = ("user", "amount", "method", "reference", "created_at")
    search_fields = ("user", "reference", "method")
    list_filter = ("user", "method", "created_at")
    ordering = ("-created_at",)
    list_editable = ()

    def has_change_permission(self, request, obj=...):
        return False

    def has_delete_permission(self, request, obj=...):
        return False


@admin.register(ExtraFee)
class ExtraFeeAdmin(DevelopmentImportExportModelAdmin):
    def total_treatments_charged(self, obj: ExtraFee) -> int:
        return obj.treatments.filter(created_at__date=timezone.now().date()).count()

    total_treatments_charged.short_description = _("Today's treatments")

    list_display = (
        "name",
        "amount",
        "total_treatments_charged",
        "updated_at",
        "created_at",
    )
    search_fields = ("name",)
    list_filter = ("updated_at", "created_at")
