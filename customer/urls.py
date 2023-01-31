from django.urls import path
from customer import views

urlpatterns=[
   path('',views.LoginView.as_view(),name="login"),
   path('signout',views.SignOutView.as_view(),name='signout'),
   path("register",views.RegistrationView.as_view(),name="register"),
   path("home",views.HomeView.as_view(),name="home"),
   path("products/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
   path("products/<int:id>/carts/add",views.AddToCartView.as_view(),name="addto-cart"),
   path("carts/all",views.MyCartView.as_view(),name="mycart"),
   path("products/<int:id>/delete",views.CartRemoveView.as_view(),name="cart-remove"),
   path("carts/placeorder/<int:c_id>/<int:p_id>",views.PlaceOrderView.as_view(),name="place-order"),
]