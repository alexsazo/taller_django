from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def select_values(dic, keys):
    keys = keys.split(',')
    values = []
    for key in keys:
        values.append(dic.get(key))
    return values

@register.simple_tag(takes_context=True)
def display_block(context, *args):
    is_active = False
    for url in args:
        try:
            url = reverse(url)
        except NoReverseMatch:
            pass
        path = context['request'].path
        if url == path:
            is_active=True
    if is_active:
        return "display: block;"
    else:
        return 'display: none;'

