# your_app/templatetags/custom_tags.py
# mainApp/templatetags/custom_tags.py
from django import template
from django.utils.http import urlencode

register = template.Library()

@register.filter
def range(value):
    """Returns a range from 0 to value (exclusive)"""
    i = 0
    lst = []
    while i < value:
        lst.append(i)
        i += 1
    return lst

@register.filter
def index(sequence, position):
    """Accesses a list item by index"""
    try:
        return sequence[int(position)]
    except:
        return None

@register.filter
def increment(value):
    return value+1

@register.filter
def decrement(value):
    return value-1

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Template tag that replaces or adds GET parameters while preserving existing ones
    
    Usage:
    {% url_replace it=2 %}  # Changes it=2 while preserving other params
    """
    query = context['request'].GET.dict()
    query.update(kwargs)
    return '?' + urlencode(query)


