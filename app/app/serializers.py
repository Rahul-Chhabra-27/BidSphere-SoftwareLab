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
            'category',
            'city',
            'pincode',
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

from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email", "full_name"]

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already registered"})
        return attrs

    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        first_name, *last_parts = full_name.split(" ", 1)
        last_name = last_parts[0] if last_parts else ""

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=first_name,
            last_name=last_name
        )
        return user