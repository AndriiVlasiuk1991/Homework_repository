from django.urls import path, include
from . import views

app_name = "authors"

urlpatterns = [
    path('', views.index, name='home'),  # authors:home
    path('tag/', views.tag, name='tag'),  # authors:tag
    path('authors/', views.authors, name='authors'),  # authors:authors
    path('quotes/', views.quotes, name='quotes'),  # authors:quotes
]
