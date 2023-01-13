from django.http import JsonResponse
from django.templatetags.static import static
import requests
import phonenumbers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.serializers import CharField, ListField

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


# def check_order_details(order, products):
#     all_fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']
#     incorect_field = [field for field in all_fields if not order.get(field)]
#     phone_parsed = phonenumbers.parse(order['phonenumber'])
#     errors = []
#     print(8)
#     if incorect_field:
#         print(1)
#         errors.append(
#             {f'{incorect_field}'.replace('[', '').replace(']', ''): 'Обязательное поле и не может быть пустым.'}
#         )
#     if not phonenumbers.is_valid_number(phone_parsed):
#         print(2)
#         errors.append({'phonenumber': 'Введен некорректный номер телефона.'})
#     print(order['products'])
#     try:
#         for product in order['products']:
#             if not products.filter(id=product['product']):
#                 print(4)
#                 errors.append({'products': f'Недопустимый первичный ключ {product["product"]}'})
#     finally:
#         if errors:
#             print(3)
#             print(errors)
#             raise ValidationError(errors)
class ApplicationSerializer(Serializer):
    products = ListField()
    firstname = CharField()
    lastname = CharField()
    phonenumber = CharField()
    address = CharField()

    def validate_products(self, value):
        if not value:
            raise ValidationError('Это поле не может быть пустым.')
        for product in value:
            if not Product.objects.filter(id=product['product']):
                raise ValidationError(f'Недопустимый первичный ключ {product.get("product")}')
        return value

    def validate_phonenumber(self, value):
        phonenumber = phonenumbers.parse(value)
        if not phonenumbers.is_valid_number(phonenumber):
            raise ValidationError('Введен некорректный номер телефона.')
        return value


@api_view(['POST'])
def register_order(request):
    serializer = ApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order = request.data
    products = Product.objects.all()
    # check_order_details(order, products)
    return Response(order)
