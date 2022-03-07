from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from boards.models import Board
from .serializers import BoardSerializer


class BoardView(generics.ListAPIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardDetailedView(generics.RetrieveAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
