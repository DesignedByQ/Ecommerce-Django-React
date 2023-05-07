from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("welcome/", views.index, name="homepage"),
    #The ProductList view handles GET requests for a list of all Product objects and POST requests to create a new Product object.
    path('products/', views.get_products_and_create_product, name='get-products-and-create-product'),
    #This view handles GET, PUT, and DELETE requests for a single Product object, specified by its primary key pk.
    path('products/<int:pk>/', views.product_by_id, name='product-by-id'),
    #This view handles GET requests for a list of all Tag objects and POST requests to create a new Tag object.
    path('tags/', views.get_tags_and_create_tag, name='get-tags-and-create-tag'),
    #This view handles GET, PUT, and DELETE requests for a single Tag object, specified by its primary key pk.
    #path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)


