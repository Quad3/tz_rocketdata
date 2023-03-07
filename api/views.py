from django.db.models import Avg
from rest_framework import generics

from api.models import Producer
from .serializers import ProducerSerializer


class ProducerAPIView(generics.ListAPIView):
    serializer_class = ProducerSerializer

    def get_queryset(self):
        queryset = Producer.objects.prefetch_related('products')\
            .select_related('contact', 'contact__address')
        country = self.request.query_params.get('country')
        if country is not None:
            queryset = Producer.objects.filter(contact__address__country=country).prefetch_related('products')\
                .select_related('contact', 'contact__address')

        return queryset


class ProducerAboveAverageDebtAPIView(generics.ListAPIView):
    serializer_class = ProducerSerializer

    def get_queryset(self):
        avg = Producer.objects.aggregate(Avg('debt'))['debt__avg']
        queryset = Producer.objects.filter(debt__gte=avg).prefetch_related('products')\
            .select_related('contact', 'contact__address')

        return queryset
