from django import template
import re

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if pattern == "/":
        if request.path == "/":
            return 'active' 
    elif re.search(pattern, request.path):
        return 'active'
    return ''