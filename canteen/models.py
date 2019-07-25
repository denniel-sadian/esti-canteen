from django.db import models



class Dish(model.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    date = models.DateField(auto_now=True)
    estimated_count = models.IntegerField('good for how many people')

    def __str__(self):
        return self.name


class Order(model.Model):
    date = models.DateField(auto_now=True)
    custumer_name = models.CharField(max_length=100)
    custumer_id_no = models.CharField(max_length=100)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    count = models.IntegerField()
    amount = models.FloatField()

    def __str__(self):
        return f'{self.customer_name} orderred {self.dish}'
    
    def save(self, *args, **kwargs):
        self.amount = self.count * self.dish.price
        super().save(*args, **kwargs)

