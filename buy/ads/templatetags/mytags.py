from django import template

register = template.Library()

@register.filter
def cutlen(value, length):
    return value[:length]