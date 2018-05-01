from django.conf.urls import url
from django.urls import path, include
from status.views import StatusView

urlpatterns = [
    path('', StatusView.as_view(), name='home'),
]
