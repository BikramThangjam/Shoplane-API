from django.urls import path
from .views import *

urlpatterns = [
    path('user/signup/', SignUpView.as_view(), name='user-signup'),
    path('user/signin/', SignInView.as_view(), name='user-signup'),
    path('products/', ProductView.as_view(), name='get-all-products'),
    path('products/add/', ProductView.as_view(), name='add-product'),
    path("products/<int:product_id>/reviews/", ProductReview.as_view(), name="product-reviews"),
    path("products/<int:product_id>/reviews/add/", ProductReview.as_view(), name="product-add-review"),
    path("products/search/", ProductSearch.as_view(), name="search-products"),
    path("products/filter/by_price_range/", ProductsByPrice.as_view(), name="products-by-price-range"),
    path("products/filter/by_category_brand_active/", ProductsFilterByCategoryBrandActive.as_view(), name="filter-products-by-category-brand-active"),
    path("products/filter/by_name_desc/", ProductsByNameDesc.as_view(), name="filter-products-by-eiter-nameOrDescription"),
]