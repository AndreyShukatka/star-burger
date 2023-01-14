from foodcartapp.models import Order
from foodcartapp.serializers import OrderSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

snippet = Order(products=[{"product": 1, "quantity": 1}], firstname="Василий", lastname="Васильевич", phonenumber="+79123456789", address="Лондон")
snippet.save()

serializer = OrderSerializer(snippet)
print(serializer.data)
