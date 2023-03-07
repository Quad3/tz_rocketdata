from rest_framework import serializers

from api.models import Producer, Product, Contact, Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'country',
            'city',
            'street',
            'house_number',
        )


class ContactSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = (
            'email',
            'address',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'model',
            'release_date',
        )


class ProducerSerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Producer
        fields = (
            'name',
            'contact',
            'products',
            'provider',
            'level',
            'debt',
            'created_at',
        )
