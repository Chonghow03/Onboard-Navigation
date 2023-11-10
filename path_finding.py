import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles
import networkx as nx
import math

def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:
    """
    Returns a shortest path between two cities for a given vehicle,
    or None if there is no path.
    """
    #create a empty graph
    #initialise an empty list call path_cities to store all the cities 
    G = nx.Graph() 
    path_cities = [] 
    for x in City.cities.values():
        path_cities.append(x) 

    #loop through the length of the (path_cities list minus 1)
    #loop through in range (from f+1 to the length of the path_cities)
    #calculate the travel time for the given vehicle from city f to city a
    #if the trip is possible for the given vehicle
    #add edge between the two cities to the graph and represent their weight in time
    for f in range(len(path_cities)-1): 
        for a in range(f+1,len(path_cities)): 
            time = vehicle.compute_travel_time(path_cities[f],path_cities[a]) 
            if time != math.inf:
                G.add_edge(path_cities[f],path_cities[a],weight=time)
                
    #nx.shortest_path will create a list and store the shortest path from source(from_city) to target(to_city) 
    #let the index 0 of the shortest_path which is from_city become parameter of the Trip class and store it into store_city list
    #loop through the shortest_path list and add the other city into store_city list
    #if the error occurs,means this trip is not possible for this vehiclereturn "Impossible vehicle"
    try: 
        shortest_path=nx.shortest_path(G,from_city,to_city)
        shortest_found = Trip(shortest_path[0])
        for trips in shortest_path[1:]:
            shortest_found.add_next_city(trips)
        return shortest_found
    except: 
        return None

if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")
    
    vehicles = create_example_vehicles()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    for vehicle in vehicles:
        print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo, find_shortest_path(vehicle, melbourne, tokyo)))
