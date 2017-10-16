# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib import admin
from users.models import ERPUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from users import views
from users.views import UsersListView


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
        ('Permissions', {'fields': ('is_active',)}),

    )
    add_fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('AuthInfo', {'fields': ('username', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_active',)}),
    )

    def get_rol(self, obj):
        return obj.erpuser.rol

    get_rol.short_description = "Rol de Usuario"

    def get_urls(self):
        urls = super(UsuarioAdmin, self).get_urls()
        my_urls = [
            url(r'^$',
                self.admin_site.admin_view(UsersListView.as_view()), name='users-list-view'),
            url(r'^(?P<pk>\d+)/$', views.UsersDetailView.as_view(), name='users-detail'),

        ]
        return my_urls + urls

    #  Overrriding the 'save' method so the user can have the 'staff' status and access the system.
    def save_model(self, request, obj, form, change):
        obj.is_staff = True

        obj.save()

        super(UsuarioAdmin, self).save_model(request, obj, form, change)


# Registering activities.
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)
