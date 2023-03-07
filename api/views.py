from rest_framework import generics

from api.models import Producer
from .serializers import ProducerSerializer


class ProducerAPIView(generics.ListAPIView):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
