from django.db.models import Avg
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken

from api.models import Producer, Product
from .serializers import (ProducerListSerializer,
                          ProducerInstanceSerializer,
                          ProductInstanceSerializer,
                          CustomAuthTokenSerializer,
                          )
from .permission_utils import IsEmployee


class ProducerAPIView(generics.ListCreateAPIView):
    serializer_class = ProducerListSerializer

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
    serializer_class = ProducerListSerializer

    def get_queryset(self):
        avg = Producer.objects.aggregate(Avg('debt'))['debt__avg']
        queryset = Producer.objects.filter(debt__gte=avg).prefetch_related('products')\
            .select_related('contact', 'contact__address')

        return queryset


class ProducerInstanceAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProducerInstanceSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        queryset = Producer.objects.prefetch_related('products')\
            .select_related('contact', 'contact__address')
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance.contact.address)
        self.perform_destroy(instance.contact)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAPIView(generics.ListCreateAPIView):
    serializer_class = ProductInstanceSerializer
    queryset = Product.objects.prefetch_related('producer_set')


class ProductInstanceAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductInstanceSerializer
    queryset = Product.objects.prefetch_related('producer_set')


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
