from rest_framework import serializers
from products.models import Product, Color, ProductImage, Size
from base.api.serializers import CategorySerializer
from django.db.models import Avg, F
from reviews.api.serializers import ReviewSerializer

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = (
            "id",
            "color"
        )

class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = (
            "id",
            "size"
        )



class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            "image",
        )


class ProductListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    color = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(read_only=True)
    totalprice = serializers.FloatField(read_only=True)
    discount_interest = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = (
            "name",
            "image",
            "brand",
            "category",
            "color",
            "description",
            "size",
            "price",
            "totalprice",
            "discount_interest",
            "quantity",
            "code",
            "slug",  
        )
        extra_kwargs = {field: {"read_only": True} for field in fields}

    def get_image(self, obj):
        return ProductImageSerializer(obj.productimage_set.first()).data
    
    def get_color(self, obj):
        return ColorSerializer(obj.color.all(), many=True).data
    
    def get_discount_interest(self, obj):
        discount_price = obj.price * (obj.discount_interest or 0) / 100
        discounted_price = obj.price - discount_price
        return round(float(discounted_price), 2) 


    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        repr_["product_color"] = ColorSerializer(instance.color).data
        if instance.category:
            repr_["category"] = CategorySerializer(instance.category).data
        return repr_
    

class ProductDetailSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    category = CategorySerializer()
    color = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "name",
            "image",
            "brand",
            "category",
            "color",
            "description",
            "size",
            "price",
            "totalprice",
            "discount_interest",
            "quantity",
            "code",
            "slug",
        )

    def get_rating(self, obj):
        rating = (obj.review_set.aggregate(rating_=Avg(F("rating")))["rating_"] or 0)
        return round(rating, 1)

    def get_images(self, obj):
        return ProductImageSerializer(obj.productimage_set.all(), many=True).data

    def get_size(self, obj):
        return SizeSerializer(obj.size.all(), many=True).data

    def get_color(self, obj):
        return ColorSerializer(obj.color.all(), many=True).data
    
    def to_representation(self, instance):
        repr_ = super().to_representation(instance)
        reviews = ReviewSerializer(instance.review_set.filter(parent__isnull=True), many=True).data
        repr_["reviews"] = reviews
        repr_["reviews count"] = instance.review_set.count()
        return repr_



            


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "name",
            "brand",
            "category",
            "color",
            "description",
            "size",
            "price",
            "discount_interest",
            "quantity",
            "code",
            "slug",
        )


