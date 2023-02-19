
from django import template
register = template.Library()

@register.filter
def index(object_list, index):
    return object_list[index]