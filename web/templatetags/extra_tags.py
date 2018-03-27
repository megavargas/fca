from django import template

register = template.Library()

@register.filter(name='default')
def default(value, arg):
    result = value if value else arg
    return result

@register.filter(name='limited')
def default(value, arg):
    return value[:arg]