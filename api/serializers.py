from rest_framework import serializers
from django.contrib.auth import authenticate

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


class ProductInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'model',
            'release_date',
            'producer_set',
        )


class ProducerSerializerMixin(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True, many=True)
    contact = ContactSerializer()
    level = serializers.IntegerField(read_only=True)

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


class ProducerListSerializer(ProducerSerializerMixin):

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


class ProducerInstanceSerializer(ProducerSerializerMixin):
    debt = serializers.FloatField(read_only=True)

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', {})
        address_data = contact_data.pop('address', {})
        
        for attr, value in address_data.items():
            setattr(instance.contact.address, attr, value)
        
        for attr, value in contact_data.items():
            setattr(instance.contact, attr, value)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if instance.provider is not None:
            instance.level = instance.provider.level + 1
        else:
            instance.level = 0
        instance.contact.address.save()
        instance.contact.save()
        instance.save()

        return instance


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label="Token",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
