from rest_framework import mixins, viewsets
from stockdata import serializers, models
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class StockViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.StockSerializer
    queryset = models.Stock.objects.all()

    @method_decorator(cache_page(60*5))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(pk=self.kwargs['pk'])




















