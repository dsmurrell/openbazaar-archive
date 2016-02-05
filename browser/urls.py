from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^vendors/', views.vendors, name="vendors"),
]