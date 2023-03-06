from django import template
from django.utils.safestring import mark_safe

register = template.Library()

## Code below is taken from https://cheat.readthedocs.io/en/latest/django/filter.html

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a param by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()


from urllib.parse import urlencode
from collections import OrderedDict


# Taken from https://stackoverflow.com/questions/19541978/django-listview-sorting-by-object-method-and-returning-python-list-as-queryset
@register.simple_tag
def url_replace(request, field, value, direction=''):
    dict_ = request.GET.copy()

    if field == 'order' and field in dict_.keys():          
      if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
        dict_[field] = value
      elif dict_[field].lstrip('-') == value:
        dict_[field] = "-" + value
      else:
        dict_[field] = direction + value
    else:
      dict_[field] = direction + value

    return urlencode(OrderedDict(sorted(dict_.items())))


@register.simple_tag
def order_sign(request, field):
    order = request.GET.get('order')
    if order == field or order=='-'+field:
        if order.startswith('-'):
            return mark_safe('&#x25b4;')
        else:
            return mark_safe('&#x25be;')
    return mark_safe('&nbsp;&nbsp;&nbsp;')


