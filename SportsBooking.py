#latest file as of 09/12/2022

import re
import copy
class Create_Lists:
    #reads a facilities file and returns a list of the facilities
    def read_facilities_file(filename: str):
        #create a file to return to user
        file_list = []
        with open(filename, "r") as r_file:
            for line in r_file:
                #use regex to remove/replace unnecessary chars
                result = re.sub(r'[^a-zA-Z\d\s:]', "", line)
                #strip of whitespace chars
                result = result.strip()
                #append the line to the list
                file_list.append(result)

            return file_list

    #reads a sessions file and returns a list of dictionaries of the sessions
    def read_sessions_file(filename: str):
        #this list holds the dictionaries
        sessions_list = []
        #a temporary dictionary for holding values
        temp_dict = {}
        with open(filename,"r") as r_file:
            #read first line to get headings
            list_of_headings = r_file.readline().split(",")
            #comprehension with regex to remove/sub unnecessary chars in a pythonic manner
            headings_list = [re.sub(r'[^a-zA-Z :]', "", piece) for piece in list_of_headings]

            for line in r_file:
                #strip line in read file of unnecessary chars
                line = line.strip()
                #split the string into a temporary list based on ,
                t_list = line.split(",")
                #create a temp dict using headings as keys and t_list values for dict values
                temp_dict[headings_list[0]] = t_list[0]
                temp_dict[headings_list[1]] = int(t_list[1])
                temp_dict[headings_list[2]] = int(t_list[2])
                
                #append the temporary dictionary to the overarching list
                sessions_list.append(temp_dict)
                #reset temp_dict
                temp_dict = {}

        return sessions_list

    #returns facilities class list
    def merging_facilities_sessions(facilities: list, sessions: list):
        classes_list = []
        facility_list = []
        #first merge the facilities and sessions
        for section in sessions:
            #print(section["Facility id"])
            if section["Facility id"] == 0:
                section["FacilityName"] = facilities[0]
            elif section["Facility id"] == 1:
                section["FacilityName"] = facilities[1]
            elif section["Facility id"] == 2:
                section["FacilityName"] = facilities[2]
            else:
                print("error")

        #in this part create a list of Facility objects
        for section in sessions:
            if "Swimming Lane" in section["FacilityName"]:
                session = Swimming_Session(section["Session name"], section["Available places"], Facility(section["FacilityName"], section["Facility id"]), 0)
            else:
                session = Squash_Session(section["Session name"], section["Available places"], Facility(section["FacilityName"], section["Facility id"]), 0)
            facility = Facility(section["FacilityName"], section["Facility id"])
            if facility not in facility_list:
                facility_list.append(facility)
            classes_list.append(session)

        return classes_list, facility_list

#Facility Class
class Facility:
    def __init__(self, facility_name: str, facility_id: int):
        self._facility_name = facility_name
        self._facility_id = facility_id
    
    def get_id(self):
        return self._facility_id
    
    def get_name(self):
        return self._facility_name

    def set_name(self, name):
        self._facility_name = name

    def __eq__(self, other):
        return self._facility_name == other._facility_name and self._facility_id == other._facility_id
        
    def __repr__(self):
        return f"Facility ID: {self._facility_id}, Facility Name: {self._facility_name}"

#super class to Swimming & Squash Session classes
class Session:
    #important to note that Sessions contain the facilities within their classes.
    def __init__(self, sesh_name: str, places: int, facility: Facility, price: float):
        self._sesh_name = sesh_name
        self._places = places
        self._facility = facility
        self._price = price

    #getter and setter for facility
    def get_facility(self):
        return self._facility 
    def set_facility(self, facility: Facility):
        self._facility = facility

    #getter and setter for price
    def get_price(self):
        return self._price
    def set_price(self, price: float):
        self._price = price

    #getter and setter for name
    def get_name(self):
        return self._sesh_name

    def set_name(self, name: str):
        self._sesh_name = name

    #getter and setter for places
    def get_places(self):
        return self._places

    def set_places(self, places:int):
        self._places = places

    def __repr__(self):
        return f"Session Name: {self._sesh_name} Available Places: {self._places} Facility ID: {self._facility.get_id()} Facility Name: {self._facility.get_name()}"


class Swimming_Session(Session):
    def __init__(self, sesh_name: str, places: int, facility: Facility, price: int):
        super().__init__(sesh_name, places, facility, 0)
        #default price is 10 euros
        self._price = float(10)

    #if places given are higher than 3, price is 0.8 x
    def get_price(self, places: int):
        if places >= 4:
            return self._price * 0.8
        return self._price
    

class Squash_Session(Session):
    def __init__(self, sesh_name: str, places: int, facility: Facility, price: int):
        super().__init__(sesh_name,places,facility, 0)
        #default price is 8 euros
        self._price = float(8)

    #if places given higher than price = 0.9 x 
    def get_price(self, places: int):
        if places > 2:
            return self._price * 0.9

        return self._price

    
class Facility_Handler:
    _facility_list = []
    _session_list = []
    _basket_list = []
    def __init__(self,facility_list: list, session_list:list):
        self._facility_list = facility_list
        self._session_list = session_list
    
    def get_facility_list(self):
        return self._facility_list

    def get_session_list(self):
        return self._session_list

    def get_basket_list(self):
        return self._basket_list

    #semi private function
    #searches through a list based on name and if .get name matches name string, returns index position
    #most searches will use indexes instead, so use case is narrow.
    def search_list(self, name:str, list_to_search: list):
        #default index is -1
        index = -1
        for i in range(len(list_to_search)):
            if list_to_search[i].get_name() == name:
                index = i
        return index

    #part 0, displays facilities listings
    def display_facilities(self):
        for i in range(len(self._facility_list)):
            print(self._facility_list[i])

    #part 1 of document
    #display all the sessions available to the user based on sessions_listing required.
    #sessions are still displayed even if 0 places are available
    def display_sessions(self):
        print(f"Index\t FacilityName\tSession Name\tSession Places Left")
        for i in range(len(self._session_list)):
            print(f"{i}\t{self._session_list[i].get_facility().get_name()}\t{self._session_list[i].get_name()}\t{self._session_list[i].get_places()}")

    #part 2 of document
    #add a facility to the facility list
    #ONLY USED IN ADMIN FUNCTIONALITY
    def add_facility(self, facility: Facility):
        self._facility_list.append(facility)

    #part 3 of document
    #add a session to the sessions list
    #ONLY USED IN ADMIN FUNCTIONALITY
    def add_session(self, session: Session):
        self._session_list.append(session)

    #part 4 of document
    #ONLY USED IN ADMIN FUNCTIONALITY
    def change_facility_name(self, new_name:str, original_id: int):
        found_facility = False
        try:
            self._facility_list = [Facility(new_name, facility.get_id()) if facility.get_id() == original_id else facility for facility in self._facility_list]
            for part in self._session_list:
                if part.get_facility().get_id() == original_id:
                    part.get_facility().set_name(new_name)
                    found_facility = True
            if not found_facility:
                print("Cannot find facility.")

        except IndexError: print(f"Index out of bounds")
        except ValueError: print("Index must be integer.")

    #part 5 of document
    #ONLY USED IN ADMIN FUNCTIONALITY
    def change_session_name(self, new_name:str, index: int):
        #index = self.search_list(index, self._session_list)
        try:
            self._session_list[index].set_name(new_name)

        except IndexError: print(f"Index {index} out of bounds")
        except ValueError: print("Index must be integer.")


    #part 6 of document
    #ONLY USED IN ADMIN FUNCTIONALITY
    def change_number_of_places(self, places: int, index: int):
        try:
            self._session_list[index].set_places(places)
        except IndexError: print(f"Index {index} out of bounds")
        except ValueError: print("Values must be integer.")


    #part 7 of document
    def change_session_facility_link(self, facility_name: str, index:int):
        try:
            self._session_list[index].get_facility().set_name(facility_name)
        except IndexError: print(f"Index out of range")
        except ValueError: print("Index must be integer")

    #part 8
    #ONLY USED IN ADMIN FUNCTIONALITY
    def delete_facility(self, facility_id: int):
        index = -1
        self.temp_list = copy.deepcopy(self._basket_list)

        for i in range(len(self._facility_list)):
            if self._facility_list[i].get_id() == facility_id:
                index = i
        if index != -1:
            self._facility_list.pop(index)
            self._session_list = [session for session in self._session_list if session.get_facility().get_id() != facility_id]
            self._basket_list = [session for session in self._basket_list if session.get_facility().get_id() != facility_id]
        else:
            print("That facility was not found")

    #part 9 of document
    #deletes a session from the session listing
    #ONLY USED IN ADMIN FUNCTIONALITY
    def delete_session(self, index: int):
        self.temp_list = copy.deepcopy(self._basket_list)
        try:
            session_name = self._session_list[index].get_name()
            self._session_list.pop(index)

            for i in range(len(self.temp_list)):
                if self.temp_list[i].get_name() == session_name:
                    self._basket_list.pop(i)

        except IndexError: print(f"Index {index} out of bounds")
        except ValueError: print("Index must be integer.")
    
    #part 10 of document
    #adds a unique item to basket
    def add_to_basket(self, index:int, places: int):
        try:
            #verify if item already exists in basket
            item_exists = self._verify_basket_item_exists(self._session_list[index].get_name())
            #if item does not exist
            if not item_exists:
                #verify that there is enough places available
                if self._session_list[index].get_places() - places >= 0:
                    #take places away from session list
                    self._session_list[index].set_places(self._session_list[index].get_places() - places)
                    #create a deepcopy of the object to add to basket list
                    session_to_add = copy.deepcopy(self._session_list[index])
                    #set the places in the basket object to places integer
                    session_to_add.set_places(places)
                    #append the new session to the basket
                    self._basket_list.append(session_to_add)
                    print("Successfully added to basket.")
                else:
                    print("I'm sorry, not enough places available.")
            else:
                #if item already exists in basket, no need to add it again.
                print("That item already exists in the basket, use modify functionality instead.")
                print()

        except IndexError: print(f"Index {index} out of bounds")
        except ValueError: print("Index must be integer.")

        

    #part 11 of document
    #Only applicable to swim session menu
    def basket_modify_number_of_places(self, index: int, new_places: int):
        try:
            #get the session name
            #this makes sure that the sessions in both basket and session list are correct
            session_name = self._basket_list[index].get_name()

            #find the basket places within the basket list
            current_basket_places = self._basket_list[index].get_places()
            #get the index position of the search list item
            index_sessions = self.search_list(session_name, self._session_list)
            if new_places > 0:
                #check to see how many places are left
                places_left = self._session_list[index_sessions].get_places()
                #if the basket places are greater than the new places to set:
                if current_basket_places > new_places:
                    #set the basket list to the new place amount
                    self._basket_list[index].set_places(new_places)
                    
                    #add the difference of places between new and old basket item places
                    self._session_list[index_sessions].set_places(self._session_list[index_sessions].get_places() + (current_basket_places - new_places))
                #else if the new places will be greater than old basket item places
                elif current_basket_places < new_places:
                    #stops user from going over the max allotted places available
                    if current_basket_places + places_left < new_places:
                        print("Not enough places available")
                    else:
                        #the basket list item places will be set to the new place amount
                        self._basket_list[index].set_places(new_places)
                        #the difference of places between new and old basket list item will be added to the sessions list.
                        self._session_list[index_sessions].set_places(self._session_list[index_sessions].get_places() - (new_places - current_basket_places))
            else:
                print("Places to set must be greater than 0")
        except IndexError: print(f"Index {index} out of bounds")
        except ValueError: print("Index must be integer.")


    #part 12 of document
    #calculate the total based on places and sessions
    def calculate_basket_total(self):
        total = 0
        total_places = 0
        for value in self._basket_list:
            #find the total number of places used in basket
            total_places += value.get_places()
        for value in self._basket_list:
            #total equals the number of places & value of the object
            total += value.get_places() * value.get_price(total_places)
        return total

    #part 13 of document
    def clear_basket(self):
        #clears the basket and adds back the number of places taken out back into sessions list
        for value in self._basket_list:
            places = value.get_places()
            index = self.search_list(value.get_name(), self._session_list)
            self._session_list[index].set_places(self._session_list[index].get_places() + places)

        self._basket_list.clear()

    #part 14 of document
    def display_basket(self):
        print("ID\tFacility Name\tSession Name\tPlaces required")

        #if user has an empty basket
        if len(self.get_basket_list()) < 1:
            print("EMPTY BASKET")
        else:
            #otherwise display all items in basket
            for i in range(len(self._basket_list)):
                print(f"{i}\t{self._basket_list[i].get_facility().get_name()}\t{self._basket_list[i].get_name()}\t{self._basket_list[i].get_places()}")

    #part 15 of document
    #remove a session from the basket
    def delete_from_basket(self, index:int ):
        
        try:
            #get the name of the session user has taken out
            session_name = self._basket_list[index].get_name()
            #get index of the sessions list basket item
            index_sessions = self.search_list(session_name, self._session_list)
            #find number of places used
            places = self._basket_list[index].get_places()
            #add back in the places that the user has taken out, back into the sessions listing
            self._session_list[index_sessions].set_places(self._session_list[index_sessions].get_places() + places)
            #pop the basket item from list
            self._basket_list.pop(index)

        except IndexError: print(f"Index {index} out of bounds")
        except ValueError: print("Index must be integer.")

    #removes all purchases from basket
    # no need to add back to sessions list
    def clear_basket_after_purchase(self):
        self._basket_list.clear()

    #private method to verify if a basket item already exists in object
    #this to prevent user adding multiples of a given session to a basket with different IDs
    def _verify_basket_item_exists(self, name: str):
        for item in self._basket_list:
            if item.get_name() == name:
                return True
        return False

    
class SportsBooking:
    def __init__(self):
        #this means user does not need to handle any of the .csv files, they are worked with automatically and hidden from user
        self._facility_handler = Facility_Handler(facility_list=[],session_list=[])
        self._squash_facilities = Create_Lists.read_facilities_file("squash_facilities.csv")
        self._swimming_facilities = Create_Lists.read_facilities_file("swimming_facilities.csv")
        self._swimming_sessions = Create_Lists.read_sessions_file("swimming_sessions.csv")
        self._squash_sessions = Create_Lists.read_sessions_file("squash_sessions.csv")
        #we merge the lists and use the "Facility" & "Sessions" object classes for the lists
        self._squash_sessions_list, self._squash_facilities = Create_Lists.merging_facilities_sessions(facilities=self._squash_facilities, sessions=self._squash_sessions)
        self._swimming_sessions_list, self._swimming_facilities = Create_Lists.merging_facilities_sessions(facilities=self._swimming_facilities, sessions=self._swimming_sessions)

    #depending on which option the user picks, the Facility Handler object is either using a Squash or Swimming Sessions list
    def instantiate_facility_handler(self, facilities_list: list, sessions_list: list):
        self._facility_handler = Facility_Handler(facility_list=facilities_list, session_list=sessions_list)

    #this allows the user to view error and confirmation messages before the menu is called again
    def confirmation_message(self):
        await_user = input("Press any key to continue....")
        print()

    #this is the primary menu called when the user starts up the sportsbooking app
    def primary_menu(self):
        show_menu=True
        while(show_menu):
            print("PRIMARY MENU")
            print("1. Book Swimming Menu")
            print("2 - Booking Squash Menu")
            print("0 - Quit System")
            try:
                option = int(input("What is your option? "))
                #user quits
                if option == 0:
                    print("Good bye")
                    show_menu = False

                #user instantiates swimming lists 
                elif option == 1:
                    show_menu = False
                    self.instantiate_facility_handler(self._swimming_facilities, self._swimming_sessions_list)
                    self.swimming_menu()
                #user instantiates squash lists
                elif option == 2:
                    show_menu = False
                    self.instantiate_facility_handler(self._squash_facilities, self._squash_sessions_list)
                    self.squash_menu()
                #if user enters in another number
                elif option > 2 or option < 0:
                    print("Please enter number: [0-2]")
                else:
                    self.calculate_menu(option)
                        #break
            #if user enters in something other than int
            except ValueError:
                print("Please enter number: [0-2]")

    #squash menu called
    def squash_menu(self):
        display_menu = True
        
        while(display_menu):
            
            
            self.display_sessions()
            print()
            self.display_basket()
            print()

            print("SQUASH ADMIN MENU")
            print("1. Add a squash session to the basket (2 places only booked at a time)")
            print("2. Pay")
            print("3. Remove the squash session from the basket")
            print("4. Return to previous menu")
           
            try: 
                option = int(input("What option will you select: "))

                if option == 1:
                    #send true as object is squash
                    # will always use 2 places  
                    self.add_session_basket(True)
                    self.confirmation_message()
                elif option == 2:
                    #user activates pay functionality
                    #will only work if items in basket exist
                    self._pay()
                    self.confirmation_message()
                elif option == 3:
                    #will activate removal functionality
                    #will only work if there are items in basket
                    self.basket_delete_session()
                    self.confirmation_message()
                    #will revert to previous menu
                elif option == 4:
                    display_menu = False
                    #this clears out basket and adds back into list as user has not finalized purchase
                    self.clear_basket()
                    #calls the main menu
                    self.primary_menu()
                #calls if user has entered in wrong number
                elif option > 4 or option < 1:
                    print("Please enter number: [1-4]")
                    self.confirmation_message()
            except ValueError:
                print("Please enter number: [1-4]")
                self.confirmation_message()

    #swimming menu - handles swimming objects
    def swimming_menu(self):
        display_menu = True
        
        while(display_menu):
            self.display_sessions()
            print()
            self.display_basket()
            print()
            print("SWIMMING ADMIN MENU")
            print("1. Add session to basket.")
            print("2. Modify swimming session places in basket.")
            print("3. Pay")
            print("4. Remove session from basket")
            print("5. Return to previous menu")
            
            try: 
                option = int(input("What option will you select: "))

                if option == 1:
                    #send false, this will mean user can add places based on need
                    #must be unique session item
                    self.add_session_basket(False)
                    self.confirmation_message()
                elif option == 2:
                    #change the number of places for a given basket item
                    self.change_basket_item_places()
                    self.confirmation_message()
                elif option == 3:
                    #calls pay functionality
                    self._pay()
                    self.confirmation_message()
                elif option == 4:
                    #delete an item from the users basket
                    self.basket_delete_session()
                    self.confirmation_message()
                #will revert to previous menu
                elif option == 5:
                    #clear the basket and add back in places to the sessions listing
                    self.clear_basket()
                    display_menu = False
                    self.primary_menu()
                #user enters in incorrect number
                elif option > 5 or option < 1:
                    print("Please enter number: [1-5]")
                    self.confirmation_message()
            except ValueError:
                print("Please enter number: [1-5]")
                self.confirmation_message()

    #this functionality is entirely for administration
    #TODO - verify that all functionality here works
    #TODO - function 7 needs to work
    def admin_menu(self, sessions_list: list, facility_list: list):

        self.instantiate_facility_handler(facility_list, sessions_list)

        while(True):
            print("Administration Menu")
            print("0. Display Facilities")
            print("1. Display Sessions")
            print("2. Add Facility")
            print("3. Add Session")
            print("4. Modify Facility Name")
            print("5. Modify Session Name")
            print("6. Modify Number of Spaces in a Session")
            print("7. Modify Session & Facility Link")
            print("8. Delete Facility (Removes all basket/session)")
            print("9. Delete Session (Removes from basket/sessions)")
            print("10. Add Session to Basket")
            print("11. Modify basket item's number of places")
            print("12. Calculate basket total")
            print("13. Clear Basket")
            print("14. Display Basket")
            print("15. Delete item from Basket")
            print("16. Quit System.")
            
            try:
                option = int(input("What is your option?"))

                if option == 16:
                    print("Good bye")
                    break
                elif option > 16 or option < 0:
                    print("Please enter number: [0-16]")
                else:
                    self.calculate_menu(option)
                    self.confirmation_message()
                        
            except ValueError:
                print("Please enter number: [0-16]")

    #this calls the various admin menu functions
    def calculate_menu(self, option: int):
        if option == 0:
            self.display_facilities()
        elif option == 1:
            self.display_sessions()
        elif option == 2:
            self.add_facility()
        elif option == 3:
            self.add_session()
        elif option == 4:
            self.change_facility_name()
        elif option == 5:
            self.change_session_name()
        elif option == 6:
            self.change_session_places()
        elif option == 7:
            self.change_session_facility_link()
        elif option == 8:
            self.delete_facility()
        elif option == 9:
            self.delete_session()
        elif option == 10:
            self.add_session_basket(False)
        elif option == 11:
            self.change_basket_item_places()
        elif option == 12:
            self._pay()
        elif option == 13:
            self.clear_basket()
        elif option == 14:
            self.display_basket()
        elif option == 15:
            self.basket_delete_session()

    #private method that allows the user to finalize basket items purchases
    def _pay(self):
        #if basket is empty
        #carry out no functionality
        if len(self._facility_handler.get_basket_list()) < 1:
            print("Sorry, your basket is empty")
            print()
        else:
            #find the total of the basket
            total = self.calculate_total()
            #print formatted total
            print(f"Your total is {total:.2f}")

            #get confirmation of purchase
            confirm = input(f"Do you wish to confirm your purchase?[y or n]").lower()
            #if user enters invalid input, continue loop
            while(True):
                if confirm == "y" or confirm =="yes":
                    print(f"You have purchased the goods, thank you.")
                    #empties basket of items and does not add places back into sessions
                    self._facility_handler.clear_basket_after_purchase()
                    break
                elif confirm == "n" or confirm == "no":
                    print(f"No problem... take your time.")
                    break
                else:
                    print("I do not recognise that input. [y or n]")

    ##Important functionality below!
    ##All functions below use Facility_Handler functionality and then add more functionality on top
    ##For example, get user input from keyboard and use it to access functionality in facility handler
    ##By separating functionality like this, it makes the code easier to understand and read.

    #option 1 - displays facilities list
    def display_facilities(self):
        self._facility_handler.display_facilities()


    #option 1 - display sessions
    #calls facility handler display sessions
    def display_sessions(self):
        self._facility_handler.display_sessions()

    #option 2 - Add facility
    #get user input for facility and add that facility to the facility list
    #TODO - Verify this works
    def add_facility(self):
        facility_name = input("Please give the name of the facility you wish to add")

        self._facility_handler.add_facility(facility_name)

    #option 3 - add session
    #TODO - Change facility list too
    #adds a session based on user list to facility handler
    def add_session(self):
        session_name = input("Please enter name of session: ")
        places = input("Enter number of places: ")
        facility_name = input("Enter the name of the facility session is attached to: ")
        facility_id = input("Enter facility id: ")

        #for testing purposes all sessions will be swimming
        temp_session = Swimming_Session(session_name,places, Facility(facility_name, facility_id))

        self._facility_handler.add_session(temp_session)

    #option 4 - modify facility name
    #get facility name and id based on user input
    def change_facility_name(self):
        facility_id = int(input("Please enter ID of Facility to change: "))
        new_name  = input("What is the new name? ")
        self._facility_handler.change_facility_name(new_name=new_name, original_id=facility_id)

    #option 5 - modify session name
    #change session name based on user input in facility handler
    def change_session_name(self):
        index = int(input("Please enter index of session to edit: "))
        name = input("Please enter new name: ")
        self._facility_handler.change_session_name(name, index)

    #option 6 - modify session places
    #change the number of sessions places within sessions list based on user input
    def change_session_places(self):
        index = int(input("Please enter index of session to edit: "))
        places = int(input("Please enter modified number of places: "))

        self._facility_handler.change_number_of_places(places, index)

    #option 7 - modify... thing
    def change_session_facility_link(self):
        index = int(input("Please enter index of session to edit"))
        facility_name = input("Please enter the new name of the facility that links to this session")

        self._facility_handler.change_session_facility_link(facility_name, index)

    #option 8 - delete facility
    #deleete a facility based on user input
    def delete_facility(self):
        facility_id = int(input("Enter the facility id of the facility to delete: "))
        self._facility_handler.delete_facility(facility_id)

    #option 9 - delete session
    #delete a session from the list based on user input
    def delete_session(self):
        index = int(input("Enter index position of session to delete: "))
        self._facility_handler.delete_session(index)

    #option 10 - Add session to basket
    #add a session to the basket based on user input via menu
    def add_session_basket(self, is_squash: bool):
        try:
            #get index position of the session within session list
            index = int(input("Enter index position of session to be added to basket: "))
            #if its not squash you can get user input for number of places
            if not is_squash:
                places = int(input("Please enter quantity of places required: "))
        #if its a squash session, default to 2.
            else:
                places = 2
            if places > 0 and index >= 0:
                self._facility_handler.add_to_basket(index, places)
            elif index < 0:
                print("Index value must be positive...")
            elif places <= 0:
                print("Places purchased must be at least 1.")

        except ValueError: print("Places & index must be integers.")
        except IndexError: print(f"Index {index} out of bounds.")
    
    #option 11 - Modify basket item's quantity
    #modify the number of places that the user wants in their basket
    #most functionality here is all about the front end to user
    def change_basket_item_places(self):
        #if the length of the basket list is less than 1, can't access this functionality
        if len(self._facility_handler.get_basket_list()) < 1:
            print("Sorry, your basket is empty")
            print()
        else:
            index = int(input("Enter index position of session in basket: "))
            places = int(input("Enter modified quantity of places: "))
            #activate the facility handlers modify places within basket
            self._facility_handler.basket_modify_number_of_places(index=index, new_places=places)

    #option 12 - calculate total
    #call the facility handlers calculate basket total
    def calculate_total(self):
        return self._facility_handler.calculate_basket_total()

    #option 13 - Clear basket
    #call the facility handler's clear basket
    def clear_basket(self):
        self._facility_handler.clear_basket()

    #option 14 - display basket
    #display all items in basket
    def display_basket(self):
        self._facility_handler.display_basket()

    #option 15 - delete item from basket
    #delete an item from the basket
    #note this handles mostly user input
    #TODO - need to get better error handling for this
    def basket_delete_session(self):
        if len(self._facility_handler.get_basket_list()) < 1:
            print("Sorry, your basket is empty")
            print()
        else:
            index = int(input("Enter index position of session in basket: "))
            self._facility_handler.delete_from_basket(index)
            print("Basket item deleted.")
