from .models import Passenger

def find_passengers(start_point, end_point, date, number_of_free_seats):
    return Passenger.objects.all()