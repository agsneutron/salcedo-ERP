# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url


# Register your models here.
from django.db.models.query_utils import Q
from Accounting import views
from Accounting.models import *
from Accounting.forms import *
from Accounting.views import AccountDetailView


from Accounting.views import CommercialAllyDetailView, CommercialAllyContactDetailView
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Shared Catalogs Imports.
from SharedCatalogs.models import GroupingCode, Account


class AccountingAdminUtilities():
    @staticmethod
    def get_detail_link_accounting(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/Accounting/" + model_name + "/" + str(obj.id) + "/"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-eye color-default eliminar' > </i>"
        if model_name == "AccountingPolicy":
            button = "<i class ='fa fa-calendar-check-o color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_delete_link_accounting(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/Accounting/" + model_name + "/" + str(obj.id) + "/delete"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-trash-o color-danger eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_change_link_accounting(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/Accounting/" + model_name + "/" + str(obj.id) + "/change"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-pencil color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    # externas
    @staticmethod
    def get_detail_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/SharedCatalogs/" + model_name + "/" + str(obj.id) + "/"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-eye color-default eliminar' > </i>"
        if model_name == "Account":
            button = "<i class ='fa fa-calendar-check-o color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_delete_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/SharedCatalogs/" + model_name + "/" + str(obj.id) + "/delete"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-trash-o color-danger eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

    @staticmethod
    def get_change_link(obj):
        model_name = obj.__class__.__name__.lower()
        link = "/admin/SharedCatalogs/" + model_name + "/" + str(obj.id) + "/change"
        css = "btn btn-raised btn-default btn-xs"
        button = "<i class ='fa fa-pencil color-default eliminar' > </i>"

        return '<a href="' + link + '" class="' + css + '" >' + button + '</a>'

# Admin for the inline documents of the current education of an employee.
class AccountingPolicyDetailInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1

                    data = form.cleaned_data
                    debit = data['debit']
                    credit = data['credit']

                    if debit != 0 and credit != 0:
                        raise forms.ValidationError(
                            'No puede existir un valor de \'debe\' y \'haber\' para el mismo movimiento. ')

                    if debit == 0 and credit == 0:
                        raise forms.ValidationError(
                            'Tiene que definirse un valor de \'debe\' o \'haber\' para todos los movimientos.')

            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass


class AccountingPolicyDetailInline(admin.TabularInline):
    model = AccountingPolicyDetail
    extra = 1
    formset = AccountingPolicyDetailInlineFormset

    fieldsets = (
        ("Detalle", {
            'fields': ('account', 'description', 'debit', 'credit')
        }),
    )


@admin.register(AccountingPolicy)
class AccountingPolicyAdmin(admin.ModelAdmin):
    form = AccountingPolicyForm
    inlines = (AccountingPolicyDetailInline,)
    actions = None

    readonly_fields = []

    fieldsets = (
        ("Póliza", {
            'fields': (
            'internal_company','fiscal_period', 'type_policy', 'folio', 'registry_date', 'reference', 'description',)
        }),
    )

    list_display = ('folio', 'type_policy', 'fiscal_period', 'description','get_detail_column','get_change_column','get_delete_column')
    list_display_links = None

    def get_urls(self):
        urls = super(AccountingPolicyAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/$', views.AccountingPolicyDetailView.as_view(), name='contractor-detail'),
        ]

        return my_urls + urls

    def get_detail_column(self, obj):
        return AccountingAdminUtilities.get_detail_link_accounting(obj)

    def get_change_column(self, obj):
        return AccountingAdminUtilities.get_change_link_accounting(obj)

    def get_delete_column(self, obj):
        return AccountingAdminUtilities.get_delete_link_accounting(obj)

    get_detail_column.short_description = 'Detalle'
    get_detail_column.allow_tags = True

    get_change_column.short_description = 'Editar'
    get_change_column.allow_tags = True

    get_delete_column.short_description = 'Eliminar'
    get_delete_column.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('folio',)
        return readonly_fields

    def save_model(self, request, obj, form, change):

        super(AccountingPolicyAdmin, self).save_model(request, obj, form, change)



@admin.register(FiscalPeriod)
class FiscalPeriodAdmin(admin.ModelAdmin):
    form = FiscalPeriodForm

    fieldsets = (
        ("Periodo Fiscal", {
            'fields': (
                'accounting_year', 'account_period', 'status')
        }),
    )

    list_display = ('account_period', 'accounting_year', 'status')
    actions = None
    search_fields = ('account_period', 'accounting_year')
    #ordering = ('account_period', 'accounting_year', 'status')
    list_per_page = 25

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(FiscalPeriodAdmin, self).get_search_results(request, queryset, search_term)

        if search_term is not "":
            keywords = search_term.split(" ")

            years_array = None  # Set to none to control whether or not the user is searching for the year.
            months_numbers_array = []

            for word in keywords:
                # Finding the month number depending on the given word.
                result = FiscalPeriod.get_month_number_from_substring(word.lower())
                for number in result:
                    months_numbers_array.append(number)

                # Checking for the query in the years.
                try:
                    year = int(word)
                    if years_array is None:
                        # If None, but no exception ocurred, turn the variable into an array.
                        years_array = []
                        # Append the value.
                        years_array.append(year)
                    else:
                        # Append the value.
                        years_array.append(year)

                except ValueError:
                    pass

            # Filter for the months using the OR operator.
            queryset |= FiscalPeriod.objects.filter(Q(account_period__in=months_numbers_array))

            # Filter for the years using the AND operator.
            if years_array is not None:
                queryset &= FiscalPeriod.objects.filter(Q(accounting_year__in=years_array))

        return queryset, use_distinct


@admin.register(TypePolicy)
class TypePolicyAdmin(admin.ModelAdmin):
    form = TypePolicyForm

    fieldsets = (
        ("Tipo de Póliza", {
            'fields': (
                'name', 'balanced_accounts')
        }),
    )

    list_display = ('name', 'balanced_accounts')
    search_fields = ('name',)
    list_per_page = 25


@admin.register(CommercialAlly)
class CommercialAllyAdmin(admin.ModelAdmin):
    form = CommercialAllyForm

    fieldsets = (
        ("", {
            'fields': (
                'name', 'curp', 'rfc', 'phone_number', 'cellphone_number', 'office_number', 'extension_number',
                'street', 'outdoor_number',
                'indoor_number', 'colony', 'zip_code', 'country', 'state', 'town', 'accounting_account', 'bank',
                'bank_account_name', 'bank_account', 'employer_registration_number', 'tax_person_type', 'status',
                'services', 'type',)
        }),
    )

    list_display = ('name', 'rfc', 'phone_number', 'type', 'status')
    actions = None

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CommercialAllyAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        type = request.GET.get('type')
        title = ""
        extra['type'] = type
        if type == "0":
            title = "Proveedor"
        elif type == "1":
            title = "Acreedor"
        elif type == "2":
            title = "Tercero"

        extra['title'] = str(title)
        #print "title" + title
        #print "type" + type

        return super(CommercialAllyAdmin, self).add_view(request, form_url, extra_context=extra)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}

        type = request.GET.get('type')
        title = ""
        extra['type'] = type
        if type == "0":
            title = "Proveedor"
        elif type == "1":
            title = "Acreedor"
        elif type == "2":
            title = "Tercero"

        commercialally_type = CommercialAlly.objects.values('type').filter(pk=object_id)
        #print "ca_type" + str(commercialally_type[0]['type'])
        #print "type" + type
        if type != str(commercialally_type[0]['type']):
            raise PermissionDenied

        extra['type'] = type
        extra['title'] = str(title)
        return super(CommercialAllyAdmin, self).change_view(request, object_id, form_url, extra)

    def get_urls(self):
        urls = super(CommercialAllyAdmin, self).get_urls()
        my_urls = [url(r'^(?P<pk>\d+)/$', views.CommercialAllyDetailView.as_view(), name='contact-detail'),

        ]
        return my_urls + urls

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = "/admin/Accounting/commercialally/" + str(obj.id)
        return HttpResponseRedirect(redirect_url)

    def response_change(self, request, obj):
        #redirect_url = "/admin/Accounting/commercialally/" + str(obj.id) + "/change/?type=" + request.GET.get('type')
        redirect_url = "/admin/Accounting/commercialally/" + str(obj.id)
        return HttpResponseRedirect(redirect_url)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm

    fieldsets = (
        ("Cuentas", {
            'fields': (
            'internal_company','number','name','status','nature_account','item','grouping_code','subsidiary_account')
        }),
    )

    list_display = ('number', 'name', 'nature_account','get_detail_column','get_change_column','get_delete_column')

    def get_urls(self):
        urls = super(AccountAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/$', views.AccountDetailView.as_view(), name='account-detail'),
        ]

        return my_urls + urls

    def get_detail_column(self, obj):
        return AccountingAdminUtilities.get_detail_link(obj)

    def get_change_column(self, obj):
        return AccountingAdminUtilities.get_change_link(obj)

    def get_delete_column(self, obj):
        return AccountingAdminUtilities.get_delete_link(obj)

    get_detail_column.short_description = 'Ver'
    get_detail_column.allow_tags = True

    get_change_column.short_description = 'Editar'
    get_change_column.allow_tags = True

    get_delete_column.short_description = 'Eliminar'
    get_delete_column.allow_tags = True


@admin.register(CommercialAllyContact)
class CommercialAllyContactAdmin(admin.ModelAdmin):
    form = CommercialAllyContactForm

    fieldsets = (
        ("Contacto", {
            'fields': (
                'name', 'rfc', 'phone_number', 'secondary_number','email',
                'street', 'outdoor_number',
                'indoor_number', 'colony', 'zip_code', 'country', 'state', 'town',
                'is_legal_representative', 'commercialally')
        }),
    )

    # Method to override some characteristics of the form.
    def get_form(self, request, obj=None, **kwargs):
        ModelForm = super(CommercialAllyContactAdmin, self).get_form(request, obj, **kwargs)

        # Class to pass the request to the form.
        class ModelFormMetaClass(ModelForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request

                return ModelForm(*args, **kwargs)

        return ModelFormMetaClass

    # Adding extra context to the change view.
    def add_view(self, request, form_url='', extra_context=None):
        # Setting the extra variable to the set context or none instead.
        extra = extra_context or {}

        commercialally_id = request.GET.get('commercialally_id')

        extra['commercialally_id'] = commercialally_id

        return super(CommercialAllyContactAdmin, self).add_view(request, form_url, extra_context=extra)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra = extra_context or {}

        commercialally_id = request.GET.get('commercialally_id')

        ca_c = CommercialAllyContact.objects.values('commercialally').filter(pk=object_id)
        print commercialally_id
        print ca_c
        if commercialally_id != str(ca_c[0]['commercialally']):
            raise PermissionDenied

        return super(CommercialAllyContactAdmin, self).change_view(request, object_id, form_url, extra)

    def get_urls(self):
        urls = super(CommercialAllyContactAdmin, self).get_urls()
        my_urls = [url(r'^(?P<pk>\d+)/$', views.CommercialAllyContactDetailView.as_view(), name='contact-detail'),

                   ]
        return my_urls + urls

    def response_add(self, request, obj, post_url_continue=None):
        redirect_url = "/admin/Accounting/commercialallycontact/" + str(obj.id)
        return HttpResponseRedirect(redirect_url)

    def response_change(self, request, obj):
        # redirect_url = "/admin/Accounting/commercialally/" + str(obj.id) + "/change/?type=" + request.GET.get('type')
        redirect_url = "/admin/Accounting/commercialallycontact/" + str(obj.id)
        return HttpResponseRedirect(redirect_url)


admin.site.register(GroupingCode)
