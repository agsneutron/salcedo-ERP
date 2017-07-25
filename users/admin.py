# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from users.models import ERPUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



class ERPUserAdmin(admin.StackedInline):
    model = ERPUser
    extra = 1


# Overriding the User Admin view.
class UsuarioAdmin(UserAdmin):
    inlines = (ERPUserAdmin,)
    list_per_page = 8
    list_display = ('username', 'first_name', 'last_name', 'email', 'get_rol',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('AuthInfo', {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        ('AuthInfo', {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active',)}),
    )


    def get_rol(self, obj):
        return obj.erpuser.rol

    get_rol.short_description = "Rol de Usuario"

    #  Overrriding the 'save' method so the user can have the 'staff' status and access the system.
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        print "Obj is:"
        print obj.erpuser
        obj.save()

        super(UsuarioAdmin, self).save_model(request, obj, form, change)


# Registering activities.
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)
