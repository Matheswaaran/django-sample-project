from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'boards_api'

router = routers.DefaultRouter()
router.register('boards', views.BoardsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('boards/',
         views.BoardView.as_view(),
         name='subject_list'),
    path('boards/<pk>/',
         views.BoardDetailedView.as_view(),
         name='subject_detail'),
]
