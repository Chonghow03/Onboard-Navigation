from locations import City, Country, test_example_countries_and_cities
import csv

def create_cities_countries_from_CSV(path_to_csv: str) -> None:
    """
    Reads a CSV file given its path and creates instances of City and Country for each line.
    """
    #create a list named lst to store the name of required column
    lst = ["city_ascii", "lat", "lng", "country", "iso3", "capital", "id"]
    
    #open the csv file that was passed in by the parameter
    #read the file
    #store the column names in a list
    #creating an empty list with the name "fields_id"
    #iterate over the list using index
    #store column index of value i into a list
    with open(path_to_csv, "r") as csvfile: 
        csvreader  = csv.reader(csvfile)
        fields = next(csvreader)
        fields_id = []
        for i in lst:
            fields_id.append(fields.index(i))
        #loop through the informations in the csvfile
        #value index of 0 in fields_id corresponds to the column index of city_ascii
        #value index of 1 in fields_id corresponds to the column index of latitude...
        #and so on
        for row in csvreader:
            city_ascii = row[fields_id[0]]
            lat = row[fields_id[1]]
            lng = row[fields_id[2]]
            country = row[fields_id[3]]
            iso3 = row[fields_id[4]]
            capital = row[fields_id[5]]
            id_country = row[fields_id[6]]

            #if this country is not in the country dictionary
            #pass in these parameters into the class Country
            if Country.countries.get(country) == None:
                Country(country,iso3)
            #pass in these parameters into the class City
            City(city_ascii, lat, lng, country, capital, id_country)

if __name__ == "__main__":
    create_cities_countries_from_CSV("worldcities_truncated.csv")
    test_example_countries_and_cities()




