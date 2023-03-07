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
