import os
import sys
from route import assign_routes
from package import package_hashtable
from deliver import begin_deliveries
from deliver import first_status_check
from deliver import second_status_check
from deliver import delivery_status_check


def start_menu():
    os.system('cls||clear')
    print('  WGUPS DLD ROUTE MANAGEMENT SYSTEM \n')
    print('        START MENU OPTIONS \n')
    print('(1)-LOAD PACKAGE FILE & VIEW ALL PACKAGES IN INVENTORY  \n')
    print('(2)-BEGIN DAILY DELIVERIES & SEE ALL PACKAGE DATA AT FINAL TIME(EOD) \n')
    print('(0)-EXIT SYSTEM \n')
    try:
        user_selection = int(input('Please Select An Option From The Start Menu: '))
    except ValueError:
        print('Invalid Option Selected. System Will Now Exit.')
        sys.exit()
    return user_selection


def main_menu():
    os.system('cls||clear')
    print('  WGUPS DLD ROUTE MANAGEMENT SYSTEM \n')
    print('        MAIN MENU OPTIONS \n')
    print('(1)-VIEW ALL PACKAGE INFORMATION AT FIRST TIME INTERVAL(09:05:00 AM) \n')
    print('(2)-VIEW ALL PACKAGE INFORMATION AT SECOND TIME INTERVAL(10:20:00 AM) \n')
    print('(3)-SEARCH FOR SPECIFIC PACKAGE \n')
    print('(4)-VIEW ALL PACKAGE INFORMATION AT A SPECIFIED TIME \n')
    print('(0)-EXIT SYSTEM \n')
    try:
        user_selection = int(input('Please Select An Option From The Main Menu: '))
    except ValueError:
        print('Invalid Option Selected. System Will Now Exit.')
        sys.exit()
    return user_selection


def search_menu():
    os.system('cls||clear')
    print('  WGUPS DLD ROUTE MANAGEMENT SYSTEM \n')
    print('        SEARCH MENU     \n')
    print('(1)-SEARCH FOR SPECIFIC PACKAGE \n')
    print('(0)-EXIT SYSTEM \n')
    try:
        user_selection = int(input('Please Select An Option From The Search Menu: '))
    except ValueError:
        print('Invalid Option Selected. System Will Now Exit.')
        sys.exit()
    return user_selection


def main():
    first_selection = start_menu()
    if first_selection == 1:
        os.system('cls||clear')
        print('*******************************************************************************************************')
        print('\t\t\t\t\t **DISPLAYING ALL INITIAL PACKAGE DATA** \n', package_hashtable, '\n')
        os.system('cls||clear')
        print('\n ALERT: Daily Packages Have Been Added To Inventory')
        print('(Y)-Route Packages & Begin Deliveries')
        print('(N)-Exit System')
        user_confirmation = input('Select Y Or N: ')
        if user_confirmation.upper() == 'Y':
            assign_routes()
            begin_deliveries()
            os.system('cls||clear')
        else:
            print('System Will Now Exit.')
            sys.exit()
    elif first_selection == 2:
        os.system('cls||clear')
        print('\n WARNING: Package File Must Be Uploaded To Inventory Before Packages Can Be Routed & Delivered.')
        print('(Y)-Load Package Data, Route Packages, & Begin Deliveries')
        print('(N)-Exit System')
        user_confirmation = input('Select Y Or N: ')
        if user_confirmation.upper() == 'Y':
            os.system('cls||clear')
            print('***************************************************************************************************')
            print('\t\t\t\t\t **DISPLAYING ALL INITIAL PACKAGE DATA** \n', package_hashtable, '\n')
            assign_routes()
            begin_deliveries()
            os.system('cls||clear')
        else:
            sys.exit()
    else:
        sys.exit()

    for i in range(1, 5):
        os.system('cls||clear')
        next_selection = main_menu()
        if next_selection == 1:  # CALL FUNCTION TO GET ALL PACKAGE DATA AT 9:05
            display_message1 = '**DISPLAYING FIRST TIME INTERVAL PACKAGE DELIVERY STATUS 09:05:00 AM**'
            first_status_check('09:05:00', display_message1)
        elif next_selection == 2:  # CALL FUNCTION TO GET ALL PACKAGE DATA AT 10:20
            display_message2 = '**DISPLAYING SECOND TIME INTERVAL PACKAGE DELIVERY STATUS 10:20:00 AM**'
            second_status_check('10:20:00', display_message2)
        elif next_selection == 3:  # SEARCH FOR SPECIFIC PACKAGE MENU
            search_selection = search_menu()
            if search_selection == 1:
                check_value = 'Y'
                while check_value == 'Y':
                    try:
                        search_package = int(input('Please Provide The Package ID Number: '))
                        if search_package in range(1, 41):
                            found_package = package_hashtable.search_for_package(search_package)
                            print('PACKAGE ' + str(search_package) + ' LOCATED:\n', found_package)
                            os.system('cls||clear')
                            print('To Search For Another Package Key Y')
                            search_again = input('Do You Want To Search For Another Package?: ')
                            check_value = search_again.upper()
                        else:
                            print('You Requested To Exit System Or Provided An Invalid Entry.')
                            sys.exit()
                    except ValueError:
                        print('ERROR: Invalid Entry.')
                        sys.exit()
            elif search_selection == 0:
                print('System Will Now Exit.')
                sys.exit()
        elif next_selection == 4:   # CALL FUNCTION TO GET ALL PACKAGE DATA AT USER DEFINED TIME
            check_value = 'Y'
            while check_value == 'Y':
                user_input_time = input('Enter A Time In Military Time Format EX: 13:00:00 ')
                delivery_status_check(user_input_time)
                os.system('cls||clear')
                print('To Check Another Time Key Y')
                see_another_time = input('Do You Want To Check Another Time?: ')
                check_value = see_another_time.upper()
        elif next_selection == 0:
            print('System Will Now Exit.')
            sys.exit()


if __name__ == "__main__":
    main()
