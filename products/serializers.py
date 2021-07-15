from .models import Product, Variant
from rest_framework import serializers
#
# class ProductIdRequiredSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#
#     def validate(self, attrs):
#         id = attrs.get('id')
#         product = Product.objects.filter(id=id).first()
#         if product is None:
#             print("gvg")
#         attrs['product'] = product
#         return attrs


class VariantSerializer(serializers.ModelSerializer):
    # type = serializers.CharField(required=False)

    class Meta:
        model = Variant
        fields = '__all__'
# This is for field level validation for variant model

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title of Variant is too short")
        return value


class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'tags', 'handle', 'body', 'variants']
# Field level validation for product title field

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title of Product is too short")
        return value

# Object level validation
    def validate(self, data):
        if data['title'] == data['body']:
            raise serializers.ValidationError("Title and Body of product should be different")
        return data

    def create(self, validated_data):
        variant_data = validated_data.pop('variants')
        new_product = Product.objects.create(**validated_data)
        for i in variant_data:
            Variant.objects.create(**i, product=new_product)
        return new_product

    def update(self, instance, validated_data):
        variant_list = validated_data.pop('variants')

        instance.title = validated_data.get('title', instance.title)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.hanlde = validated_data.get('handle', instance.handle)
        instance.body = validated_data.get('body', instance.body)
        instance.save()

        variants_with_same_product_instance = Variant.objects.filter(product=instance.pk).values_list('id', flat=True)

        variants_id_pool = []

        for variant in variant_list:
            if "id" in variant.keys():
                if Variant.objects.filter(id=variant['id'].exists()):
                    variant_instance = Variant.objects.get(id=variant['id'])
                    variant_instance.title = variant.get('title', variant_instance.title)
                    variant_instance.sku = variant.get('sku', variant_instance.sku)
                    variant_instance.barcode = variant.get('barcode', variant_instance.barcode)
                    variant_instance.quantity = variant.get('quantity', variant_instance.quantity)
                    variant_instance.save()
                    variants_id_pool.append(variant_instance.id)
                else:
                    continue
            else:
                variants_instance = Variant.objects.create(product=instance, **variant)
                variants_id_pool.append(variants_instance.id)
        for variant_id in variants_with_same_product_instance:
            if variant_id not in variants_id_pool:
                Variant.objects.filter(pk=variant_id).delete()

        return instance


   #
    # def update(self, instance, validated_data):
    #     variants = validated_data.pop('prod_var')
    #     for variant in variants:
    #         type = variant.pop('type', None)
    #         product_id = variant.pop('product_id', None)
    #         if type is not None:
    #             if type == "add":
    #                 Variant.objects.create(**variant)
    #             if type == "update":
    #                 Variant.objects.filter(product_id=product_id).update(**variant)
    #             if type == "remove":
    #                 Variant.objects.filter(product_id=product_id).delete()
    #
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.tags = validated_data.get('tags', instance.tags)
    #     instance.handle = validated_data.get('handle', instance.handle)
    #     instance.body = validated_data.get('body', instance.body)
    #     instance.save()
    #     return instance


        # products_variants = validated_data.pop('prod_var')
        # instance.variants.title = products_variants.set('title', instance.variants.title)
        # instance.variants.sku = products_variants.get('sku', instance.variants.sku)
        # instance.variants.barcode = products_variants.get('barcode', instance.variants.barcode)
        # instance.variants.quantity = products_variants.get('quantity', instance.variants.quantity)