from copy import deepcopy

from main import DirectedGraph


class Services(DirectedGraph):
    def __init__(self):
        self._graph = DirectedGraph()
        self._copies = []

    def read_graph_from_file(self, filename):
        return self._graph.reading_graph(filename)

    def writing_graph_to_file(self, filename):
        self._graph.writing_graph(filename)

    def read_and_print(self, filename):
        self._graph.reading_graph(filename)
        print(self._graph)

    def add_vertex(self, v):
        self._graph.adding_a_vertex(v)

    def add_edge(self, v1, v2, weight):
        self._graph.adding_an_edge(v1, v2, weight)

    def remove_vertex(self, v):
        self._graph.removing_a_vertex(v)

    def remove_edge(self, v1, v2):
        self._graph.removing_an_edge(v1, v2)

    def get_nr_of_vertices(self):
        return self._graph.get_number_of_vertices()

    def get_list_of_vertices(self):
        return self._graph.get_list_of_vertex()

    def checking_if_edge_exists(self, v1, v2):
        return self._graph.check_if_edge_exists(v1, v2)

    def get_in_degree(self, v):
        return self._graph.in_degree(v)

    def get_out_degree(self, v):
        return self._graph.out_degree(v)

    def get_edge_endpoint(self, ids):
        return self._graph.get_edge_endpoints(ids)

    def get_weight(self, v1, v2):
        return self._graph.get_edge_weight(v1, v2)

    def set_weight(self, v1, v2, weight):
        self._graph.set_edge_weight(v1, v2, weight)

    def get_outbound_vertex(self, v):
        return self._graph.parse_outbound_vertex(v)

    def get_inbound_vertex(self, v):
        return self._graph.parse_inbound_vertex(v)

    def copy_graph(self):
        self._copies.append(deepcopy(self._graph))

    def create_rndm_graph(self, nr_vertices, nr_edges):
        return self._graph.create_random_graph(nr_vertices, nr_edges)

    def doing_BFS_in_reverse(self, start, end):
        return self._graph.reverse_BFS(start, end)

    def lowest_cost_walk(self, start, end):
        return self._graph.Dijkstra_algorithm(start, end)

    def read_activities(self, filename):
        return self._graph.read_activities(filename)

    def is_dag(self):
        return self._graph.is_dag()

    def early_start(self, duration, sorted):
        return self._graph.early_start(duration, sorted)

    def latest_start(self, duration, sorted, earliest):
        return self._graph.latest_start(duration, sorted, earliest)

    def critical_activities(self, earliest, latest):
        return self._graph.critical_activities(earliest, latest)

    def __str__(self):
        return str(self._graph)
