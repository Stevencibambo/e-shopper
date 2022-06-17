"""
url of main app
author <steven@gmail.com>
"""
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from rest_framework.authtoken import views as authtoken_views
from django.urls import path, include
from rest_framework import routers
from main import endpoints
from main import views
from main import models
from main import forms

router = routers.DefaultRouter()
router.register(r'orderlines', endpoints.PaidOrderLineViewSet)
router.register(r'orders', endpoints.PaidOrderViewSet)


urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("contact-us/", views.ContactUsView.as_view(), name="contact_us"),
    path("about-us/", TemplateView.as_view(template_name="about_us.html"), name="about_us"),

    path("products/", views.all_products, name="product_tags"),
    path("product/<slug:slug>/", views.product_detail, name="product"),
    path("products/<slug:tag>/<slug:subtag>/", views.tag_products, name="products"),

    path("basket/", views.manage_basket, name="basket"),
    path("add_to_basket/", views.add_to_basket, name="add_to_basket"),

    path("order/done", TemplateView.as_view(template_name="order_done.html"), name="checkout_done"),
    path("order/address_select/", views.AddressSelectionView.as_view(), name="address_select"),
    path("order-dashboard/", views.OrderView.as_view(), name="order_dashboard"),

    path("address/", views.AddressListView.as_view(), name="address_list"),
    path("address/create/", views.AddressCreateView.as_view(), name="address_create"),
    path("address/<int:pk>/", views.AddressUpdateView.as_view(), name="address_update"),
    path("address/<int:pk>/delete", views.AddressDeleteView.as_view(), name="address_delete"),

    path("login/", auth_views.LoginView.as_view(template_name="login.html", form_class=forms.AuthenticationForm,), name="log-in"),
    path("signup/", views.SignupView.as_view(), name="signup"),

    path("api/", include(router.urls)),
    path("customer-service/<int:order_id>/", views.room, name="cs_chat",),
    path("customer-service/", TemplateView.as_view(template_name="customer_service.html"), name="cs_main",),
    path("mobile-api/auth/", authtoken_views.obtain_auth_token, name="mobile_token",),
    path("mobile-api/my-orders/", endpoints.my_orders, name="mobile_my_orders",),
]
