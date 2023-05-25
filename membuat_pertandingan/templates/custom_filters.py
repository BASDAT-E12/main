from django import template

register = template.Library()

@register.filter
def split_teams(value):
    return value.split(' vs ')
