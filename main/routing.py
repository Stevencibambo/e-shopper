# Define WebSocket and No WebSocket, by default http is added

from eshopper.auth import TokenGetAuthMiddlewareStack
from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/customer-service/<int:order_id>/", consumers.ChatConsumer)
]

http_urlpatterns = [
    path("customer-service/notify/", AuthMiddlewareStack(consumers.ChatNotifyConsumer)),
    path("mobile-api/my-orders/<int:order_id>/tracker/",
         TokenGetAuthMiddlewareStack(consumers.OrderTrackerConsumer)),
]
