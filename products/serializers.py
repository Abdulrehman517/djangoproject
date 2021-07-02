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
    prod_var = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['title','tags', 'handle','body','prod_var']


    def create(self, validated_data):
        products_variant_data = validated_data.pop('prod_var')
        variant = Variant.objects.create(**products_variant_data)
        product = Product.objects.create(variants=variant, **validated_data)
        return product


    def update(self, instance, validated_data):
        instance.title=validated_data.get('title', instance.title)
        instance.tags=validated_data.get('tags', instance.tags)
        instance.handle=validated_data.get('handle', instance.handle)
        instance.body=validated_data.get('body', instance.body)

        products_variants = validated_data.pop('prod_var')
        instance.variants.title = products_variants.get('title', instance.variants.title)
        instance.variants.sku = products_variants.get('sku', instance.variants.sku)
        instance.variants.barcode = products_variants.get('barcode', instance.variants.barcode)
        instance.variants.quantity = products_variants.get('quantity', instance.variants.quantity)
        instance.save()
        return instance

