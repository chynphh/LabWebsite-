from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
	return dictionary[key]

@register.filter
def get_class_name(value):
    return value.__class__.__name__
