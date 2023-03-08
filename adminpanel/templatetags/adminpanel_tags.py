from django.template import Library

register = Library()


@register.simple_tag
def get_verbose(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()



@register.simple_tag
def hasroom(instance):
    if hasattr(instance, 'room'):
        return True
    return False