from __future__ import unicode_literals

from django.db import models

# Create your models here.


# *********************************************************************
#                                CARGA                                *
# *********************************************************************
from django.forms import model_to_dict


class UsuarioFolio(models.Model):
    usuario = models.CharField(verbose_name="Nombre de Usuario", max_length=60, null=False, blank=False,
                               unique=True, db_index=True)
    folio = models.CharField(verbose_name="Folio", max_length=36, null=False, blank=False, unique=True);
    fecha = models.DateTimeField(verbose_name="Fecha de Subida", null=False, blank=False, auto_now=True);

    class Meta:
        ordering = ['fecha']
        verbose_name = "Registro de Carga"
        verbose_name_plural = "Registros de Carga"

    def __str__(self):  # __unicode__ on Python 2
        return self.folio

    def to_serilizable_dic(self):
        ans = model_to_dict(self)
        ans['id'] = str(self.id)
        ans['fecha'] = str(self.fecha)
        return ans
