from locations import City, Country, test_example_countries_and_cities, create_example_countries_and_cities
import city_country_csv_reader
from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley, create_example_vehicles
from trip import Trip, create_example_trips
from map_plotting import plot_trip
from path_finding import find_shortest_path
import networkx as nx
import math
import time
from typing import List

class Navigation():
    
    def __init__(self) -> None:
        """
        Create these empty lists for further fuctions to use
        """
        #create self.fleet as an empty list to store the vehicles selected by user
        #create self.trips as en empty list to store the trip of user
        #suppose there is not fastest vehicle and the duration of trip is 0 at the initially trip
        #create self.each_cities_time_lst as an empty list to store the travel time of each city in the trip
        #create self.travel_city as an empty list to store the cities in trip
        #create self.order_total_time as a list to store the addtion of travel time in the self.each_cities_time_lst,and we assign 0 in the list because the travel time is 0 when user doesn't start the trip 
        #read the data in worldcities_truncated.csv and call the function self.main_menu
        self.fleet=[]
        self.trips=[]
        self.fastest_vehicle= None
        self.duration = 0
        self.each_cities_time_lst = []
        self.travel_city = []
        self.order_total_time = [0]
        city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")
        self.main_menu()

    def vehicle_customization(self):
        """
        Ask the user to input the number of vehicles in their fleet
        Ask the user to customize their vehicles if they want to customize their vehicles 
        """
        #create a while loop for user to input the number of vehicles in fleet until it is valid 
        #try and except is used to identify the input of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
        #since the user should create at least 2 vehicles in the fleet,so when the input is below 2,we will prompt the user to input again
        print("Let's customize your fleet of vehicles"+" \N{slightly smiling face}")
        while True:
            try:
                num_of_vehicles = int(input("Please enter the number of vehicles (at least 2) in your fleet:"))
                if num_of_vehicles < 2:
                    print("You should create your fleet with at least two vehicles!")
                else:
                    break
            except ValueError:
                print("Wrong input format ! Please try again "+"\U0001F61E")
        
        #this for loop will run through with the number of vehicles decided by user 
        #it is because user can either choose the vehicles from example vehicles or customize vehicles manually in their fleet
        for vehicles in range(num_of_vehicles):
            print("Vehicle",int(vehicles+1))
            print("1:Select from example vehicles\n2:Create your own fleet of vehicle")
            
            #create a while loop for user to input their option until it is valid
            #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
            #since the user has 2 options only,therefore if user's input is greater than 2 or lower than 1,we will prompt the option is not available
            #if user's option is 1,call the function of self.example_vehicles for user to select vehicles from example_vehicles,and store the vehicle into the self.fleet
            #if user's option is 2,call the function of self.create_vehicles for user to create their own vehicles,and store the vehicle into the self.fleet
            while True:
                try:
                    option = int(input("Enter your option:"))
                    if option > 2 or option < 1:
                        print("Option is not available!")
                    else:
                        if option == 1:
                            vehicle = self.example_vehicles()
                            self.fleet.append(vehicle)
                            break
                        else:
                            vehicle = self.create_vehicles()
                            self.fleet.append(vehicle)
                            break
                except ValueError:
                    print("Wrong input format ! Please try again "+"\U0001F61E")
        print("\N{slightly smiling face}"+"Your fleet of vehicles are customized done!\n")
        with open("vehicle_history.txt","a") as history:
            for vehicles in self.fleet:
                history.write(str(vehicles)+'\n')
            history.close()
        
        
    def trip_customization(self):
        """
        Ask the user to customize their trip 
        """
        #we need to check user has selected vehicles in their fleet or not,because user should use vehicle to start the Trip
        #if user doesn't has vehicles in their fleet,call the function self.vehicle_customization for user to customize vehicles
        if len(self.fleet) == 0:
            print("You do not have any vehicles ")
            self.vehicle_customization()
        print("Let customize your trip"+" \N{winking face}")
        print("------Select your trip from these three options------")
        print("1.Select the example trips\n2.Adding your preferred cities to your trip\n3.The shortest path between two cities")
            
        #create a while loop for user to input their option until it is valid
        #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
        #since the user has 3 options only,therefore if user's input is greater than 3 or lower than 1,we will prompt the option is not available
        while True:
            try:
                option = int(input("Enter your option:"))
                if option < 1 or option > 3:
                    print("Option is not available!")
                else:

                    #if user's option is 1,call the function self.example_trips for user to select their trip from example_trips,and store the trip into self.trips
                    #if user's option is 2,call the function self.manually_create_trips for user to create their trip by inputting multiple 
                    #if user's option is 3,call the function self.shortest_path_trip for user to enter 2 cities only,and we will find the shortest path between these 2 cities for user's trip
                    if option == 1:
                        trip = self.example_trips()
                        self.trips.append(trip)
                        break
                    elif option == 2:
                        trip = self.manually_create_trip()
                        self.trips.append(trip)
                        break
                    else:
                        trip = self.shortest_path_trip()
                        self.trips.append(trip)
                        break
            except ValueError:
                print("Wrong input format ! Please try again "+"\U0001F61E")
        
        with open("trip_history.txt","a") as journey:
            for trip in self.trips:
                journey.write(str(trip)+'\n')
            journey.close()
        
    def trip_fastest_vehicle(self):
        """
        Find the fastest vehicle from self.fleet
        """
        #we need to check user has selected vehicles in their fleet or not,because user should use vehicle to start the Trip
        #if user doesn't has vehicles in their fleet,call the function self.vehicle_customization for user to customize vehicles
        #we need to check user has selected trips or not,because user should has trips to find the fastest vehicle
        #if user hasn't selected trips,call the function self.trip_customization for user to customize trip
        if len(self.fleet) == 0:
            print("You does not have any vehicles")
            self.vehicle_customization()
        if len(self.trips) == 0:
            print("You haven't customize your trip")
            self.trip_customization()
        
        #if user has selected vehicles and trips,create a for loop to run through each trip in the self.trips in order to find the fastest vehicle
        for trip in self.trips:
            self.fastest_vehicle, self.duration = trip.find_fastest_vehicle(self.fleet)
            print("The fastest vehicle is {}".format(self.fastest_vehicle))

    def trip_map_plotting(self):
        """
        Plot the trip of user
        """
        #if user hasn't selected trips,call the function self.trip_customization for user to customize trip
        #create a for loop to run through each trip in the self.trips,and call the function plot_trip to plot the map of each trip
        if len(self.trips) == 0:
            print("You haven't customize your trip")
            self.trip_customization()
        for trip in self.trips:
            plot_trip(trip)
        
    def trip_simulation(self):
        """
        Simulates the time of trip of user, 0.1 second means 1 hour
        """
        #if the user has not find the fastest vehicle,call the function trip_fastest_vehicle to let user find the fastest vehicle
        if self.fastest_vehicle == None:
            self.trip_fastest_vehicle()

        #set the number of progress_bar_size to 100,which means there will 100 bar
        #the self.duration should multiply with 0.1 because 0.1 second represent 1 hour,and store the result to variable named download_time
        #each of the bar time is equal to the result of download_time divided by progress_bar_size
        progress_bar_size = 100
        download_time = self.duration * 0.1
        one_bar_time = download_time / progress_bar_size
        
        #the first for loop will run through the trip in self.trips
        #the second for loop will run through the range of self.store_city - 1
        #we need to minus 1 because if there has 5 cities,we only need to compare 4 times in order to find the travel time of this city to next city by ordering 
        #then we store the travel time of this city to next city into the variable named each_cities_time by multiplying with 0.1
        #and store each_cities_time into each_cities_time_lst
        for trip in self.trips:
            for city in range(len(trip.store_city) - 1):
                each_cities_time = (self.fastest_vehicle.compute_travel_time(trip.store_city[city],trip.store_city[city+1])) * 0.1
                self.each_cities_time_lst.append(each_cities_time)
        
        #these two for loops are created to store each city of the trip into self.travel_city,so we can display the city in the trip in the next for loop
        for trip in self.trips:
            for city in trip.store_city:
                self.travel_city.append(city)

        #initialise initial_time to 0,because the initial travel time is 0
        #this for loop is created to add the time from one city to next city accordingly by ordering,and append the result into self.order_total_time
        #for instance if there are 4 cities,the self.order_total_time will include travel time of first city to second city,and travel time of first city to second city and third city,and so on
        initial_time = 0
        for timelapse in self.each_cities_time_lst:
            initial_time += timelapse
            self.order_total_time.append(initial_time)
        print(' 0%  [                                                                                                      ]',end='\r')

        #initialise current_time for storing the one_bar_time
        #initialise index to 0 for displaying the city in self.travel_city 
        #this for loop will run through the number of progress bar size
        #create a variable named star to represent the number of star,bar should plus 1 because the first time the for loop run,bar is 0 
        #create a variable named percentage to represent the percentage,bar should plus 1 because the first time the for loop run,bar is 0
        #create a variable named space to create the space in print statement,and this space should minus the number of star because by adding 1 star,the number of space will decrease by 1
        #adding the one bar time and store it into current_time
        #create a variable named display_city to print the according city in self.travel_city during the user's trip
        current_time = 0
        index = 0
        for bar in range (progress_bar_size): 
            star="*"*(bar+1)
            percentage=(bar+1)
            space=" "*(progress_bar_size-len(star))
            current_time += one_bar_time
            display_city=self.travel_city[index]

            #if the first time in order_total_time is lower than current_time,we remove this first time
            #so the second time will become first time,and we compare the second time with current time again
            #if we don't remove,this for loop will always compare the first time with current time
            #then adds the index with 1,therefore the display_city will display the next city
            #inside the print statement we add star and space together because when star decrease,space will decrease,but the length will remain same
            if self.order_total_time[0] < current_time :
                self.order_total_time.remove(self.order_total_time[0])
                index += 1
            time.sleep(one_bar_time)
            print(str(percentage)+'%  ['+star+space+'] ✈️Travel to '+str(display_city)+'                 ',end='\r')
        print("\n")
        
        #reset these variables again because these variables are set at init
        self.each_cities_time_lst = []
        self.travel_city = []
        self.order_total_time = [0]
    
    def history(self):
        """
        This fucntion is created to store the history vehicles and history trips entered by user
        """
        #create a file named vehicle_history.txt to store the history of vehicles entered by user
        #the for loop will print each of the vehicle entered by user
        with open("vehicle_history.txt",'r') as vehicles:
            print("Your history vehicles:\n")
            for vehicle in vehicles.readlines():
                print(vehicle)
            vehicles.close()

        #create a file named trip_history.txt to store the history of trip selected by user
        #the for loop will print each of the trip entered by user
        with open("trip_history.txt",'r') as trips:
            print("Your history trips:\n")
            for trip in trips.readlines():
                print(trip)
            trips.close()

    def restart(self):
        """
        If user presses restart, we will reset all data 
        """
        self.fleet=[]
        self.trips=[]
        self.fastest_vehicle= None
        self.duration = 0
        self.each_cities_time_lst = []
        self.travel_city = []
        self.order_total_time = [0]

    def create_vehicles(self):
        """
        This function is created for user to modify the conditions of their vehicle in the trip
        """
        print("1:CrappyCrepeCar \U0001F3CE\n2:DiplomacyDonutDinghy \U0001F3CE\n3:TeleportingTarteTrolley \U0001F3CE")

        #create a while loop for user to input their option until it is valid
        #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
        #since the user has 3 options only,therefore if user's input is greater than 3 or lower than 1,we will prompt the option is not available
        while True:
            try:
                option = int(input("\U0001F3CE Create your own vehicle by choosing three optional vehicles (e.g. '1'):"))
                if option < 1 or option > 3:
                    print("Option is not available!")
                
                else:
                    #if user's option is 1,ask the user to input the speed of CrappyCrepeCar
                    #create a while loop for user to input their option
                    #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
                    #since both speeds must be positive integer,if user enter negative speed,we will prompt the user to enter again
                    if option == 1:
                        while True:
                            try:
                                speed = int(input("\U0001F3CE Please enter the speed of CrappyCrepeCar:"))
                                if speed < 1:
                                    print("\U0001F3CE Please enter a proper speed of CrappyCrepeCar!")
                                else:
                                    vehicle=CrappyCrepeCar(speed)
                                    break
                            except ValueError:
                                print("Wrong input format ! Please try again "+"\U0001F61E")
                        break
                    
                    #if user's option is 2,ask the user to input the country_speed and primary_speed of DiplomacyDonutDinghy
                    #create 2 while loops,the first while loop is for user to enter the country_speed until it is valid,the second while loop is for user to enter primary_speed until it is valid
                    #try and except is used to identify the input of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
                    #since both speeds must be positive integer,if user enters negative speed,we will prompt the user to enter again
                    elif option == 2:
                        while True:
                            try:
                                country_speed = int(input("\U0001F3CE Please enter the in country speed of DiplomacyDonutDinghy:"))
                                if country_speed < 1:
                                    print("\U0001F3CE Please enter a proper in country speed of DiplomacyDonutDinghy!")
                                else:
                                    while True:
                                        try:
                                            primary_speed = int(input("\U0001F3CE Please enter the between primary speed of DiplomacyDonutDinghy:"))
                                            if primary_speed < 1:
                                                print("\U0001F3CE Please enter a proper between primary speed of DiplomacyDonutDinghy!")
                                            else:
                                                vehicle = DiplomacyDonutDinghy(country_speed,primary_speed)
                                                break
                                        except ValueError:
                                            print("Wrong input format ! Please try again "+"\U0001F61E")
                                    break
                            except ValueError:
                                print("Wrong input format ! Please try again "+"\U0001F61E")
                        break
                    
                    #if user's option is 3,ask the user to input the fixed time and maximum distance of DiplomacyDonutDinghy
                    #create 2 while loops,the first while loop is for user to enter the fixed time until it is valid,the second while loop is for user to enter the maximum distance until it is valid
                    #try and except is used to identify the input of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
                    #since the time and maximum distance must be positive integer,if user enters negative time and maximum distance,we will prompt the user to enter again
                    else:
                        while True:
                            try:
                                time = int(input("\U0001F3CE Please enter the fixed time of TeleportingTarteTrolley:"))
                                if time < 1:
                                    print("\U0001F3CE Please enter a proper time of TeleportingTarteTrolley!")
                                else:
                                    while True:
                                        try:
                                            distance = int(input("\U0001F3CE Please enter the maximum distance of TeleportingTarteTrolley:"))
                                            if distance < 1:
                                                print("\U0001F3CE Please enter a proper maximum distance of TeleportingTarteTrolley!")
                                            else:
                                                vehicle = TeleportingTarteTrolley(time,distance)
                                                break
                                        except ValueError:
                                            print("Wrong input format ! Please try again "+"\U0001F61E")
                                    break      
                            except ValueError:
                                print("Wrong input format ! Please try again "+"\U0001F61E")
                        break
            except ValueError:
                print("Wrong input format ! Please try again "+"\U0001F61E")
        return vehicle

    def example_vehicles(self) -> Vehicle:
        """
        Creates examples of vehicles for user 
        """
        print("------ \U0001F3CE \U0001F3CE Select your vehicle from these three options \U0001F3CE \U0001F3CE------")
        print("1.CrappyCrepeCar with 200 km/h \U0001F3CE\n2:DiplomacyDonutDinghy with 100km/h (in country speed) and 500km/h (between primary speed) \U0001F3CE\n3:TeleportingTarteTrolley with fixed 3 hours within 2000km \U0001F3CE")
        
        #create a while loop for user to input their option until it is valid
        #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
        #since the user has 3 options only,therefore if user's input is greater than 3 or lower than 1,we will prompt the option is not available
        while True:
            try:
                option = int(input("Enter your option:"))
                if option < 1 or option > 3:
                    print("Option is not available!")
                else:

                    #if user's option is 1,the vehicle is CrappyCrepeCar
                    #if user's option is 2,the vehicle is DiplomacyDonutDinghy
                    #if user's option is 3,the vehicle is TeleportingTarteTrolley
                    if option == 1:
                        vehicle = CrappyCrepeCar(200)
                        break
                    elif option == 2:
                        vehicle = DiplomacyDonutDinghy(100, 500)
                        break
                    else:
                        vehicle = TeleportingTarteTrolley(3, 2000)
                        break
            except ValueError:
                print("Wrong input format ! Please try again "+"\U0001F61E")
        return vehicle
    
    def example_trips(self) -> 'list[Trip]':
        """
        Creates examples trips for user.
        """
        create_example_countries_and_cities()
        
        australia = Country.countries["Australia"]
        melbourne = australia.get_city("Melbourne")
        sydney = australia.get_city("Sydney")
        canberra = australia.get_city("Canberra")
        japan = Country.countries["Japan"]
        tokyo = japan.get_city("Tokyo")
        print("1.Melbourne -> Sydney\n2.Canberra -> Tokyo\n3.Melbourne -> Canberra -> Tokyo\n4.Canberra -> Melbourne -> Tokyo")
        
        #create a while loop for user to input their option until it is valid
        #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
        #since the user has 4 options only,therefore if user's input is greater than 4 or lower than 1,we will prompt the option is not available
        while True:
            try:
                option = int(input("\N{slightly smiling face}"+"Please select your trip from the example trips :"))
                if option < 1 or option > 4:
                    print("Option is not available!")
                else:
                    #if their option is 1, the trip is from Melbourne to Sydney
                    #if their option is 2, the trip is from Canberra to Tokyo
                    #if their option is 3, the trip is from Melbourne to Sydney to Tokyo
                    #if their option is 4, the trip is from Canberra to Melbourne to Tokyo
                    if option == 1:
                        trip = Trip(melbourne)
                        trip.add_next_city(sydney)
                        break
                    elif option == 2:
                        trip = Trip(canberra)
                        trip.add_next_city(tokyo)
                        break
                    elif option == 3:
                        trip = Trip(melbourne)
                        trip.add_next_city(canberra)
                        trip.add_next_city(tokyo)
                        break
                    else:
                        trip = Trip(canberra)
                        trip.add_next_city(melbourne)
                        trip.add_next_city(tokyo)
                        break                       
            except ValueError:
                print("Wrong input format ! Please try again \U0001F61E")
        #print the statement of their chosen trip
        print("Your trip is: "+str(trip))
        return trip

    def manually_create_trip(self):
        """
        This function is created for user to create the trip manually
        """
        #create an empty list named travel to store the cities enter by user
        #create a while loop for user to enter the city until it is valid
        travel = []
        while True:
            found = True 
            #assign a variable named journey,which is a list to store the cities entered by user
            #since user must enter at leat 2 cities,so when the length of journey is lower than 2,we will prompt the user to enter again
            journey = list(map(str,input("Please select your preferred cities in your trip (e.g. Melbourne,Sydney,Bangkok ):").split(',')))
            if len(journey) < 2:
                print("Please create a trip with at least two cities!")
            else:
                #this for loop will loop through each city in the journey
                #if the city entered by user is not in the file,we will break this for loop
                for city in journey: 
                    if not found:
                        break
                    #create a variable named found_city,and initialise it is None 
                    #this for loop will run through the items in cities dictionary
                    #if the name of city(value) in file is equal to the city entered by user
                    #we store the key into found_city,and break this for loop
                    found_city=None
                    for x,y in City.cities.items():
                        if y.name.lower() == city.lower():
                            found_city = City.cities[x]
                            break
                    #if we found the city entered by user is same as the cities in the file,we append the cities into travel
                    #otherwise we will prompt the user that the city is not occur
                    #in here we need to clear the elments in travel because the trip is impossible since there is a city not occur in file
                    if found_city:
                        travel.append(found_city)
                    else:
                        found = False
                        print(city+" is not occur...\U0001F61E")  
                        travel.clear()
                #if the city entered by user is same as the city in the file  
                #we first create a variable named trip to store the first city entered by user  
                #and create a for loop to run through the other cities excluding the first city,and call the function add_next_city in the class of trip to add the remaining cities
                #and print the statement to let user know the each city in user's trip
                #if the city entered by user is not same as the city in the file,we will prompt the user to enter again
                if found:
                    trip = Trip(travel[0])
                    for city in travel[1:]:
                        trip.add_next_city(city)
                    print("Your trip is: "+str(trip))
                    return trip
                else:
                    print("Please enter again!")    

    def shortest_path_trip(self):
        """
        This method is to find the shortest path of a trip for given Vehicle
        """
        #since we want the user to input 2 cities,and check these two cities are occur or not in the file
        #so we create 2 while loops,the first while loop is for user to enter the departure city until it is valid,the second while loop is for user to enter arrival city until it is valid
        #if the departure city and arrival city entered by user is not in the city in the file,we will prompt the user to enter again
        #we create a variable named found_departure to match the same city in the file,first we assign it into None,because we have not started checking the city 
        #if the departure city entered by user is valid,we create another variable named arrival city to match the same city in the file,and assign it into None since we have not started checking the city
        while True:
            departure_city = input("Please select your departure city in your trip (e.g. Melbourne):")
            found_departure=None
            for x,y in City.cities.items():
                if y.name.lower() == departure_city.lower():
                    found_departure = City.cities[x]
                    break
            if found_departure:
                while True:
                    arrival_city = input("Please select your arrival city in your trip (e.g. Melbourne):")
                    found_arrival=None
                    for x,y in City.cities.items():
                        if y.name.lower() == arrival_city.lower():
                            found_arrival = City.cities[x]
                            break
                    
                    #if both departure city and arrival city are valid,we create an empty list named possible_trip_lst to store the shortest path of these 2 cities
                    #this for loop will run through with the number of vehicles in the self.fleet,because we need to check the shortest path by using each vehicle
                    #create a variable named path to store the shortest path of between these 2 cities by using each vehicles in self.fleet,and then append the path into possible_trip_lst
                    if found_arrival:
                        possible_trip_lst=[]
                        for vehicle in range(len(self.fleet)):
                            path = find_shortest_path(self.fleet[vehicle],found_departure,found_arrival)
                            possible_trip_lst.append(path)
                            print("Shortest path of trip for vehicle \U0001F3CE",vehicle+1,":",path)
                        
                        #create a while loop for user to select the option until it is valid
                        #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
                        #if the user's option is below 1 or greater than the length of self.fleet,we will prompt the user to enter again
                        #because how many vehicles in the self.fleet means how many shortest path,therefore the user's option cannot greater than the length of self.fleet
                        while True:
                            try:
                                final_trip = int(input("Please select one trip:"))
                                if final_trip < 1 or final_trip > len(self.fleet):
                                    print("Trip is not available")
                                else:
                                    break
                            except ValueError:
                                print("Wrong input format ! Please try again \U0001F61E")
                        trip = possible_trip_lst[final_trip - 1]
                        print("Your trip is: "+str(trip))
                        return trip
                    else:
                        print(arrival_city + " is not occur...\U0001F61E\nPlease enter again!")
            else:
                print(departure_city + " is not occur...\U0001F61E\nPlease enter again!")
        
    def main_menu(self):
        while True:
            print("-----------------Main Menu------------------")
            print("                                            ")
            print("\N{slightly smiling face}   ♥ Welcome to ICE LATTE Adventure ♥   \N{slightly smiling face}")
            print("                                            ")
            print("--------------------------------------------")
            print("✈️ ✈️ Let's start our journey! ✈️ ✈️")
            print("1. Vehicle customization \U0001F3CE\n2. Trip customization\n3. Find fastest vehicle for trip \U0001F3CE\n4. Trip map plotting\n5. Trip simulation\n6. History\n7. Restart\n8. Exit\n\n")
            
            #create a while loop for user to select the option until it is valid
            #try and except is used to identify the option of user is valid or not,if the input is not integer, we will prompt the user to wrong input format and input again
            #if the user's option is 1,call the function self.vehicle_customization to let user customize vehicles
            #if the user's option is 2,call the function self.trip_customization to let user customize trip 
            #if the user's option is 3,call the function self.trip_fastest_vehicle to let user know the fastest vehicle in the trip 
            #if the user's option is 4,call the function self.trip_map_plotting to plot the map of user's trip
            #if the user's option is 5,call the function self.trip_simulation to simulate the trip 
            #if the user's option is 6,call the function self.history to know the search history
            while True:
                try:
                    option = int(input("Enter your option:"))
                    if option < 1 or option > 8:
                        print("Option is not available!")
                    elif option == 1:
                        self.vehicle_customization()
                        back = input("Press any key then press enter to go back to main menu")
                        if back:
                            break
                    elif option == 2:
                        self.trip_customization()
                        back = input("Press any key then press enter to go back to main menu")
                        if back:
                            break
                    elif option == 3:
                        self.trip_fastest_vehicle()
                        back = input("Press any key then press enter to go back to main menu")
                        if back:
                            break
                    elif option == 4:
                        self.trip_map_plotting()
                        back = input("Press any key then press enter to go back to main menu")
                        if back:
                            break
                    elif option == 5:
                        self.trip_simulation()
                        back = input("Press any key then press enter to go back to main menu")
                        if back:
                            break
                    elif option == 6:
                        self.history()
                        back = input("Press any key then press enter to go back to main menu")
                        if back:
                            break
                    elif option == 7:
                        self.restart()
                        time.sleep(1)
                        break
                    else:
                        break
                except ValueError:
                    print("Wrong input format ! Please try again "+"\U0001F61E")
            if option == 8:
                break


if __name__ == "__main__":
    Navigation()
        

