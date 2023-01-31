from django.urls import path
from owner import views

urlpatterns=[
    path("index",views.AdminDashBoardView.as_view(),name="dashboard"),
    path("order/latest",views.OrderListView.as_view(),name="neworders"),
    path("order/details/<int:id>",views.OrderDetailView.as_view(),name="order-details")
]