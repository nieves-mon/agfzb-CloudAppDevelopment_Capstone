from django.db import models
from django.utils.timezone import now


# Create your models here.

# CarMake Model
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='ford')
    description = models.CharField(max_length=500)
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.name + ': ' + self.description

# CarModel
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=30, default="")
    dealer_id = models.IntegerField(null=False)
    type = models.CharField(null=False, max_length=9, choices=(('Sedan', 'Sedan',), ('SUV', 'SUV'), ('HATCHBACK', 'HATCHBACK'),('WAGON', 'WAGON')))
    year = models.DateField(null=False)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    def __str__(self):
        return self.make + ' ' + self.name + ' ' + self.year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
