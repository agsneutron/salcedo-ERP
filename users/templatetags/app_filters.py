__author__ = 'ariaocho'

from django import template
from django import forms
from django.contrib.humanize.templatetags.humanize import intcomma
import locale

from django.utils.safestring import mark_safe

import json

import re
from decimal import Decimal

from django import template
from django.conf import settings
from django.template import defaultfilters
from django.utils.formats import number_format
from django.utils.safestring import mark_safe
from django.utils.timezone import is_aware, utc
from django.utils.translation import gettext as _, ngettext, pgettext

register = template.Library()


@register.filter(name='add_attributes')
def add_attributes(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v
    return field.as_widget(attrs=attrs)


@register.filter(name='add_desc')
def add_desc(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if '=' not in d:
            attrs['data-filename-placement'] = d
        else:
            t, v = d.split('=')
            attrs[t] = v
    return field.as_widget(attrs=attrs)


@register.filter(name='is_file')
def is_file(field):
    return isinstance(field.field.widget, forms.ClearableFileInput)


@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='formatoNumero')
def currency(field):
    if field == '-' or field == "None": field = 0

    print 'The field is: ' + str(field)
    return locale.currency(field, grouping=True)
    # moneda = round(float(field), 2)
    # return "$%s%s" % (intcomma(int(moneda)), ("%0.2f" % moneda)[-3:])
    # return field


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.filter(is_safe=True)
def intcomma(value, use_l10n=True):
    """
    Convert an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    if settings.USE_L10N and use_l10n:
        try:
            if not isinstance(value, (float, Decimal)):
                value = int(value)
        except (TypeError, ValueError):
            return intcomma(value, False)
        else:
            return number_format(value, force_grouping=True)
    orig = str(value)

    new = re.sub(r"^(-?\d+)(\d{3})", r'\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intcomma(new, use_l10n)
