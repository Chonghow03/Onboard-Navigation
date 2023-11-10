from __future__ import annotations
from geopy.distance import great_circle
from enum import Enum
from math import ceil


class CapitalType(Enum):
    """
    The different types of capitals (e.g. "primary").
    """
    primary = "primary"
    admin = "admin"
    minor = "minor"
    unspecified = ""

    def __str__(self) -> str:
        return self.value


class Country():
    """
    Represents a country.
    """

    countries = dict() # a dict that associates country names to instances.

    def __init__(self, name: str, iso3: str) -> None:
        """
        Creates an instance with a country name and a country ISO code with 3 characters.
        """
        #initialise the name, iso of country
        #store the name of each country into countries dictionary
        #create an empty list named self.country_city to store city
        #self is a Country class

        self.name = name
        self.iso3 = iso3
        self.country_cities = []
        Country.countries[name] = self


    def _add_city(self, city: City):
        """
        Adds a city to the country.
        """	
        #add city into the self.country_cities list
        
        self.country_cities.append(city)

    def get_cities(self, capital_types: list[CapitalType] = None) -> list[City]:
        """
        Returns a list of cities of this country.

        The argument capital_types can be given to specify a subset of the capital types that must be returned.
        Cities that do not correspond to these capital types are not returned.
        If no argument is given, all cities are returned.
        """
        #create an empty list named result
        #if the cities correspond to these capital types
        #the first for loop is to loop each city in the list of self.country_cities
        #the second for loop is to check the types of each city
        #if the values of the type is equal to the cities' capital type, we store it into the result and break the loop
        
        result = []
        if capital_types:
            for city_ in self.country_cities:
                for type_ in capital_types:
                    if type_.value == city_.capital_type:
                        result.append(city_)
                        break
        #if the cities do not correspond to these capital types
        
        else:
            result = self.country_cities
        
        return result


    def get_city(self, city_name: str) -> City:
        """
        Returns a city of the given name in this country.
        Returns None if there is no city by this name.
        If there are multiple cities of the same name, returns an arbitrary one.
        """
        #no city by this name
        #loop through the city name in this country
        #if there is a city by this name, returns the city and break
        
        city = None 
        for city_ in self.country_cities:
            if city_.name == city_name: 
                city = city_
                break 
        
        return city

    def __str__(self) -> str:
        """
        Returns the name of the country.
        """
        return self.name


class City():
    """
    Represents a city.
    """

    cities = dict() # a dict that associates city IDs to instances.

    def __init__(self, name: str, latitude: str, longitude: str, country: str, capital_type: str, city_id: str) -> None:
        """
        Initialises a city with the given data.
        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.country = country
        self.capital_type = capital_type
        self.city_id = city_id
        City.cities[city_id] = self
        Country.countries[country]._add_city(self)

    def distance(self, other_city: City) -> int:
        """
        Returns the distance in kilometers between two cities using the great circle method,
        rounded up to an integer.
        """
        #the latitude and longtitude of the first city
        #the latitude and longtitude of the next city
        #return the distance between two cities by using the function called great_circle which was imported from geopy
        #since we ceil the distance,as long as the distance includes decimal point,distance will plus one 
        
        city_1 = (self.latitude, self.longitude)
        city_2 = (other_city.latitude, other_city.longitude)

        return ceil(great_circle(city_1, city_2).km)

    def __str__(self) -> str:
        """
        Returns the name of the city and the country ISO3 code in parentheses.
        For example, "Melbourne (AUS)".
        """
        return f"{self.name} ({Country.countries[self.country].iso3})"

def create_example_countries_and_cities() -> None:
    """
    Creates a few Countries and Cities for testing purposes.
    """
    australia = Country("Australia", "AUS")
    melbourne = City("Melbourne", "-37.8136", "144.9631", "Australia", "admin", "1036533631")
    canberra = City("Canberra", "-35.2931", "149.1269", "Australia", "primary", "1036142029")
    sydney = City("Sydney", "-33.865", "151.2094", "Australia", "admin", "1036074917")

    japan = Country ("Japan", "JPN")
    tokyo = City("Tokyo", "35.6839", "139.7744", "Japan", "primary", "1392685764")


def test_example_countries_and_cities() -> None:
    """
    Assuming the correct cities and countries have been created, runs a small test.
    """
    australia = Country.countries['Australia']
    canberra =  australia.get_city("Canberra")
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")

    print("The distance between {} and {} is {}km".format(melbourne, sydney, melbourne.distance(sydney)))

    for city in australia.get_cities([CapitalType.admin, CapitalType.primary]):
        print("{} is a {} capital of {}".format(city, city.capital_type, city.country))


if __name__ == "__main__":
    create_example_countries_and_cities()
    test_example_countries_and_cities()

