from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("simple/", views.simple_view),
    path("simple/<int:year>/", views.simple_view),
]
