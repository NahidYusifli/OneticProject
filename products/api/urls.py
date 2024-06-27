from django.urls import path
from products.api import views

app_name = "products-api"

urlpatterns = [

    ############Class Based##############
    path("list/", views.ProductListView.as_view(), name="list"),
    path("create/", views.ProductCreateView.as_view(), name="create"),
    path("detail/<uuid>/", views.ProductDetailView.as_view(), name="detail"),
    path("update/<id>/", views.ProductUpdateView.as_view(), name="update"),
    path("delete/<id>/", views.ProductDeleteView.as_view(), name="delete"),

]