
from rest_framework import generics
from .serializers import ProductListSerializer, ProductCreateSerializer, ColorSerializer
from products.models import Product, Color
from rest_framework.response import Response



class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductListSerializer
    
    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "uuid"

    def get_object(self, *args, **kwargs):
        uuid = self.kwargs.get("uuid")
        return Product.objects.get(id=uuid)
    
    def get(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "id"

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=obj)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(data=request.data, instance=obj, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = "id"

    

class ColorListView(generics.CreateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    


    

