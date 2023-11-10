import city_country_csv_reader
from locations import create_example_countries_and_cities
from trip import Trip, create_example_trips
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

def plot_trip(trip: Trip, projection = 'robin', line_width=2, colour='b') -> None:
    """
    Plots a trip on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.
    """
    #figure size of the map 
    plt.figure(figsize=(12,9))
    
    #from string convert it to numbers
    lats = [float(city.latitude) for city in trip.store_city]
    lons = [float(city.longitude) for city in trip.store_city]
    
    #to expand border width
    lllat = min(lats) - 5
    urlat = max(lats) + 5
    lllon = min(lons) - 5
    urlon = max(lons) + 5

    #the width of the latitude equals to upper right latitude minus lower left latitude
    #if the  width of the latitude is lesser than 100
    #then the upper right latitude is equal to lower left latitude + 100
    width_lat = urlat - lllat
    if width_lat < 100:
        urlat = lllat + 100
    
    #the width of the longtitude equals to upper right longtitude minus lower left longtitude
    #if the  width of the longtitude is lesser than 100
    #then the upper right longtitude is equal to lower left longtitude + 100
    width_lon = urlon - lllon
    if width_lon < 100:
        urlon = lllon + 100
    
    #draw the map background
    m = Basemap(projection="mill", resolution='c',
                llcrnrlat=lllat, urcrnrlat=urlat,
                llcrnrlon=lllon, urcrnrlon=urlon)

    
    m.drawcoastlines()
    m.fillcontinents(color = 'lightgreen')
    m.drawmapboundary(fill_color = 'lightblue')
    #labels=[left,right,top,bottom]
    m.drawparallels(np.arange(-90,90,30),labels = [True,False,False,False])
    m.drawmeridians(np.arange(-180,180,30),labels = [False,False,False,True])
 
    
    #iterates through numbers which can be used for index access of trip.store_city and subtract 1
    #lon1,lat1 is the longtitude and latitude of the first city
    #lon2,lat2 is the longtitude and latitude of the next cit
    #i+1 corresponds to the travelling of the first city to next city
    for i in range(len(trip.store_city) - 1):
        lon1, lat1 = float(trip.store_city[i].longitude), float(trip.store_city[i].latitude)
        lon2, lat2 = float(trip.store_city[i+1].longitude), float(trip.store_city[i+1].latitude)
        m.drawgreatcircle(lon1, lat1, lon2, lat2, lw=line_width, c=colour)

    figname = "_".join([city.name for city in trip.store_city])
    title = "->".join([city.name for city in trip.store_city])
    ax = plt.title(label=title)
    plt.savefig(f"map_{figname}.png")
    plt.show()


if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

    create_example_countries_and_cities()

    trips = create_example_trips()

    for trip in trips:
        plot_trip(trip)



