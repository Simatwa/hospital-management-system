from hospital_ms import settings
from import_export.admin import ImportExportModelAdmin
from import_export.forms import ImportForm, SelectableFieldsExportForm
from django.contrib import admin


class CustomImportExportModelAdmin(ImportExportModelAdmin):
    """ImportExportModelAdmin with `ImportForm` and `SelectableFieldsExportForm`"""

    import_class_form = ImportForm
    export_class_form = SelectableFieldsExportForm


DevelopmentImportExportModelAdmin = (
    CustomImportExportModelAdmin if settings.DEBUG == True else admin.ModelAdmin
)
"""ModelAdmin class for importing & exporting entries in `development environment`"""
