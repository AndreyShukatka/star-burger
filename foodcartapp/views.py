from django.http import JsonResponse
from django.templatetags.static import static
import requests
import phonenumbers
from rest_framework.response import Response
from rest_framework import status

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
    products = Product.objects.all()
    all_fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']
    incorect_field = [field for field in all_fields if not request.data.get(field)]
    phone_parsed = phonenumbers.parse(request.data['phonenumber'])
    if incorect_field:
        return Response({f'{incorect_field}'.replace('[', '').replace(']', ''): 'Обязательное поле и не может быть пустым.'}, status=status.HTTP_404_NOT_FOUND)
    elif not phonenumbers.is_valid_number(phone_parsed):
        return Response({'phonenumber': 'Введен некорректный номер телефона.'}, status=status.HTTP_404_NOT_FOUND)
    for product in request.data['products']:
        if not products.filter(id=product['product']):
           return Response({'products': f'Недопустимый первичный ключ {product["product"]}'}, status=status.HTTP_404_NOT_FOUND)
    order = request.data
    return Response(order)
