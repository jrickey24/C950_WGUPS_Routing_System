import datetime as dt
from truck import Truck
from truck import truck3
from truck import truck2
from truck import truck1
from package import package_hashtable


def convert_to_delta(input_time):
    # bigO O(1)-constant
    (hh, mm, ss) = input_time.split(':')
    delta_time = dt.timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss))
    return delta_time


def update_package_address(correct_street, correct_zip, package_number):
    # bigO O(1)-constant
    pkg_to_update = package_hashtable.search_for_package(int(package_number))
    pkg_to_update[1] = correct_street
    pkg_to_update[4] = correct_zip


def load_truck(packages_on_truck, t):
    # bigO O(n)-linear
    for package_num in packages_on_truck:
        package_status_to_update = package_hashtable.search_for_package(int(package_num))
        package_status_to_update[9] = 'IN TRANSIT ON TRUCK ' + str(t)


def run_delivery_route(start_time, route, route_items, truck_number):
    # bigO O(n^2)-quadratic since nested for loop operates on a subset of the same n
    current_time = convert_to_delta(start_time)
    if truck_number == 3 and truck3.is_available():
        load_truck(truck3.package_id_list, truck_number)
        truck3.location_status = 'IN TRANSIT'
    elif truck_number == 2 and truck2.is_available():
        update_package_address('410 S State St', '84111', '9')
        load_truck(truck2.package_id_list, truck_number)
        truck2.location_status = 'IN TRANSIT'
    elif truck_number == 1 and truck1.is_available():
        load_truck(truck1.package_id_list, truck_number)
        truck1.location_status = 'IN TRANSIT'
    for pkg_tuple in route:
        if pkg_tuple[0] != 'WGU_HUB':
            miles_traveled = pkg_tuple[1]
            delivered_packages = [item[0] for item in route_items if item[1] == pkg_tuple[0]]
            elapsed_time = miles_traveled / Truck.speed
            delivery_time = current_time + dt.timedelta(seconds=elapsed_time)
            current_time = delivery_time
            for pkg_id in delivered_packages:
                package_to_update = package_hashtable.search_for_package(int(pkg_id))
                package_to_update[9] = 'DELIVERED BY TRUCK ' + str(truck_number) + ' ' + str(delivery_time)
            delivered_packages.clear()
        else:
            elapsed_time = pkg_tuple[1] / Truck.speed
            completion_time = current_time + dt.timedelta(seconds=elapsed_time)
            if int(truck_number) == 3:
                truck3.location_status = 'HUB'
                truck3.return_time = str(completion_time)
            elif int(truck_number) == 2:
                truck2.location_status = 'HUB'
                truck2.return_time = str(completion_time)
            elif int(truck_number) == 1:
                truck1.location_status = 'HUB'
                truck1.return_time = str(completion_time)


def begin_deliveries():
    run_delivery_route(truck3.departure_time, truck3.delivery_route, truck3.packages_to_deliver, 3)
    run_delivery_route(truck2.departure_time, truck2.delivery_route, truck2.packages_to_deliver, 2)
    run_delivery_route(truck1.departure_time, truck1.delivery_route, truck1.packages_to_deliver, 1)
    daily_miles_traveled = Truck.get_total_miles_driven()
    print('***********************************************************************************************************')
    print('\n\t**DISPLAYING FINAL TIME INTERVAL(EOD) PACKAGE DELIVERY STATUS 12:46:00 PM**\n', package_hashtable, '\n')
    print('***********************************************************************************************************')
    print('\t\t\t\t\t\t\t**DISPLAYING DAILY DELIVERY ROUTE EOD SUMMARY**')
    print('\tTruck 3 Departure Time: ', truck3.departure_time, '\tTruck 3 Return Time: ', truck3.return_time)
    print('\tTruck 3 Total Packages: ', truck3.get_package_count(), '\t\tTruck 3 Distance Traveled: ',
          truck3.route_mileage)
    print('***********************************************************************************************************')
    print('\tTruck 2 Departure Time: ', truck2.departure_time, '\tTruck 2 Return Time: ', truck2.return_time)
    print('\tTruck 2 Total Packages: ', truck2.get_package_count(), '\t\tTruck 2 Distance Traveled: ',
          truck2.route_mileage)
    print('***********************************************************************************************************')
    print('\tTruck 1 Departure Time: ', truck1.departure_time, '\tTruck 1 Return Time: ', truck1.return_time)
    print('\tTruck 1 Total Packages: ', truck1.get_package_count(), '\t\tTruck 1 Distance Traveled: ',
          truck1.route_mileage)
    print('***********************************************************************************************************')
    print('TOTAL DISTANCE TRAVELED BY ALL TRUCKS IN MILES: ', daily_miles_traveled)
    print('***********************************************************************************************************')


def first_status_check(time_interval, display_message):
    # bigO O(n)-linear since the for loop is a fixed length it's O(1), the print list is O(n)
    view_package_list = []
    if time_interval == truck1.departure_time:
        for i in range(1, 41):
            get_data = package_hashtable.search_for_package(int(i))
            if get_data[9].find('DELIVERED BY TRUCK 1') != -1:
                package_data = get_data[0:9] + ['IN TRANSIT ON TRUCK 1']
                view_package_list.append(package_data)
            elif get_data[9].find('DELIVERED BY TRUCK 2') != -1:
                if get_data[7].find('Wrong Address') != -1:
                    package_data = get_data[0:1] + ['300 State St'] + get_data[2:4] + ['84103'] + get_data[5:9] + ['HUB']
                else:
                    package_data = get_data[0:9] + ['HUB']
                view_package_list.append(package_data)
            elif get_data[9].find('DELIVERED BY TRUCK 3') != -1:
                if get_data[9].find('9:11:') != -1 or get_data[9].find('9:14:') != -1 or get_data[9].find('9:28:') != -1:
                    package_data = get_data[0:9] + ['IN TRANSIT ON TRUCK 3']
                    view_package_list.append(package_data)
                else:
                    view_package_list.append(get_data)
    print('***********************************************************************************************************')
    print('\n\t' + display_message, *view_package_list, sep='\n')


def second_status_check(time_interval, display_message):
    # bigO O(n)-linear since the for loop is a fixed length it's O(1), the print list is O(n)
    view_package_list = []
    if time_interval == truck2.departure_time:
        for i in range(1, 41):
            get_data = package_hashtable.search_for_package(int(i))
            if get_data[9].find('BY TRUCK 1') != -1 or get_data[9].find('BY TRUCK 3') != -1:
                if get_data[9].find('TRUCK 1 10:51:00') != -1:
                    package_data = get_data[0:9] + ['IN TRANSIT ON TRUCK 1']
                    view_package_list.append(package_data)
                else:
                    view_package_list.append(get_data)
            else:
                package_data = get_data[0:9] + ['IN TRANSIT ON TRUCK 2']
                view_package_list.append(package_data)
    print('***********************************************************************************************************')
    print('\n\t' + display_message, *view_package_list, sep='\n')


def delivery_status_check(check_time_string):
    # bigO O(n)-linear since the for loop is a fixed length it's O(1), the print list is O(n)
    delivery_status_list = []
    check_time = convert_to_delta(check_time_string)
    t1_departure_time = convert_to_delta(truck1.departure_time)
    t2_departure_time = convert_to_delta(truck2.departure_time)
    t3_departure_time = convert_to_delta(truck3.departure_time)
    for i in range(1, 41):
        status_data = package_hashtable.search_for_package(int(i))
        status_string = status_data[9]
        delivery_truck = int(status_string[19:20])
        delivered_time_string = status_string[21:]
        time_delivered = convert_to_delta(delivered_time_string)
        if check_time >= time_delivered:
            delivery_status_list.append(status_data)
        elif check_time < time_delivered and delivery_truck == 1:
            if check_time >= t1_departure_time:
                delivery_status = status_data[0:9] + ['IN TRANSIT ON TRUCK 1']
                delivery_status_list.append(delivery_status)
            elif check_time < t1_departure_time:
                if status_data[7].find('Delayed Flight') != -1:
                    delivery_status = status_data[0:9] + ['DELAYED']
                else:
                    delivery_status = status_data[0:9] + ['HUB']
                delivery_status_list.append(delivery_status)
        elif check_time < time_delivered and delivery_truck == 2:
            if check_time >= t2_departure_time:
                delivery_status = status_data[0:9] + ['IN TRANSIT ON TRUCK 2']
                delivery_status_list.append(delivery_status)
            elif check_time < t2_departure_time:
                if status_data[7].find('Wrong Address') != -1:
                    delivery_status = status_data[0:9] + ['DELAYED']
                else:
                    delivery_status = status_data[0:9] + ['HUB']
                delivery_status_list.append(delivery_status)
        elif check_time < time_delivered and delivery_truck == 3:
            if check_time >= t3_departure_time:
                delivery_status = status_data[0:9] + ['IN TRANSIT ON TRUCK 3']
                delivery_status_list.append(delivery_status)
            elif check_time < t3_departure_time:
                delivery_status = status_data[0:9] + ['HUB']
                delivery_status_list.append(delivery_status)
    print('***********************************************************************************************************')
    print('\n\t' + 'DELIVERY STATUS AT ' + check_time_string, *delivery_status_list, sep='\n')
