from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def uglify(field):
    i = 1
    result_ = ''
    for sym in field:
        if i % 2 == 0:
            result_ += sym.upper()
        else:
            result_ += sym.lower()
        i += 1
    return result_
