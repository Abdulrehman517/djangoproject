from django.db import models
from django.db.models import fields
# from rest_framework.fields import ReadOnlyField
from rest_framework.exceptions import ValidationError

from .models import Product, Variant
from rest_framework import serializers


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, source="prod_var", read_only=True)

    class Meta:
        model = Product
        fields = ['title','tags', 'handle','body','variants']


    # def create(self, validated_data):
    #     variants_data = validated_data.pop('variants')
    #     product = Product.objects.create(**validated_data)
    #     for variant_data in variants_data:
    #         Variant.objects.create(product=product, **variant_data)
    #     return product

