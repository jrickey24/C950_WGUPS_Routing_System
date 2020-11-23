import pprint as pp


class HashTable:

    def __init__(self, table_size=41):
        self.table = []
        for i in range(table_size):
            self.table.append([])

    def __str__(self):
        return pp.pformat(self.table[1:41], indent=0, width=158, compact=True)

    def insert_package(self, key, package_item):
        ht_bucket = key % len(self.table)
        self.table[ht_bucket].append(package_item)

    def remove_package(self, key):
        ht_bucket = key % len(self.table)
        ht_bucket_list = self.table[ht_bucket]
        for package_item in ht_bucket_list:
            if int(package_item[0]) == key:
                ht_bucket_list.remove(key)

    def search_for_package(self, key):
        ht_bucket = key % len(self.table)
        ht_bucket_list = self.table[ht_bucket]
        for package_item in ht_bucket_list:
            if int(package_item[0]) == key:
                return package_item
            else:
                return None
