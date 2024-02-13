from django.conf import settings
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("",views.home),
     path("about/",views.about,name="about"),
     path("contact/",views.contact,name="contact"),
    path("category/<slug:val>",views.CategoryView.as_view(),name="category"),
    path("category-title/<val>",views.CategoryTitle.as_view(),name="category-title"),
    
    path('add-to-cart/',views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    # path('orders/',views.orders,name='orders'),
    
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.address, name="address"),
    path("updateAddress/<int:pk>", views.updateAddress.as_view(), name="updateAddress"),

path("product-detail/<int:pk>",views.ProductDetail.as_view(),name="product-detail"),
path("product_list",views.product_list,name="product_list"),

#login authentication
path('registration/',views.CustomerRegistrationView.as_view(),name='customerregistration'),
path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
