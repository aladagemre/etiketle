# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag()
def check_annotation_status(annotations_dict, user, post):
    # <td>{% check_annotation_status annotations_dict request.user object %}</td>
    print("checking status")
    if user.pk in annotations_dict[post.pk]:
        return "✅"
    return ""


@register.filter(name="dict_key")
def dict_key(d, k):
    """Returns the given key from a dictionary."""
    """
    {% for user in dataset.project.members.all %}
        <td>{% if user.pk in annotation_dict.items|dict_key:object.pk %}YES{% endif %}</td>
      {% endfor %}
    """
    return d[k]
