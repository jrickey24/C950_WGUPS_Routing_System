class Truck(object):
    _registry = []

    def __init__(self, location_status, packages_to_deliver, delivery_route,
                 departure_time, return_time, route_mileage):
        self._registry.append(self)
        self.location_status = location_status
        self.packages_to_deliver = packages_to_deliver
        self.delivery_route = delivery_route
        self.departure_time = departure_time
        self.return_time = return_time
        self.route_mileage = route_mileage
        self.package_id_list = []

    capacity = 16  # CAPACITY FOR ALL TRUCKS IS A CONSTANT OF 16 PACKAGES/TRUCK LOAD
    speed = 0.005  # TRUCK SPEED IS PROVIDED IN MILES PER SECOND. CONSTANT SPEED FOR ALL TRUCKS IS 18 MPH.

    @classmethod
    def get_total_miles_driven(cls, total_miles_driven=0):
        # bigO O(n)-linear
        for t in Truck._registry:
            total_miles_driven += t.route_mileage
        return total_miles_driven

    def is_available(self):
        # bigO O(1)-constant
        if self.location_status == 'HUB':
            return True
        else:
            return False

    def get_package_count(self):
        # bigO O(1)-constant
        package_count = len(self.packages_to_deliver)
        return package_count


truck1 = Truck('HUB', [], [], '09:05:00', None, 0)
truck2 = Truck('HUB', [], [], '10:20:00', None, 0)
truck3 = Truck('HUB', [], [], '08:00:00', None, 0)
