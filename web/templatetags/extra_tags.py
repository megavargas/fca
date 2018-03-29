from django import template

register = template.Library()

@register.filter(name='default')
def default(value, arg):
    result = value if value else arg
    return result

@register.filter(name='limited')
def limited(value, arg):
    return value[:arg]

@register.filter(name='cleanone')
def cleanone(value):
    return value if value else ""
