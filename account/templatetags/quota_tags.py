from django import template

register = template.Library()

@register.inclusion_tag('account/snippets/quota_progress.html')
def quota_progress(user, quota_type):
    try:
        return getattr(user, "{}_quota".format(quota_type))()
    except AttributeError:
        return {
            "limit": 0,
            "used": 0,
            "perc": 100,
        }