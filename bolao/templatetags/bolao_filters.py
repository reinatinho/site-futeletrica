from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Acessa um valor de dict por chave dinâmica no template."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def get_nested(dictionary, key):
    """Acessa um valor aninhado em dict."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def flag_url(selecao):
    """Retorna o path da bandeira PNG de uma seleção."""
    if hasattr(selecao, 'codigo'):
        return f"images/flags/{selecao.codigo.lower()}.png"
    return ""
