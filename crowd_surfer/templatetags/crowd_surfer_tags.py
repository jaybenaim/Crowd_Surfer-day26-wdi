from django import template
register = template.Library()

@register.filter
def keyvalue(dict, key):    
    return dict[key]

def subtract(value, arg):
    return value - arg