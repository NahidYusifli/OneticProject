import django_filters
from ..models import Product
from django.db.models import Q
from services.choices import RATING
from base.models import Category
from products.models import Color
from services.choices import DISCOUNT_CHOICES



class ProductFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(label="Search", method="filter_search")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    brand = django_filters.CharFilter(field_name="brand", lookup_expr="icontains")
    rating = django_filters.ChoiceFilter(choices=RATING, label="Rating")
    color = django_filters.ModelMultipleChoiceFilter(field_name="color", label="Colors", queryset=Color.objects.all())
    size = django_filters.CharFilter(field_name="size", lookup_expr="icontains")
    category = django_filters.ModelChoiceFilter(field_name="category", queryset=Category.objects.all())
    discount_interest = django_filters.ChoiceFilter(field_name="discount_interest", choices=DISCOUNT_CHOICES)

    class Meta:
        model = Product
        fields = (
            "search",
            "name",
            "brand",
            "rating",
            "color",
            "size",
            "category",
            "discount_interest",
        )

    # def filter_queryset(self, queryset):
    #     queryset = super().filter_queryset(queryset)

    #     category_value = self.form.cleaned_data.pop("category")
    #     search = self.form.cleaned_data.pop("search")

    #     if category_value:

    #         queryset = queryset.filter(category__in=category_value.get_descendants(include_self=True))

    #     if search:
    #         queryset = queryset.filter(Q(name__icontains=search) | Q(category__name__icontains=search))

    #     return queryset.order_by("-created_at")

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(category__name__icontains=value))
