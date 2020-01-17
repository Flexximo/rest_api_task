from .models import Car
from .serializers import CarSerializer, ResponseSerializer
from datetime import datetime
from django.db.utils import IntegrityError
import re
from rest_framework.decorators import api_view
from rest_framework.response import Response



class ResponseOnRequest(object):
    def __init__(self, status, info, created=None):
        self.status = status
        self.info = info
        self.created = created or datetime.now()


#One function, no class-based views

@api_view(["GET", "POST", "DELETE", "PATCH"])
def api_handler(request, id=None):
    cars = Car.objects.all()
    colors = [color[0] for color in Car.colors]
    manufacturers = [name[0] for name in Car.manufacturers] 
    #api/cars/<car_id> logic
    if id:
        if request.method == "GET":           
            car = cars.filter(car_id=id).get()
            if car:
               serializer = CarSerializer(car, many=False)     
               return Response(serializer.data)
            else:
               return Response(ResponseSerializer(ResponseOnRequest(status=f"id {id} doesn't exist", 
                                                                     info="Please, use valid car id"))
                                                                     .data)            
        elif request.method == "DELETE":
            car = cars.filter(car_id=id).get()
            if car:
                car.delete()
                return Response(ResponseSerializer(ResponseOnRequest(status=f"Success!", 
                                                                     info=f"Car with id {id} is deleted"))
                                                                     .data)   
            else:
                return Response(ResponseSerializer(ResponseOnRequest(status=f"id {id} doesn't exist", 
                                                                     info="Please, use valid car id"))
                                                                     .data)   
        #Im the wonder is it needed to change id here, if it's unique? -_-
        elif request.method == "PATCH":
            car = cars.filter(car_id=id).get()
            print(car)
            if car:
                data = request.data
                color = data["color"]
                manufacturer = data["manufacturer"]
                price = float(data["price"])
                year = int(data["year"])
                if not color in colors:
                        return Response(ResponseSerializer(ResponseOnRequest(status=f"color {color} is not a color of set", 
                                                                             info=f"Please, use color from the given set {colors} only"))
                                                                             .data)
                elif not manufacturer in manufacturers:
                        return Response(ResponseSerializer(ResponseOnRequest(status=f"manufacturer {manufacturer} is not a in our set", 
                                                                             info=f"Please, use manufacturer from the given set {manufacturers} only"))
                                                                             .data)   
                elif price < 1000 or price > 1000000:
                        return Response(ResponseSerializer(ResponseOnRequest(status=f"price {price} is not acceptable or wrong format", 
                                                                             info=f"Price should be greater than 1.000 and less than 1.000.000 only"))
                                                                             .data)   
                elif year < 1989 or year > 2020:
                        return Response(ResponseSerializer(ResponseOnRequest(status=f"year of manufacture {year} is not acceptable or wrong format", 
                                                                             info=f"Please, use correct year between 1989 and 2020 inclusively {manufacturers}"))
                                                                             .data)   
                else:
                    car.color = color
                    car.manufacturer = manufacturer
                    car.price = price
                    car.year = year
                    car.save()
                    return Response(ResponseSerializer(ResponseOnRequest(status=f"Success!", 
                                                                         info=f"Data with id {id} is patched and updated"))
                                                                         .data)    
    #api/cars/ logic
    else:
        #show all the car objects on GET request
        if request.method == "GET":
            cars = Car.objects.all()
            serializer = CarSerializer(cars, many=True)
            return Response(serializer.data)
        #check if data is valid, if not - sends Response object to client, otherwise saves in data in db and sends OK response.
        elif request.method == "POST":
            data = request.data          
            car_id = str(data["car_id"])
            color = data["color"]
            manufacturer = data["manufacturer"]
            price = float(data["price"])
            year = int(data["year"])
            if not re.match(r"[A-Za-z0-9]{8}", car_id):
                return Response(ResponseSerializer(ResponseOnRequest(status=f"id {car_id} of invalid length or data", 
                                                                     info="Please, use digits only or characters only, or both to create id with min & max length of 8, e.g. FF0X2b01"))
                                                                     .data)
            elif not color in colors:
                return Response(ResponseSerializer(ResponseOnRequest(status=f"color {color} is not a color of set", 
                                                                     info=f"Please, use color from the given set {colors} only"))
                                                                     .data)
            elif not manufacturer in manufacturers:
                return Response(ResponseSerializer(ResponseOnRequest(status=f"manufacturer {manufacturer} is not a in our set", 
                                                                     info=f"Please, use manufacturer from the given set {manufacturers} only"))
                                                                     .data)   
            elif price < 1000 or price > 1000000:
                return Response(ResponseSerializer(ResponseOnRequest(status=f"price {price} is not acceptable or wrong format", 
                                                                     info=f"Price should be greater than 1.000 and less than 1.000.000 only"))
                                                                     .data)   
            elif year < 1989 or year > 2020:
                return Response(ResponseSerializer(ResponseOnRequest(status=f"year of manufacture {year} is not acceptable or wrong format", 
                                                                     info=f"Please, use correct year between 1989 and 2020 inclusively {manufacturers}"))
                                                                     .data)   
            else:
                try:
                    Car.objects.create(car_id=car_id, color=color, manufacturer=manufacturer, price=price, year=year).save()
                except IntegrityError:
                    return Response(ResponseSerializer(ResponseOnRequest(status=f"id {car_id} is not unique", 
                                                                     info="Please, use another unique id"))
                                                                     .data)
                else:
                    return Response(ResponseSerializer(ResponseOnRequest(status=f"OK!", 
                                                                     info=f"Data with id {car_id} is created"))
                                                                     .data)
        else:
            return Response(ResponseSerializer(ResponseOnRequest(status=f"Bad", 
                                                                     info=f"Only POST and GET methods available"))
                                                                     .data)    