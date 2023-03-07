from django.urls import path

from .views import ProducerAPIView


urlpatterns = [
    path('producer', ProducerAPIView.as_view()),
]
