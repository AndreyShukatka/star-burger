from django import template

register = template.Library()


@register.filter('get_order_cost')
def get_order_cost(orders_cost, order):
    if order:
        return orders_cost.get(order, 0)
