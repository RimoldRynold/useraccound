from django import template
register = template.Library()

@register.filter(name='username')
def username(name):
    if name.first_name:
        return name.first_name
    else:
        return str(name)
    
@register.filter(name='state')
def state(val,bal):
    if float(val) >= float(bal):
        return True