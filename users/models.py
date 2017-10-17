# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict


def profile_picture_document_destination(instance, filename):
    return '/'.join(['documentos_del_usuario', str(instance.user.id), 'profile_' + filename])


# Create your models here.
class ERPUser(models.Model):
    ADMINISTRATOR = "AD"

    DIRECTIVO = "DI"

    ROLES_CHOICES = (
        (ADMINISTRATOR, 'Administrador General'),
        (DIRECTIVO, 'Directivo'),
    )

    user = models.OneToOneField(User)
    # rol = models.CharField(max_length=2, choices=ROLES_CHOICES, default=ADMINISTRATOR)
    # projects = models.ManyToManyField(through=AccessToProject,null=True,blank=True)

    profile_picture = models.FileField(blank=True, null=True, upload_to=profile_picture_document_destination,
                                       verbose_name="Foto de Perfil")

    class Meta:
        verbose_name_plural = 'Usuarios'

        # Director General
        #
        # Director  de Obras
        #
        # Vicepresidente Empresarial
        #
        # Jefe de Administración
        #
        # Presidente

        permissions = (
            ("is_general_director", "Es director general"),
            ("is_project_director", "Es director de obras"),
            ("is_vicepresident", "Es vicepresidente empresarial"),
            ("is_head_manager", "Es jefe de administración"),
            ("is_president", "Es presidente"),
        )

    def to_serializable_dict(self):
        ans = model_to_dict(self)
        ans['name'] = str(self.user.first_name)
        ans['lastname'] = str(self.user.last_name)
        return ans

    def __str__(self):
        return self.user.get_username()




        # Create your models here.


@receiver(post_save, sender=User, dispatch_uid='create_profile')
def create_profile(sender, instance, **kwargs):
    # Creating the sections for each saved project.
    id = instance.id
    users = ERPUser.objects.filter(user_id=id)
    if len(users) == 0:
        new_user = ERPUser()
        new_user.profile_picture = ''
        new_user.user_id = id
        new_user.save()
