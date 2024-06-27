from rest_framework import serializers
from ..models import Category




class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "icon",
            "parent",
            "children"
        )

    def get_children(self, instance):
        qs = instance.get_children()
        return CategorySerializer(qs, many=True).data