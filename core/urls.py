from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/accounts/", include("accounts.api.urls")),
    path("api/products/", include("products.api.urls")),
    path("api/reviews/", include("reviews.api.urls")),
    path("api/orders/", include("orders.api.urls")),
    path("api/address/", include("address.api.urls")),
    path("api/basket/", include("basket.api.urls")),
    path("api/shipping/", include("shipping.api.urls")),

]

admin.site.site_title = 'Onetic Ecommerce'
admin.site.site_header = 'Onetic Administration'
admin.site.index_title = 'Welcome To Onetic Admin Portal'



urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 

# SWAGGER CONFIG
 
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Onetic API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
   path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]