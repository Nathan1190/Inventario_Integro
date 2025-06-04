from django import template

register = template.Library()

@register.filter(name='has_pantalla')
def has_pantalla(user, identificador):
    """Return True if the user has an active pantalla with this identificador."""
    if not hasattr(user, 'is_authenticated') or not user.is_authenticated:
        return False
    return user.roles.filter(pantallas__identificador=identificador).exists()