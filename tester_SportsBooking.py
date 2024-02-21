from SportsBooking import *
if __name__ == "__main__":

    #testing Sessions parent class functionality
    t_facility = Facility(facility_name="Tennis Court 1", facility_id=0)
    tennis_session = Session(sesh_name="S1__13_11_2022__8-9__SL1", places=10, facility=t_facility,price=10.00)

    #print tennis_session
    print(tennis_session)
    print()

    #set and get facility
    tennis_session.set_facility(Facility("Tennis Court 2", 1))
    print(f"Facility: {tennis_session.get_facility()}")


    #set and get price
    tennis_session.set_price(5)
    print(f"Price: {tennis_session.get_price()}")

    #set and get places
    tennis_session.set_places(5)
    print(f"Places: {tennis_session.get_places()}")

    #set and get session name
    tennis_session.set_name("S2__12_11_2023__9-10__SL2")
    print(f"Session name: {tennis_session.get_name()}")
    print()

    #print new tennis session string representation
    print(tennis_session)


    continue_via_keyboard=input("Press any key to continue...")

    #for the admin menu below it will use these lists
    #this means user does not need to handle any of the .csv files, they are worked with automatically and hidden from user
    facility_handler = Facility_Handler(facility_list=[],session_list=[])
    squash_facilities = Create_Lists.read_facilities_file("squash_facilities.csv")
    swimming_facilities = Create_Lists.read_facilities_file("swimming_facilities.csv")
    swimming_sessions = Create_Lists.read_sessions_file("swimming_sessions.csv")
    squash_sessions = Create_Lists.read_sessions_file("squash_sessions.csv")
    #we merge the lists and use the "Facility" & "Sessions" object classes for the lists
    squash_sessions_list, squash_facilities = Create_Lists.merging_facilities_sessions(facilities=squash_facilities, sessions=squash_sessions)
    swimming_sessions_list, swimming_facilities = Create_Lists.merging_facilities_sessions(facilities=swimming_facilities, sessions=swimming_sessions)

    #create sports booking object
    sports_booking = SportsBooking()

    #for purposes of testing, first, the swimming sessions + facilities list will be used
    #please run this to see 16 pieces of functionality as described in the CA3 pdf. 
    #I thought this would be a neater way of creating the tester class
    print("SWIMMING ADMIN MENU")
    sports_booking.admin_menu(swimming_sessions_list, swimming_facilities)
    print()
    print()
    print()

    #secondly, this will show the admin functionality of the squash sessions class
    print("SQUASH ADMIN MENU")
    sports_booking.admin_menu(squash_sessions_list, squash_facilities)
    print()
    print()
    print()


    #to see main menu functionality, either comment out or quit the admin menu call up above
    #this functionality has swimming and squash lists
    sports_booking.primary_menu()