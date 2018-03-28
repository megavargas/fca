from django import template

register = template.Library()

@register.filter(name='default')
def default(value, arg):
    result = value if value else arg
    return result

@register.filter(name='limited')
def limited(value, arg):
    return value[:arg]

@register.filter(name='chart')
def chart(opportunity, arg):
    return str([record.value for record in opportunity.history.all()][arg:])