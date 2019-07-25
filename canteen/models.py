from django.db import models



class Dish(model.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    date = models.DateField(auto_now=True)
    estimated_count = models.IntegerField('good for how many people')

    def __str__(self):
        return self.name
