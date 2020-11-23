import heapq
from truck import truck3
from truck import truck2
from truck import truck1
from distance import get_distance


# PROVIDE UNSORTED LIST OF TUPLES CONTAINING (PACKAGE ID, ADDRESS ALIAS) FOR ALL PACKAGES TO BE DELIVERED
# ON A GIVEN TRUCKLOAD. RETURN LIST OF DISTINCT UNVISITED LOCATIONS TO OPTIMIZE ROUTE/PATH FINDING ALGORITHM
def get_unvisited_locations(input_route):
    # bigO O(n)-linear
    unvisited_locations = []
    for x, y in input_route:
        if y not in unvisited_locations:
            unvisited_locations.append(y)
    return unvisited_locations


# RETURNS A TUPLE VALUE CONTAINING THE CLOSEST LOCATION FROM THE STARTING LOCATION(HUB) & COST OF TRAVEL IN MILES
def get_nearest_to_hub(input_route):
    # bigO O(n)-linear
    cost_matrix = []
    for location in get_unvisited_locations(input_route):
        cost = get_distance('WGU_HUB', location)
        cost_matrix.append((location, cost))
    nearest_to_hub = heapq.nsmallest(1, cost_matrix, key=lambda x: float(x[1]))
    return nearest_to_hub


# RETURNS A TUPLE VALUE CONTAINING THE CLOSEST LOCATION FROM THE LAST VISITED LOCATION & COST OF TRAVEL IN MILES
def get_nearest_location(last_visited, unvisited):
    # bigO O(n)-linear
    cost_matrix = []
    for destination in unvisited:
        cost = get_distance(last_visited, destination)
        cost_matrix.append((destination, cost))
    nearest_location = heapq.nsmallest(1, cost_matrix, key=lambda x: float(x[1]))
    return nearest_location


# TAKES AN UNORDERED BUNDLE OF PACKAGES & DELIVERY LOCATIONS PRE-ASSIGNED TO ANY GIVEN TRUCK
# RETURNS AN ORDERED OPTIMIZED ROUTE THAT CAN BE EXECUTED AT A GIVEN DELIVERY TIME
def get_route(input_route):
    # bigO O(n)-linear
    total_cost_list = []
    visited_locations = []
    first_location = get_nearest_to_hub(input_route)
    unvisited_locations = get_unvisited_locations(input_route)
    visited_locations.append((first_location[0][0], first_location[0][1]))
    unvisited_locations.remove(first_location[0][0])
    total_cost_list.append(first_location[0][1])
    previous_location = first_location[0][0]
    while len(unvisited_locations) > 0:
        min_cost = get_nearest_location(previous_location, unvisited_locations)
        current_location = min_cost[0][0]
        cost = min_cost[0][1]
        visited_locations.append((current_location, cost))
        unvisited_locations.remove(current_location)
        total_cost_list.append(cost)
        previous_location = current_location
    return_to_hub = get_distance(previous_location, 'WGU_HUB')
    total_cost_list.append(return_to_hub)
    visited_locations.append(('WGU_HUB', return_to_hub))
    tcl = round(sum(total_cost_list), 2)
    return tcl, total_cost_list, visited_locations


def assign_routes():
    route1 = get_route(truck3.packages_to_deliver)
    truck3.delivery_route = route1[2]
    truck3.route_mileage = route1[0]

    route2 = get_route(truck2.packages_to_deliver)
    truck2.delivery_route = route2[2]
    truck2.route_mileage = route2[0]

    route3 = get_route(truck1.packages_to_deliver)
    truck1.delivery_route = route3[2]
    truck1.route_mileage = route3[0]
