from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from vehicles import create_example_vehicles
from locations import City, Country
from locations import create_example_countries_and_cities
import math

class Trip():
    """
    Represents a sequence of cities.
    """
    def __init__(self, departure: City) -> None:
        """
        Initialises a Trip with a departure city.
        """
        #initialise the departure
        #create an empty list named self.store_city to store the departure city in order to calculate the total travel time
        self.departure = departure
        self.store_city = [] 
        self.store_city.append(self.departure) 

    def add_next_city(self, city: City) -> None:
        """
        Adds the next city to this trip.
        """
        #initialise the next city
        #add the next city to self.store_city
        self.city = city
        self.store_city.append(self.city) 
        
    def total_travel_time(self, vehicle: Vehicle) -> float:
        """
        Returns a travel duration for the entire trip for a given vehicle.
        Returns math.inf if any leg (i.e. part) of the trip is not possible.
        """     
        #create an empty list named time to store the travel time of each city in self.store_city
        #this for loop will calculate the travel time from the first city to second city first,after that calculate the travel time from second city to third city,and so on
        #after that we return the total of travel time by using sum
        time = []
        for i in range(len(self.store_city)-1):
            time.append(vehicle.compute_travel_time(self.store_city[i],self.store_city[i+1]))
        return sum(time)
      
    def find_fastest_vehicle(self, vehicles: 'list[Vehicle]') -> (Vehicle, float):
        """
        Returns the Vehicle for which this trip is fastest, and the duration of the trip.
        If there is a tie, return the first vehicle in the list.
        If the trip is not possible for any of the vehicle, return (None, math.inf).
        """
        #create a list called trip_time to store the total trip time for each vehicle
        #this for loop will check the total travel time of each vehicle in vehicles
        trip_time =[]
        for vehicle in vehicles:
            trip_duration = self.total_travel_time(vehicle)
            trip_time.append(trip_duration)
        
        #create an empty list named proper_time to store the proper total travel time of each vehicle
        #if the total travel time of vehicle is not math.inf,we append it into proper_time
        #other there is not fastest vehicle,and the fastest time is equal to math.inf
        proper_time = []
        for time in trip_time:
            if time != math.inf: 
                proper_time.append(time)
            else:
                car=None
                fastest_time = math.inf
        
        #then we arrange the time in proper_time by arranging from low to high
        #if there are many proper time,we will select the first element because the first element is the shortest total travel time as we sort already
        proper_time.sort()
        if len(proper_time) > 0:
            fastest_time = proper_time[0]
            car = vehicles[trip_time.index(fastest_time)]          
        return (car,fastest_time)
              
    def __str__(self) -> str:
        """
        Returns a representation of the trip as a sequence of cities:
        City1 -> City2 -> City3 -> ... -> CityX
        """
        
        cities = "{}".format(self.departure)
        for city in self.store_city[1:]:
            cities +=  " -> {}".format(city) 
        return cities

def create_example_trips() -> 'list[Trip]':
    """
    Creates examples of trips.
    """

    #first we create the cities and countries
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    #then we create trips
    trips = []

    for cities in [(melbourne, sydney), (canberra, tokyo), (melbourne, canberra, tokyo), (canberra, melbourne, tokyo)]:
        trip = Trip(cities[0])
        for city in cities[1:]:
            trip.add_next_city(city)
        trips.append(trip)

    return trips

if __name__ == "__main__":
    vehicles = create_example_vehicles()
    trips = create_example_trips()
      
    for trip in trips:
        vehicle, duration = trip.find_fastest_vehicle(vehicles)
        print("The trip {} will take {} hours with {}".format(trip, duration, vehicle))
