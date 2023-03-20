from django.urls import path

from .views import (ProducerAPIView,
                    ProducerAboveAverageDebtAPIView,
                    ProducerInstanceAPIView,
                    ProductAPIView,
                    ProductInstanceAPIView,
                    CustomAuthToken,
                    )


urlpatterns = [
    path('producer', ProducerAPIView.as_view()),
    path('producer-debt-above-average', ProducerAboveAverageDebtAPIView.as_view()),
    path('producer/<int:pk>', ProducerInstanceAPIView.as_view()),
    path('product', ProductAPIView.as_view()),
    path('product/<int:pk>', ProductInstanceAPIView.as_view()),
    path('api-token-auth', CustomAuthToken.as_view()),
]
