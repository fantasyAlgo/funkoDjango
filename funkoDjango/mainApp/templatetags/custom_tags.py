# your_app/templatetags/custom_tags.py
# mainApp/templatetags/custom_tags.py
from django import template

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
