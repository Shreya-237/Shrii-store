from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('',views.home,name='home'),

    # Products
    path('products/',views.product_list,name='product_list'),

    # Product Details
    path('product/<int:id>/',views.product_detail,name='product_detail'),

    # Cart
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),

    path('cart/',views.cart,name='cart'),

    path('increase/<int:id>/',views.increase_quantity,name='increase_quantity'),

    path('decrease/<int:id>/',views.decrease_quantity,name='decrease_quantity'),

    path('remove/<int:id>/',views.remove_from_cart,name='remove_from_cart'),

    # Checkout
    path('checkout/',views.checkout,name='checkout'),

    # Orders
    path('my-orders/',views.my_orders,name='my_orders'),

    # User Registration
    path('register/',views.register,name='register'),

    # User Login
    path('login/',views.user_login,name='login'),

    # User Logout
    path('logout/',views.user_logout,name='logout'),
    
]