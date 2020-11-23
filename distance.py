import csv


class Graph:

    def __init__(self):
        self.delivery_adj_dict = {}  # USES THE ADDRESS ALIAS EX: WGU_HUB AS THE VERTEX LABEL
        self.edge_weights = {}  # WEIGHT = DISTANCE(IN MILES) BETWEEN DELIVERY LOCATIONS

    def add_vertex(self, vertex_to_add):
        self.delivery_adj_dict[vertex_to_add] = []

    def add_undirected_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.delivery_adj_dict[from_vertex].append(to_vertex)


def get_distance_csv(distance_file):
    # bigO O(n)-linear
    distance_csv = []
    with open(distance_file) as csv_file:
        read_csv = csv.reader(csv_file)
        next(read_csv, None)
        for row in read_csv:
            distance_csv.append(row)
    return distance_csv


def map_distances(distance_file):
    # bigO O(n)-linear since nested for loop is defined by constant range value
    distances = get_distance_csv(distance_file)
    distance_graph = Graph()
    for row in distances:
        distance_graph.add_vertex(row[1])
        for i in range(2, 29):
            distance_graph.add_undirected_edge(row[1], distances[i - 2][1], float(row[i]))
    return distance_graph


graph = map_distances(distance_file="WGUPSDistances.csv")


def get_distance(from_vertex, to_vertex):
    # bigO O(1)-constant
    distance_to_location = graph.edge_weights.get((from_vertex, to_vertex))
    return distance_to_location
