from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator

class Car(models.Model):
    
    colors = [
        ("white", "WE"),
        ("black", "BK"),
        ("yellow", "YW"),
        ("green", "GN"),
        ("orange", "OE"),
        ("grey", "GY"),
        ("violet", "VT"),
        ("magenta", "MA")
    ]

    manufacturers = [
        ("Toyota", "TY"),
        ("Mitsubishi", "MI"),
        ("Mazda", "MZ"),
        ("Nissan", "NN"),
        ("Lexus", "LS"),
        ("VAZ", "LA"),
        ("Mercedes-Benz", "MB"),
        ("BMW", "BW"),
        ("Audi", "AI")
    ]


    car_id = models.CharField(max_length=8, unique=True, validators=[MinLengthValidator(8)])   
    color = models.CharField(max_length=16, choices=colors)
    manufacturer = models.CharField(max_length=16, choices=manufacturers)
    price = models.FloatField()  
    year = models.IntegerField(validators=[MinValueValidator(1989), MaxValueValidator(2020)])
    

