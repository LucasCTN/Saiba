from django import template

register = template.Library()

@register.filter(name = 'should_hide_chain')
def should_hide_chain(value, args):
    terms = args.split(",")
    current_comment_id = terms[0]
    chain_testing = terms[1]

    if current_comment_id == chain_testing:
        return ""
    else:
        return str(value)