from django.urls import path

from .views import ProducerAPIView, ProducerAboveAverageDebtAPIView


urlpatterns = [
    path('producer', ProducerAPIView.as_view()),
    path('producer-debt-above-average', ProducerAboveAverageDebtAPIView.as_view()),
]
