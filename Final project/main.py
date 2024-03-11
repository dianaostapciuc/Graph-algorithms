import heapq
import random
from collections import deque
from copy import deepcopy


class DirectedGraph:
    def __init__(self):
        self.graph = {}
        self.edge_ids = {}
        self.nr_of_edges = 0
        self.nr_of_vertices = 0

    def adding_a_vertex(self, v):
        if v in self.graph:
            print("Vertex already exists!")
        else:
            self.graph[v] = []
            self.nr_of_vertices += 1

    def adding_an_edge(self, v1, v2, weight):
        edge_id = len(self.edge_ids)
        if v1 not in self.graph:
            self.adding_a_vertex(v1)
        if not self.check_if_edge_exists(v1, v2):
            self.graph[v1].append([v2, weight, edge_id])
        self.edge_ids[(v1, v2)] = edge_id
        self.nr_of_edges += 1

    def removing_a_vertex(self, v):
        if v in self.graph:
            del self.graph[v]

        for vertex in self.graph:
            for edge in self.graph[vertex]:
                if vertex == v or edge[0] == v:
                    del self.edge_ids[(vertex, edge[0])]

        for vertex in self.graph:
            for edge in self.graph[vertex]:
                if edge[0] == v:
                    self.graph[vertex].remove(edge)

    def removing_an_edge(self, v1, v2):
        if self.check_if_edge_exists(v1, v2):
            for edge in self.graph[v1]:
                if edge[0] == v2:
                    self.graph[v1].remove(edge)
            del self.edge_ids[(v1, v2)]

    def __str__(self):
        string = ""
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                string += str(vertex) + "->" + str(edge[0]) + ", weight: " + str(edge[1]) + "\n"
        return string

    def get_number_of_vertices(self):
        return len(self.graph)

    def get_list_of_vertex(self):
        vertices = []
        vertices = list(self.graph.keys())
        return vertices

    def reading_graph(self, filename):
        fin = open(filename, "rt")
        first_line = fin.readline()
        first_line = first_line.split()
        nr_of_vertices = int(first_line[0])
        nr_of_edges = int(first_line[1])
        for line in fin:
            lines = line.strip().split()
            v1 = int(lines[0])
            v2 = int(lines[1])
            e = int(lines[2])
            if v1 not in self.graph:
                self.adding_a_vertex(v1)
            if v2 not in self.graph:
                self.adding_a_vertex(v2)
            self.adding_an_edge(v1, v2, e)

            edge_id = len(self.edge_ids)
            self.edge_ids[(v1, v2)] = edge_id
        fin.close()

    def writing_graph(self, filename):
        fout = open(filename, "wt")
        first_line = str(self.get_number_of_vertices()) + " " + str(len(self.get_list_of_vertex())) + "\n"
        fout.write(first_line)
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                line = str(vertex) + " " + str(edge[0]) + " " + str(edge[1]) + "\n"
                fout.write(line)
        fout.close()

    def check_if_edge_exists(self, v1, v2):
        if v1 not in self.graph:
            return False
        for edge in self.graph[v1]:
            if edge[0] == v2:
                return True
        return False

    def in_degree(self, v):
        degree = 0
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                if edge[0] == v:
                    degree += 1
        return degree

    def out_degree(self, v):
        if v in self.graph:
            return len(self.graph[v])
        else:
            print("Given vertex does not exist")
            return None

    def get_edge_endpoints(self, edge_id):
        for key in self.edge_ids:
            if self.edge_ids[key] == edge_id:
                return key
        return None

    def get_edge_weight(self, v1, v2):
        ok = 0
        for edge in self.graph[v1]:
            if edge[0] == v2:
                return edge[1]
                ok = 1
        if ok == 0:
            return None

    def set_edge_weight(self, v1, v2, weight):
        for edge in self.graph[v1]:
            if edge[0] == v2:
                edge[1] = weight

    def parse_outbound_vertex(self, vertex):
        outbound_vertices = []
        for edge in self.graph[vertex]:
            outbound_vertices.append(edge[0])
        return outbound_vertices

    def parse_inbound_vertex(self, v):
        inbound_vertices = []
        for vertex in self.graph:
            for edge in self.graph[vertex]:
                if edge[0] == v:
                    inbound_vertices.append(vertex)
        return inbound_vertices

    def reverse_BFS(self, start, end):
        # we initialise what we use
        queue = deque([end])
        visited = set([end])
        parents = {end: None}
        # this happens until nothing's left in the queue
        while queue:
            vertex = queue.popleft()
            if vertex == start:
                path = []
                while vertex is not None:
                    path.append(vertex)
                    vertex = parents[vertex]
                path.reverse()
                return path
            # we add the nodes that we haven't checked yet and update the info
            for neighbor in self.graph[vertex]:
                if neighbor[0] not in visited:
                    visited.add(neighbor[0])
                    parents[neighbor[0]] = vertex
                    queue.append(neighbor[0])
        return None

    def Dijkstra_algorithm(self, start, end):
        distances = {vertex: float('inf') for vertex in self.graph}
        distances[start] = 0
        previous = {}
        queue = [(0, start)]
        while queue:
            current_distance, current_vertex = heapq.heappop(queue)
            if current_distance > distances[current_vertex]:
                continue
            for edge in self.graph[current_vertex]:
                neighbor = edge[0]
                weight = edge[1]
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(queue, (distance, neighbor))
        if end not in previous:
            return None
        path = []
        current_vertex = end
        while current_vertex != start:
            path.append(current_vertex)
            current_vertex = previous[current_vertex]
        path.append(start)

        path.reverse()
        return path, distances[end]

    # ------------------------------------------------------------------------------------------------------------------
    #                                              PRACTICAL WORK NO.4
    # ------------------------------------------------------------------------------------------------------------------

    def read_activities(self, filename):
        fin = open(filename, "rt")
        duration = {}
        number_of_vertices = int(fin.readline())

        for i in range(number_of_vertices):
            line = fin.readline()
            line = line.split(" ")
            vertex_to_add = int(line[0])  # gets the first element of the line
            if vertex_to_add not in self.graph:
                self.adding_a_vertex(vertex_to_add)

            duration_of_vertex = int(line[len(line) - 1])  # gets the last element of the like (the duration)
            duration[vertex_to_add] = duration_of_vertex
            for j in range(1, len(line) - 1):  # iterates all prerequisites (everything in between vertex-duration)
                # prerequisite vertex needs to "happen" before our current vertex
                # -> we add the edge prerequisite_vertex -> vertex_to_add
                prerequisite_vertex = int(line[j])

                # -1 is the notation for when a vertex does not have prerequisites
                # the weight is irrelevant in this scenario, so it can be set to anything (so is the edge id)
                if prerequisite_vertex != -1:
                    if prerequisite_vertex not in self.graph:
                        self.adding_a_vertex(prerequisite_vertex)
                    self.adding_an_edge(prerequisite_vertex, vertex_to_add, 1)
                    edge_id = len(self.edge_ids)
                    self.edge_ids[(prerequisite_vertex, vertex_to_add)] = edge_id
        fin.close()
        return duration

    def is_dag(self):  # directed acyclic graph
        '''
                The algorithm used is THE PREDECESSOR COUNTING ALGORITHM
                Step 1. Look for the "root" vertices (in_degree = 0)
                Step 2. Taking the vertices obtained above one by one
                        -iterate through each of their outbound neighbours and subtract 1 from their inbound count
                    By doing this: we start with "roots", which we eliminate, and obtain other "roots"
                    (repeat until the queue is empty)

                => if by the end, we have visited all vertices, then the graph is a DAG

                -dict <in_degree> to retain the in degree of every vertex
                -list <sorted> to retain the order in which we added the vertices
                -queue <queue> to go through all possible vertices
                :return: a vector containing the vertices topologically sorted
                '''
        in_degree = {}
        sorted = []
        queue = []
        for v in self.get_list_of_vertex():  # retaining all in degrees
            in_degree[v] = self.in_degree(v)  # dict with key vertex, list as the in bound vertices
            if in_degree[v] == 0:  # start vertex(root)
                sorted.append(v)
                queue.append(v)
        while len(queue) != 0:
            v1 = queue.pop()
            for v2 in self.parse_outbound_vertex(v1):  # going through the outbounds of the vertex in queue
                in_degree[v2] -= 1  # remove v1 from v2
                if in_degree[v2] == 0:  # check if v2 is left with in_degree = 0 (making it a root), add to queue
                    queue.append(v2)
                    sorted.append(v2)
        # sorting topologically
        if len(sorted) is not self.nr_of_vertices:  # check if DAG (it is DAG when the length of sorted vertices is
            # the nr of vertices
            return None
        return sorted

    def early_start(self, duration, sorted):
        '''
            Step 1. Our queue is easily created because our activities are sorted
                    - the sorted dict needs to be flipped (the first in needs to first out)
            Step 2. Initialize the earliest start with 0
            Step 3. Take each vertex one by one from the queue and
                    -calculate the duration from it to its outbound neighbours
            NOTE: we retain in <earliest> dict only the longest durations to get to an activity
                    (because an activity can only start if the ones before it finishes)
                    (in other words, a vertex's earliest duration = when the last inbound neighbour gets to it)
        :param duration: a dict of the vertices and their durations
        :param sorted: a dict of the vertices sorted topologically
        :return: a dict of the activities and the earliest times they can start
        '''
        queue = deepcopy(sorted)  # after the is_dag function does it
        queue.reverse()  # we reverse it
        earliest = {}
        for v in self.graph:  # initialise all earliest start vertices with 0
            earliest[v] = 0

        while len(queue) != 0:  # take vertices from the queue, parse their outbounds (where they go)
            v1 = queue.pop()
            for v2 in self.parse_outbound_vertex(v1):
                earliest[v2] = max(earliest[v2], earliest[v1] + duration[v1])  # so we get the largest duration possible
        return earliest

    def latest_start(self, duration, sorted, earliest):
        '''
            Step 1. We need to figure out when all activities (including the last one) finish
                    -look for the activity that starts FINISHES last
                    -from there, we apply the reverse of the earliest algorithm
                        - initialize the <latest> dict for all vertices like: finish_time - last_action
                          to estimate when they could start their last action
            Step 2. Take the queue (this time in reverse order) and reverse the method used to find <earliest>
        :param duration: a dict of the vertices and their durations
        :param sorted: a dict of the vertices sorted topologically
        :param earliest: a dict of the activities and the earliest times they can start
        :return: a dict of the activities and the latest times they can start
        '''
        finish_time = 0
        for v in earliest:  # iterate the vertices of earliest times
            finish_time = max(finish_time, earliest[v] + duration[v])

        latest = {}
        for v in self.graph:
            latest[v] = finish_time - duration[v]

        queue = deepcopy(sorted)
        while len(queue) != 0:
            v1 = queue.pop()
            for v2 in self.parse_inbound_vertex(v1):
                latest[v2] = min(latest[v2], latest[v1] - duration[v2])
        return latest

    def critical_activities(self, earliest, latest):
        # an activity is critical if its earliest time is also its latest
        critical_activities = []
        for v in self.graph:
            if earliest[v] == latest[v]:  # check what is equal
                critical_activities.append(v)
        return critical_activities

    @classmethod
    def create_random_graph(cls, nr_of_vertices, nr_of_edges):

        if nr_of_edges > nr_of_vertices * (nr_of_vertices - 1):
            raise ValueError("Too many edges")
        graph = cls()
        vertices = list(range(nr_of_vertices))
        random.shuffle(vertices)
        num_edges_added = 0
        while num_edges_added < nr_of_edges:
            u, v = random.sample(vertices, 2)
            graph.adding_a_vertex(u)
            graph.adding_a_vertex(v)
            graph.adding_an_edge(u, v, random.randint(1, 10))
            num_edges_added += 1
        return graph

# if __name__ == "__main__":
#     graph = DirectedGraph()
#     graph.adding_a_vertex(1)
#     graph.adding_a_vertex(2)
#     graph.adding_a_vertex(3)
#     graph.adding_a_vertex(2)
#     graph.adding_an_edge(1, 3, 5)
#     graph.adding_an_edge(5, 3, 5)
#     graph.adding_an_edge(1, 2, 6)
#     graph.adding_an_edge(2, 3, 1)
#     graph.adding_an_edge(3, 4, 2)
#     graph.adding_an_edge(4, 5, 0)
#     graph.adding_an_edge(3, 1, 1)
#     graph.removing_an_edge(3, 1)
#     graph.removing_an_edge(6, 6)
#     print(graph)
#     graph.reverse_BFS(1, 5)
#     print(graph.get_number_of_vertices())
#     print(graph.get_list_of_vertex())
#     print(graph.in_degree(1))
#     print(graph.in_degree(3))
#     print(graph.out_degree(1))
#     print(graph.out_degree(3))
#     print(graph.get_edge_weight(1,3))
#     graph.set_edge_weight(1,3,10)
#     print(graph.get_edge_weight(1, 3))
#     print(graph.parse_outbound_vertex())
#     print(graph.parse_inbound_vertex())

# self.graph : key : { inkey, weight, edge_id }
