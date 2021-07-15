from django.contrib import admin
from django.urls import path
from products import views
from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/',views.ProductList.as_view()),
    path('products/<int:pk>/',views.ProductDetail.as_view()),
    # path('products/variants/',views.VariantList.as_view()),
    # path('products/variants/<int:pk>', views.VariantDetail.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)
