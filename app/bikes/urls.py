from django.urls import path, include
from rest_framework.routers import DefaultRouter

from bikes import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'bikes'

urlpatterns = [
    path('', include(router.urls))
]
