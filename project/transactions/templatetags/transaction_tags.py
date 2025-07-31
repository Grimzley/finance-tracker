from django import template
from transactions.utils import get_category_icon, get_category_color, get_category_description

register = template.Library()

@register.filter
def category_icon(category):
    return get_category_icon(category)

@register.filter
def category_color(category):
    return get_category_color(category)

@register.filter
def category_description(category):
    return get_category_description(category)
