from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            {"message": "Category created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
class ProductView(APIView):

    def get(self, request):
        products = Product.objects.all()

        if not products.exists():
            return Response(
                {"message": "No products found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = ProductSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(
            {"message": "Product added successfully", "product": serializer.data},
            status=status.HTTP_201_CREATED
        )
class ProductsByCategoryView(APIView):

    def get(self, request, category_name):
        category = get_object_or_404(Category, name__iexact=category_name)

        products = Product.objects.filter(category=category)

        if not products.exists():
            return Response(
                {"message": "No products found in this category."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

class ProductDetailView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)

        if not serializer.is_valid():
            return Response(
                {"message": "Invalid data", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {"message": "Product updated successfully", "product": serializer.data},
            status=status.HTTP_200_OK
        )


    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(
            {"message": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
