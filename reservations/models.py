from django.db import models
from products.models import Product
from customers.models import Customer

class Timestart(models.Model):
     name = models.CharField(max_length=500)
     def __str__(self):
        return self.name

class Table(models.Model):
     name = models.CharField(max_length=500, default='A', blank=True)
     def __str__(self):
        return self.name


class Reservation(models.Model):
      DURATION_CHOICES = (("15", "15"),("30", "30"),("45", "45"),("60", "60"),
                        ("75", "75"),("90", "90"),("105", "105"),("120", "120"),
                        ("135", "135"),("150", "150"),("165", "165"),)

      table = models.ForeignKey(Table, related_name='reservation', on_delete=models.CASCADE)
      customer = models.ForeignKey(Customer, related_name='reservation', on_delete=models.CASCADE)
      product = models.ForeignKey(Product, related_name='reservation', on_delete=models.CASCADE)
      timestart = models.ForeignKey(Timestart, related_name='reservation', on_delete=models.CASCADE)
      duration = models.CharField(max_length=5, choices=DURATION_CHOICES, default="30")
      date = models.DateField()

      def __str__(self):
        return str(self.customer)

class Avail(models.Model):
     name = models.CharField(max_length=1000)
     reservation = models.ForeignKey(Reservation, related_name='avail', on_delete=models.CASCADE)
     date = models.DateField()
     def __str__(self):
        return self.name
