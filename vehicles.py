from abc import ABC, abstractmethod
import math
from locations import CapitalType, City, Country
from locations import create_example_countries_and_cities

class Vehicle(ABC):
    """
    A Vehicle defined by a mode of transportation, which results in a specific duration.
    """

    @abstractmethod
    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """   
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        """
        pass


class CrappyCrepeCar(Vehicle):
    """
    A type of vehicle that:
        - Can go from any city to any other at a given speed.
    """

    def __init__(self, speed: int) -> None:
        """
        Creates a CrappyCrepeCar with a given speed in km/h.
        """
        #initialise the speed of CrappyCrepeCar
        self.speed = speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        """
        #there is not any limitation for CrappyCrepeCar,therefore the duration of travel will be distance divided by speed
        #after calculating the duration,we use ceil to round up duration to an integer 
        duration = math.ceil(departure.distance(arrival) / self.speed)
        return duration

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "CrappyCrepeCar (100 km/h)"
        """
        return "CrappyCrepeCar ({} km/h)".format(self.speed)


class DiplomacyDonutDinghy(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities in the same country.
        - Can travel between two cities in different countries only if they are both "primary" capitals.
        - Has different speed for the two cases.
    """

    def __init__(self, in_country_speed: int, between_primary_speed: int) -> None:
        """
        Creates a DiplomacyDonutDinghy with two given speeds in km/h:
            - one speed for two cities in the same country.
            - one speed between two primary cities.
        """
        #initialise the in_country_speed and between_primary_speed of DiplomacyDonutDinghy
        self.in_country_speed = in_country_speed
        self.between_primary_speed = between_primary_speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        #if the iso code of departure is equal to arriva;, the speed will be in_country_speed
        #therefore the duration will be the distance between departure and arrival divided by in_country_speed
        #after calculating the duration,we use ceil to round up duration to an integer 
        if self.search_iso(departure) == self.search_iso(arrival):
            duration = math.ceil(departure.distance(arrival) / self.in_country_speed)

        #if the iso code of departure is not equal to arrival,while both cities are primary type
        #therefore the duration will be the distance between departure and arrival divided by between_primary_speed
        #after calculating the duration,we use ceil to round up duration to an integer 
        #if the iso code of departure is not equal to arrival,while both cities are not primary type
        #the duration will be math.inf
        else:
            if departure.capital_type == "primary" and arrival.capital_type == "primary":
                duration = math.ceil(departure.distance(arrival) / self.between_primary_speed)
            else: 
                duration = math.inf
                
        return duration

    def search_iso(self, metro: City):
        """
        Create a function to find the iso code of each City
        """
        #first we convert the city into string,therefore by adding string metro with index -4,-3,-2,we can get the iso code of each city
        #we cannot select index -1 because -1 is ")"
        iso = list(str(metro))[-4]+list(str(metro))[-3]+list(str(metro))[-2]
        return iso

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "DiplomacyDonutDinghy (100 km/h | 200 km/h)"
        """
        return "DiplomacyDonutDinghy ({} km/h | {} km/h)".format(self.in_country_speed, self.between_primary_speed)


class TeleportingTarteTrolley(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities if the distance is less than a given maximum distance.
        - Travels in fixed time between two cities within the maximum distance.
    """

    def __init__(self, travel_time:int, max_distance: int) -> None:
        """
        Creates a TarteTruck with a distance limit in km.
        """
        #initialise the travel_time and max_distance of TeleportingTarteTrolley
        self.travel_time = travel_time
        self.max_distance = max_distance

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        #if the distance of travel is within maximum distance,the duration will be travel_time,which is a fixed time
        #if the distance of travel is over maximum distance,the duration will be math.inf
        if departure.distance(arrival) < self.max_distance:
            duration = self.travel_time
        else:
            duration = math.inf
        return duration

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "TeleportingTarteTrolley (5 h | 1000 km)"
        """
        return "TeleportingTarteTrolley ({} h | {} km)".format(self.travel_time,self.max_distance)


def create_example_vehicles() -> 'list[Vehicle]':
    """
    Creates 3 examples of vehicles.
    """
    return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]
    

if __name__ == "__main__":
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    vehicles = create_example_vehicles()
    for vehicle in vehicles:
        for from_city, to_city in [(melbourne, canberra), (tokyo, canberra), (tokyo, melbourne)]:
            print("Travelling from {} to {} will take {} hours with {}".format(from_city, to_city, vehicle.compute_travel_time(from_city, to_city), vehicle))
