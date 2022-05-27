from django.db import models


class Stock(models.Model):
    stock_name = models.CharField(max_length=30, editable=False, primary_key=True)

    def __str__(self):
        return self.stock_name


class Trade(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    time = models.DateTimeField()
    price = models.FloatField()
    volume = models.IntegerField()

    def __str__(self):
        return self.stock

    class Meta:
        ordering = ['time']
