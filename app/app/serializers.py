from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'location',
            'category',
            'category_name',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        category_name = validated_data.pop("category_name")
        category, _ = Category.objects.get_or_create(
            name__iexact=category_name, defaults={"name": category_name}
        )
        validated_data["category"] = category
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if "category_name" in validated_data:
            category_name = validated_data.pop("category_name")
            category, _ = Category.objects.get_or_create(
                name__iexact=category_name, defaults={"name": category_name}
            )
            instance.category = category

        return super().update(instance, validated_data)
