from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """Divide uma string usando o delimitador especificado"""
    return value.split(delimiter)