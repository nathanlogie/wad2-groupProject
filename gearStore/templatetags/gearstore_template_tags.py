from django import template
from gearStore.models import Category

register = template.Library()

@register.inclusion_tag('gearStore/category_menu.html')
def get_category_list():
    return {'categories': Category.objects.all()}

@register.inclusion_tag('gearStore/base.html')
def get_categories():
    return {'categories': Category.objects.all()}