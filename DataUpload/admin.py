from django.contrib import admin

# Register your models here.
from DataUpload.models import UsuarioFolio

class UsuarioFolioAdmin(admin.ModelAdmin):
    list_display = ('folio', 'usuario', 'fecha')


admin.site.register(UsuarioFolio, UsuarioFolioAdmin);