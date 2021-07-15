from rest_framework.response import Response
from .serializers import ProductSerializer, VariantSerializer
from .models import Product, Variant
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from products.models import Product


class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # ser = ProductSerializer(data=request.data, instance=serializer.validated_data['product'])
        # ser.is_valid(raise_exception=True)
        # ser.save()
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class VariantList(APIView):
#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise Http404
#
#     def get(self, request, format=None):
#         variant = Variant.objects.all()
#         serializer = VariantSerializer(variant, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = VariantSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response (serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class VariantDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk):
#         variant = self.get_object(pk)
#         serializer = VariantSerializer(variant)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         variant = self.get_object(pk)
#         variant.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
