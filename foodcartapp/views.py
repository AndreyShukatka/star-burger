from django.http import JsonResponse
from django.templatetags.static import static
import requests
from rest_framework.response import Response

from rest_framework.decorators import api_view
from .models import Product, Order


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })

@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return Response(dumped_products)


@api_view(['POST'])
def register_order(request):
    # TODO это лишь заглушка
    try:
        products = request.data['products']
        if not products:
            return Response({'products': 'Это поле не может быть пустым.'})
    except KeyError:
        return Response({'products': 'Обязательное поле.'})
    if not isinstance(products, list) or len(products):
        return Response({'products': 'Ожидался list со значениями, но был получен "str".'})
    else:
        order = request.data
        print(order)
    return Response(order)
