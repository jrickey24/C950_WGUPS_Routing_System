import csv
from truck import truck3
from truck import truck2
from truck import truck1
from hashtable import HashTable


class Package:
    def __init__(self, p_id, street, city, state, zipcode, deliver_by,
                 weight, notes, address_alias, delivery_status):
        self._p_id = p_id
        self._street = street
        self._city = city
        self._state = state
        self._zipcode = zipcode
        self._deliver_by = deliver_by
        self._weight = weight
        self._notes = notes
        self._address_alias = address_alias
        self._delivery_status = delivery_status

    @property
    def p_id(self):
        return self._p_id

    @property
    def street(self):
        return self._street

    @property
    def city(self):
        return self._city

    @property
    def state(self):
        return self._state

    @property
    def zipcode(self):
        return self._zipcode

    @property
    def deliver_by(self):
        return str(self._deliver_by)

    @property
    def weight(self):
        return self._weight

    @property
    def notes(self):
        return self._notes

    @property
    def address_alias(self):
        return self._address_alias

    @property
    def delivery_status(self):
        return self._delivery_status

# READ PACKAGE DATA FROM CSV, INSTANTIATE PACKAGE OBJECT & INJECT PACKAGES INTO HASHTABLE AS A LIST OF OBJECT PROPERTIES
# USE QUALIFIERS TO SORT & ASSIGN EACH PACKAGE TO RESPECTIVE TRUCK LIST TO BE ROUTED & DELIVERED
# INSERT PACKAGE ITEM AS TUPLE (PACKAGE ID, ADDRESS ALIAS) TO AIDE WITH EFFICIENCY/ROUTING OPTIMIZATION
# PACKAGE SORTING WAS PRE-DETERMINED AS FOLLOWS:
# **TRUCK 3 TAKES ROUTE 1: *DEPARTURE TIME IS DICTATED BY START OF DAY 8:00*
# 1-ALL PACKAGES THAT MUST BE DELIVERED TOGETHER(& AREN'T SPECIFIED TO BE DELIVERED ON TRUCK 2)
# 2-PACKAGES THAT SHARE A DELIVERY ADDRESS WITH THE ABOVE PACKAGES & AREN'T DELAYED
# 3-ADDITIONAL PACKAGES THAT HAVE A 10:30 DELIVERY TIME & AREN'T DELAYED
# **TRUCK 2 ROUTE 2: *DEPARTURE TIME IS DICTATED BY THE PACKAGE WITH 10:20 ADDRESS UPDATE & DRIVER AVAILABILITY*
# 1-ALL PACKAGES THAT MUST BE DELIVERED ON TRUCK 2
# 2-PACKAGES THAT SHARE A DELIVERY ADDRESS WITH THE ABOVE PACKAGES & DON'T HAVE A 10:30 DELIVER TIME
# 3-PACKAGES WITH NO SPECIAL NOTES, EOD DELIVER BY TIME, & ZIPCODE IN [84104, 84106, 84119]
# **TRUCK 1 ROUTE 3: *DEPARTURE TIME IS DICTATED BY THE ARRIVAL OF DELAYED ON FLIGHT PACKAGES 9:05*
# 1-PACKAGES THAT ARE DELAYED ON FLIGHT
# 2-PACKAGES THAT SHARE AN ADDRESS WITH THE ABOVE
# 3-REMAINING PACKAGES THAT DON'T MEET OTHER QUALIFIERS


package_hashtable = HashTable()
truck3_packages = []
truck2_packages = []
truck1_packages = []
truck3_package_id_list = []
truck2_package_id_list = []
truck1_package_id_list = []
set_status = None

with open('WGUPSPackageFile.csv') as csv_file:
    read_csv = csv.reader(csv_file, delimiter=',')

    for row in read_csv:  # bigO O(n)-linear
        p = Package(p_id=row[0], street=row[1], city=row[2], state=row[3], zipcode=row[4], deliver_by=row[5],
                    weight=row[6], notes=row[7], address_alias=row[8], delivery_status=set_status)

        pkg = [p.p_id, p.street, p.city, p.state, p.zipcode, p.deliver_by, p.weight, p.notes,
               p.address_alias, p.delivery_status]

        package_hashtable.insert_package(key=int(p.p_id), package_item=pkg)

        # TRUCK 3 QUALIFIERS
        if pkg[7].find('Accompany') != -1:
            truck3_packages.append((int(p.p_id), p.address_alias))
            truck3_package_id_list.append(int(p.p_id))
        elif pkg[8].find('HC_Office') > -1 or pkg[8].find('SLC_Housing') > -1 or pkg[8].find('SLCS_Sanitation') > -1:
            if pkg[7].find('Truck 2') == -1 and pkg[7].find('Delayed') == -1 and pkg[7].find('Wrong') == -1:
                truck3_packages.append((int(p.p_id), p.address_alias))
                truck3_package_id_list.append(int(p.p_id))
        elif pkg[5].find('10:30') != -1 and pkg[7].find('Delayed Flight') == -1:
            if pkg[7].find('Wrong Address') == -1 and pkg[8].find('SLC_UPD') == -1:
                truck3_packages.append((int(p.p_id), p.address_alias))
                truck3_package_id_list.append(int(p.p_id))
        elif pkg[8].find('C_Hall') != -1 or pkg[8].find('SH_Park') != -1:
            if pkg[8].find('TC_Hall') == -1:
                truck3_packages.append((int(p.p_id), p.address_alias))
                truck3_package_id_list.append(int(p.p_id))
        # TRUCK 2 QUALIFIERS
        elif pkg[7].find('Truck 2') != -1 or (pkg[8].find('TDJ_Court') != -1 and pkg[5].find('EOD') != -1):
            truck2_packages.append((int(p.p_id), p.address_alias))
            truck2_package_id_list.append(int(p.p_id))
        elif pkg[5].find('EOD') != -1 and pkg[7].find('None') != -1:
            if pkg[4].find('84104') > -1 or pkg[4].find('84106') > -1 or pkg[4].find('84119') > -1:
                truck2_packages.append((int(p.p_id), p.address_alias))
                truck2_package_id_list.append(int(p.p_id))
        # TRUCK 1 QUALIFIERS
        if pkg[7].find('Delayed Flight') != -1 or pkg[8].find('WH_Farm') != -1:
            truck1_packages.append((int(p.p_id), p.address_alias))
            truck1_package_id_list.append(int(p.p_id))
        elif (pkg[8].find('CCR_Springs') != -1 and pkg[5].find('EOD') != -1) or pkg[8].find('SLC_UPD') != -1:
            truck1_packages.append((int(p.p_id), p.address_alias))
            truck1_package_id_list.append(int(p.p_id))
        elif pkg[8].find('TC_Hall') != -1 or (pkg[8].find('UDMV_Office') != -1 and pkg[5].find('EOD') != -1):
            truck1_packages.append((int(p.p_id), p.address_alias))
            truck1_package_id_list.append(int(p.p_id))
        elif pkg[8].find('MC_Museum') != -1 or pkg[8].find('VRS_Complex') != -1 or pkg[8].find('RTP_Park') != -1:
            truck1_packages.append((int(p.p_id), p.address_alias))
            truck1_package_id_list.append(int(p.p_id))

        if pkg[7].find('Delayed Flight') != -1 or pkg[7].find('Wrong Address') != -1:
            set_status = 'DELAYED'
        else:
            set_status = 'HUB'

        update_package = package_hashtable.search_for_package(int(p.p_id))
        update_package[9] = set_status

truck3.packages_to_deliver = truck3_packages
truck3.package_id_list = truck3_package_id_list[:]
truck2.packages_to_deliver = truck2_packages
truck2.package_id_list = truck2_package_id_list[:]
truck1.packages_to_deliver = truck1_packages
truck1.package_id_list = truck1_package_id_list[:]
