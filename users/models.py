# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.forms.models import model_to_dict


# Create your models here.
class ERPUser(models.Model):
    ADMINISTRATOR = "ADMIN"

    ROLES_CHOICES = (
        (ADMINISTRATOR, 'Administrador General'),
    )

    user = models.OneToOneField(User)
    rol = models.CharField(max_length=2, choices=ROLES_CHOICES, default=ADMINISTRATOR)


    class Meta:
        verbose_name_plural = 'Usuarios'

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['name'] = str(self.user.first_name)
        ans['lastname'] = str(self.user.last_name)
        return ans

    def __str__(self):
        return self.user.get_username()