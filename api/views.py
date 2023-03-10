from django.db.models import Avg
from rest_framework import generics

from api.models import Producer
from .serializers import ProducerSerializer


class ProducerAPIView(generics.ListCreateAPIView):
    serializer_class = ProducerSerializer

    def get_queryset(self):
        queryset = Producer.objects.prefetch_related('products')\
            .select_related('contact', 'contact__address')
        country = self.request.query_params.get('country')
        product_id = self.request.query_params.get('product_id')
        if country is not None:
            queryset = queryset.filter(contact__address__country=country)
        if product_id is not None:
            try:
                product_id = int(product_id)
            except ValueError:
                raise ValueError(f'product_id - Invalid number: {product_id}')
            queryset = queryset.filter(products__id=product_id)

        return queryset


class ProducerAboveAverageDebtAPIView(generics.ListAPIView):
    serializer_class = ProducerSerializer

    def get_queryset(self):
        avg = Producer.objects.aggregate(Avg('debt'))['debt__avg']
        queryset = Producer.objects.filter(debt__gte=avg).prefetch_related('products')\
            .select_related('contact', 'contact__address')

        return queryset
