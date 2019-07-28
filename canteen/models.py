from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    date = models.DateField(auto_now=True)
    description = models.CharField(max_length=101)
    sold_out = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'dishes'

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    id_no = models.CharField('id no.', max_length=100)
    contact_no = models.IntegerField('contact no.')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    count = models.IntegerField()
    amount = models.FloatField(editable=False)
    served = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} orderred {self.dish}'
    
    def save(self, *args, **kwargs):
        self.amount = self.count * self.dish.price
        super().save(*args, **kwargs)

