from rest_framework import mixins, viewsets
from stockdata import serializers, models


class StockViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.StockSerializer
    queryset = models.Stock.objects.all()























