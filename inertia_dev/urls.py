from django.contrib import admin
from django.urls import path
from main.views import home, chat

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"", home),
    path('chat/', chat, name='chat'),
]
