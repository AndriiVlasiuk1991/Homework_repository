from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("upload_quote/", views.upload_quotes, name="upload_quote"),
    path('author_info/<str:author_name>/', views.author_info, name='author_info'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
]
