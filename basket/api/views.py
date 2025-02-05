from ..models import Basket
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import BasketListSerializer, BasketCreateSerializer


class BasketListView(generics.ListAPIView):
    serializer_class = BasketListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        qs = Basket.objects.filter(user=self.request.user)
        return qs


class BasketCreateView(generics.CreateAPIView):
    serializer_class = BasketCreateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Basket.objects.all()

    def post(self, request, *args, **kwargs):
        obj, created = Basket.objects.get_or_create(
            user=request.user,
            product_id=request.data.get("product"),
            defaults={
                "size_id": request.data.get("size"),
                "color_id": request.data.get("color"),
                "quantity": request.data.get("quantity")
            }
        )
        if not created:
            serializer = self.serializer_class(instance=obj, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        serializer = self.serializer_class(obj).data
        return Response(serializer)


class BasketDeleteView(generics.DestroyAPIView):
    serializer_class = BasketCreateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)
