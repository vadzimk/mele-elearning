# this is a custom template filter
# which type of object each of the item object is: Text, Video, Image, File
# need the model name but cannot access _meta attribute in the template bc it starts with _


from django import template

register = template.Library()
@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
