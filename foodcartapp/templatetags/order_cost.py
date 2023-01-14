from django import template

register = template.Library()


@register.filter('get_order_param')
def get_order_param(orders_param, order):
    if order:
        return orders_param.get(order)
