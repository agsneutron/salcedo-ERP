# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.conf.urls import url
from decimal import *
# Register your models here.
from django.db.models import Sum
from django.db.models.query_utils import Q
from Accounting import views
from Accounting.models import *
from Accounting.forms import *
from Accounting.views import AccountDetailView

from Accounting.views import CommercialAllyDetailView, CommercialAllyContactDetailView
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

# Shared Catalogs Imports.
from HumanResources.models import AccessToDirection, Direction
from SharedCatalogs.models import GroupingCode, Account,ItemAccount


class AccountingAdminUtilities():
    @staticmethod
    def get_expense(obj):
        model_name = obj.__class__.__name__.lower()
        totaldebit = 0
        totalexpense = 0
        expenses = ExpenseDetail.objects.filter(Q(expense__id=obj.id))
        for expense in expenses:
            totaldebit += expense.debit
            totalexpense = obj.monto - Decimal(totaldebit)

        return '$ {:,}'.format(totalexpense)

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
    extra = 0
    formset = AccountingPolicyDetailInlineFormset


    fieldsets = (
        ("Detalle", {
            'fields': ('account', 'description', 'debit', 'credit')
        }),
    )


class ExpenseDetailInline(admin.TabularInline):
    model = ExpenseDetail
    extra = 0

    fieldsets = (
        ("Detalle", {
            'fields': ('internal_company', 'project', 'description', 'debit', 'deliveryto', 'registry_date')
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

    list_display = ('folio', 'internal_company', 'type_policy', 'fiscal_period', 'description','get_detail_column','get_change_column','get_delete_column')
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


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm
    inlines = (ExpenseDetailInline,)
    actions = None

    readonly_fields = []

    fieldsets = (
        ("", {
            'fields': (
                'internal_company', 'type_document', 'reference', 'total_ammount', 'monto', 'registry_date', 'description',)
        }),
    )

    list_display = ('reference', 'get_formated_monto', 'internal_company', 'description', 'registry_date', 'get_expense_column', 'get_detail_column', 'get_change_column')
    list_display_links = None
    search_fields = [
        'internal_company__name', 'type_document__name', 'reference', 'total_ammount', 'monto', 'registry_date', 'description',]

    def get_urls(self):
        urls = super(ExpenseAdmin, self).get_urls()
        my_urls = [
            url(r'^(?P<pk>\d+)/$', views.ExpenseAdminDetailView.as_view(), name='expense-detail'),
        ]

        return my_urls + urls

    def get_queryset(self, request):
        qs = super(ExpenseAdmin, self).get_queryset(request)
        user = request.user
        direction_ids = AccessToDirection.get_directions_for_user(user)
        ic_directions = Direction.objects.filter(id__in=direction_ids).values('internal_company_id')
        qs = qs.filter(internal_company_id__in=ic_directions)


        return qs

    def queryset(self, request):
        qs = super(ExpenseAdmin, self).queryset(request)
        # modify queryset here, eg. only user-assigned tasks
        qs.filter(assigned__exact=request.user)
        return qs

    def get_detail_column(self, obj):
        return AccountingAdminUtilities.get_detail_link_accounting(obj)

    def get_change_column(self, obj):
        return AccountingAdminUtilities.get_change_link_accounting(obj)

    def get_delete_column(self, obj):
        return AccountingAdminUtilities.get_delete_link_accounting(obj)

    def get_expense_column(self, obj):
        return AccountingAdminUtilities.get_expense(obj)

    def get_formated_monto(self, obj):
        return '$ {:,}'.format(obj.monto)

    get_detail_column.short_description = 'Detalle'
    get_detail_column.allow_tags = True

    get_change_column.short_description = 'Editar'
    get_change_column.allow_tags = True

    get_delete_column.short_description = 'Eliminar'
    get_delete_column.allow_tags = True

    get_expense_column.short_description = "Restante"
    get_expense_column.allow_tags = True

    get_formated_monto.short_description = "Monto"
    get_formated_monto.allow_tags = True

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ('folio',)
        return readonly_fields

    def save_model(self, request, obj, form, change):
        super(ExpenseAdmin, self).save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        response = super(ExpenseAdmin, self).changelist_view(request, extra_context)
        filtered_query_set = response.context_data["cl"].queryset

        expense_count = filtered_query_set.values('monto').aggregate(totalexpense=Sum('monto'))
        expensebydocument = filtered_query_set.values('id')

        print 'expensebydocument'
        print expensebydocument
        print expense_count

        amount_left = 0
        total_expense = 0
        for ebyd in expensebydocument:
            expenses = ExpenseDetail.objects.filter(Q(expense__id=ebyd['id']))
            for expense in expenses:
                total_expense += expense.debit

        if expense_count['totalexpense'] is not None:
            amount_left = expense_count['totalexpense'] - Decimal(total_expense)
        else:
            amount_left = 0

        extra_context = {
            'expense_count': expense_count['totalexpense'],
            'amount_left': amount_left,
            'total_expense': total_expense,
        }
        response.context_data.update(extra_context)

        return response


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
    # ordering = ('account_period', 'accounting_year', 'status')
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

    def save_model(self, request, obj, form, change):
        FiscalPeriodExist = FiscalPeriod.objects.filter(Q(accounting_year=obj.accounting_year),
                                                        Q(account_period=obj.account_period))

        if FiscalPeriodExist.count() == 0:
            super(FiscalPeriodAdmin, self).save_model(request, obj, form, change)
        else:
            messages.error(request, 'Este periodo fiscal ya existe.', fail_silently=True)


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


@admin.register(TypeDocument)
class TypeDocumentAdmin(admin.ModelAdmin):
    model = TypeDocument

    fieldsets = (
        ("Tipo de Documento", {
            'fields': (
                'name', 'description')
        }),
    )

    list_display = ('name', 'description')
    search_fields = ('name',)
    list_per_page = 25


@admin.register(CommercialAlly)
class CommercialAllyAdmin(admin.ModelAdmin):
    form = CommercialAllyForm

    fieldsets = (
        ("", {
            'fields': (
                'name', 'curp', 'rfc', 'phone_number', 'phone_number_2', 'email', 'cellphone_number', 'office_number',
                'extension_number',
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
        # print "title" + title
        # print "type" + type

        return super(CommercialAllyAdmin, self).add_view(request, form_url, extra_context=extra)

    def response_delete(self, request, obj_display, obj_id):

        redirect_page = request.redirect_delete # this is set on CommercialAllyAdmin.delete_model

        return HttpResponseRedirect("/accounting/" + request.redirect_delete)

    def delete_model(self, request, obj):
        request.redirect_delete = obj.get_delete_redirect_page()
        return super(CommercialAllyAdmin, self).delete_model(request, obj);

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
        # print "ca_type" + str(commercialally_type[0]['type'])
        # print "type" + type
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
        # redirect_url = "/admin/Accounting/commercialally/" + str(obj.id) + "/change/?type=" + request.GET.get('type')
        redirect_url = "/admin/Accounting/commercialally/" + str(obj.id)
        return HttpResponseRedirect(redirect_url)


@admin.register(ItemAccount)
class ItemAccountAdmin(admin.ModelAdmin):

    fieldsets = (
        ("Rubro de Cuenta", {
            'fields': (
                'key', 'name',)
        }),
    )

    list_display = ('key', 'name', 'get_change_column', 'get_delete_column')
    search_fields = ('name',)

    def get_change_column(self, obj):
        return AccountingAdminUtilities.get_change_link(obj)

    def get_delete_column(self, obj):
        return AccountingAdminUtilities.get_delete_link(obj)

    get_change_column.short_description = 'Editar'
    get_change_column.allow_tags = True

    get_delete_column.short_description = 'Eliminar'
    get_delete_column.allow_tags = True

@admin.register(GroupingCode)
class GroupingCode(admin.ModelAdmin):

    fieldsets = (
        ("Código Agrupador", {
            'fields': (
                'level', 'grouping_code','account_name')
        }),
    )

    list_display = ('level', 'grouping_code', 'account_name', 'get_change_column', 'get_delete_column')
    search_fields = ('account_name','grouping_code',)

    def get_change_column(self, obj):
        return AccountingAdminUtilities.get_change_link(obj)

    def get_delete_column(self, obj):
        return AccountingAdminUtilities.get_delete_link(obj)

    get_change_column.short_description = 'Editar'
    get_change_column.allow_tags = True

    get_delete_column.short_description = 'Eliminar'
    get_delete_column.allow_tags = True


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    form = AccountForm

    fieldsets = (
        ("Cuentas", {
            'fields': (
                'internal_company', 'number', 'name', 'status', 'nature_account', 'grouping_code',
                'subsidiary_account')
        }),
    )

    list_display = ('number', 'name', 'nature_account', 'get_detail_column', 'get_change_column', 'get_delete_column')

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
                'name', 'rfc', 'phone_number', 'secondary_number', 'email',
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

