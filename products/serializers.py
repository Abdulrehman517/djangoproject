from django.db import models
from django.db.models import fields
# from rest_framework.fields import ReadOnlyField
from rest_framework.exceptions import ValidationError

from .models import Product, Variant
from rest_framework import serializers


class VariantSerializer(serializers.ModelSerializer):
    type= serializers.CharField(required=False)
    class Meta:
        model = Variant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    prod_var = VariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'tags', 'handle', 'body', 'prod_var']
        # fields = '__all__'

    def create(self, validated_data):
        products_variant_data = validated_data.pop('prod_var')
        product = Product.objects.create(**validated_data)
        Variant.objects.create(product=product, **products_variant_data)
        return product

    def update(self, instance, validated_data):
        varients = validated_data.pop('prod_var')
        for varient in varients:
            type = varient.pop('type', None)
            product_id = varient.pop('product_id', None)
            if type is not None:
                if type == "add":
                    Variant.objects.create(**varient)
                if type == "update":
                    Variant.objects.filter(product_id=product_id).update(**varient)
                if type == "remove":
                    Variant.objects.filter(product_id=product_id).delete()

        instance.title = validated_data.get('title', instance.title)
        instance.title = validated_data.get('title', instance.title)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.handle = validated_data.get('handle', instance.handle)
        instance.body = validated_data.get('body', instance.body)

        # products_variants = validated_data.pop('prod_var')
        # instance.variants.title = products_variants.set('title', instance.variants.title)
        # instance.variants.sku = products_variants.get('sku', instance.variants.sku)
        # instance.variants.barcode = products_variants.get('barcode', instance.variants.barcode)
        # instance.variants.quantity = products_variants.get('quantity', instance.variants.quantity)
        instance.save()
        return instance




class ProductIdRequiredSerializer(serializers.Serializer):
    id= serializers.IntegerField()

    def validate(self, attrs):
        id = attrs.get('id')
        product = Product.objects.filter(id = id).first()
        if product is None:
            print("gvg")
        attrs['product'] = product
        return attrs

