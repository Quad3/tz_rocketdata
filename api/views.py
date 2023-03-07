from rest_framework import generics

from api.models import Producer
from .serializers import ProducerSerializer


class ProducerAPIView(generics.ListAPIView):
    queryset = Producer.objects.all().prefetch_related('products')\
        .select_related('contact', 'contact__address')
    serializer_class = ProducerSerializer
