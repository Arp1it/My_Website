from django import template

register = template.Library()

@register.filter(name='getvalu')
def getvalu(dict, key):
    return dict.get(key)