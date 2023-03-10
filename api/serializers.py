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
    address = AddressSerializer()

    class Meta:
        model = Contact
        fields = (
            'email',
            'address',
        )
    
    def create(self, validated_data):
        address = Address.objects.create(**validated_data.pop('address'))
        contact = Contact.objects.create(address=address, **validated_data)

        return contact


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
    contact = ContactSerializer()
    level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Producer
        # read_only_fields = ('level', 'debt') # don't work
        fields = (
            'name',
            'contact',
            'products',
            'provider',
            'created_at',
            'level',
            'debt',
        )
    
    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        address = Address.objects.create(**contact_data.pop('address'))
        contact = Contact.objects.create(address=address, **contact_data)

        level = 0
        provider = None
        if 'provider' in validated_data:
            provider = validated_data.pop('provider')
            level = provider.level + 1

        producer = Producer.objects.create(contact=contact,
                                           level=level,
                                           provider=provider,
                                           **validated_data,
                                           )

        return producer
