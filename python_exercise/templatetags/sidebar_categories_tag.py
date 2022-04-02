from django import template
from python_exercise.models import *

register = template.Library()


@register.inclusion_tag('python_exercise/sidebar_categories_tag.html', takes_context=True)
def sidebar_categories_tag(context):
    context['tags'] = Tag.objects.all()
    return context
