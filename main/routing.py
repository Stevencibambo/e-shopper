# Define WebSocket and No WebSocket, by default http is added

from channels.auth import AuthMiddlewareStack
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/customer-service/<int:order_id>/", consumers.ChatConsumer)
]

http_urlpatterns = [
    path("customer-service/notify/", AuthMiddlewareStack(consumers.ChatNotifyConsumer))
]
