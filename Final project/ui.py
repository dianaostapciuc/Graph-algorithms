from services import Services


class UI():
    def __init__(self):
        self._services = Services()

    def menu(self):
        command = 0
        while command != '0':
            print("0. Exit.")
            print("1. Get the number of vertices.")
            print("2. Parse the set of vertices.")
            print("3. Check for the existence of an edge.")
            print("4. Get <in> and <out> degree of a vertex.")
            print("5. Parse the set of outbound edges of a vertex.")
            print("6. Parse the set of inbound edges of a vertex.")
            print("7. Get the endpoints of a an edge_id.")
            print("8. Retrieve the cost of an edge.")
            print("9. Modify the cost of an edge.")
            print("10. Add vertex.")
            print("11. Remove vertex.")
            print("12. Add edge.")
            print("13. Remove edge.")
            print("14. Make a copy.")
            print("15. Read graph from a text file.")
            print("16. Write graph to a text file.")
            print("17. Create random graph with specified number of vertices and edges.")
            print("18. Print the graph.")
            print("19. Shortest path - reverse breadth first search.")
            print("20. Find a lowest cost walk between the given vertices, using the Dijkstra algorithm.")
            print("21. Verify if the graph is DAG, perform a topological sorting of the activities (Predecessor "
                  "counting algorithm), print the earliest and latest starting times, and critical activities.")

            command = input("What would you like to do> ")
            if command == "0":
                return
            elif command == "1":
                print(self._services.get_nr_of_vertices())
            elif command == "2":
                print(self._services.get_list_of_vertices())
            elif command == "3":
                v1 = input("first vertex: ")
                v2 = input("second vertex: ")
                ok = self._services.checking_if_edge_exists(int(v1), int(v2))
                if ok:
                    print("the edge exists!")
                else:
                    print("the edge does not exist!")
            elif command == "4":
                v = input("vertex: ")
                in_degree = self._services.get_in_degree(int(v))
                out_degree = self._services.get_out_degree(int(v))
                print("the in degree: " + str(in_degree))
                print("the out degree: " + str(out_degree))
            elif command == "5":
                v = input("vertex: ")
                print(self._services.get_outbound_vertex(int(v)))
            elif command == "6":
                v = input("vertex: ")
                print(self._services.get_inbound_vertex(int(v)))
            elif command == "7":
                ids = input("id: ")
                print(self._services.get_edge_endpoint(int(ids)))
            elif command == "8":
                v1 = input("first vertex: ")
                v2 = input("second vertex: ")
                print(self._services.get_weight(int(v1), int(v2)))
            elif command == "9":
                v1 = input("first vertex: ")
                v2 = input("second vertex: ")
                cost = input("cost: ")
                self._services.set_weight(int(v1), int(v2), int(cost))
            elif command == "10":
                v = input("vertex: ")
                self._services.add_vertex(int(v))
            elif command == "11":
                v = input("vertex: ")
                self._services.remove_vertex(int(v))
            elif command == "12":
                v1 = input("first vertex: ")
                v2 = input("second vertex: ")
                cost = input("cost: ")
                self._services.add_edge(int(v1), int(v2), int(cost))
            elif command == "13":
                v1 = input("first vertex: ")
                v2 = input("second vertex: ")
                self._services.remove_edge(int(v1), int(v2))
            elif command == "14":
                self._services.copy_graph()
                print("the copy has been made!")
            elif command == "15":
                filename = input("filename: ")
                self._services.read_graph_from_file(filename)
            elif command == "16":
                filename = input("filename: ")
                self._services.writing_graph_to_file(filename)
            elif command == "17":
                nr_vertices = input("number of vertices: ")
                nr_edges = input("number of edges: ")
                graph = self._services.create_rndm_graph(int(nr_vertices), int(nr_edges))
                print("The randomized graph: \n")
                print(str(graph))
                filename = input("filename: ")
                fout = open(filename, "wt")
                first_line = str(len(graph.graph)) + " " + str(graph.nr_of_edges) + "\n"
                fout.write(first_line)
                for vertex in graph.graph:
                    for edge in graph.graph[vertex]:
                        line = str(vertex) + " " + str(edge[0]) + " " + str(edge[1]) + "\n"
                        fout.write(line)
                fout.close()
            elif command == "18":
                print(str(self._services))
            elif command == "19":
                start_node = int(input("starting node: "))
                end_node = int(input("ending node: "))
                path = self._services.doing_BFS_in_reverse(start_node, end_node)
                print("Length is: " + str(len(path)) + ", the path being: " + str(path))
            elif command == "20":
                first_node = int(input("first node: "))
                second_node = int(input("second node: "))
                path, distance = self._services.lowest_cost_walk(first_node, second_node)
                print("Length is: " + str(distance) + ", the path being: " + str(path))
            elif command == "21":
                '''
                    1. First we need to extract the activities from the input file
                        INPUT FILE FORMAT:
                        <vertex> <vertices that proceed our vertex> <duration>
                        NOTE: we cannot retain the <duration> parameter as an "edge weight" (because it is not specific
                              to the edge, rather to the vertex
                        SOLUTION: save a dictionary like <vertex>:<duration> that we further send as parameter            
                        
                    2. Use the Predecessor Counting Algorithm to check if the graph is DAG => also sort it topologically
                    3. Calculate latest using previously calculated: duration and sorted
                    4. Calculate latest using previously calculated: duration and sorted and earliest
                    5. Calculate critical activities using previously calculated: earliest and latest
                    6. Print them in an orderly fashion :)
                '''
                duration = self._services.read_activities("dag2.txt")  # site teacher
                sorted = self._services.is_dag()
                if sorted == None:
                    print("The graph is not DAG")
                    continue  # skips the rest of this "if command == 21"
                # print(f"Topological order: {str(sorted)}")

                earliest = self._services.early_start(duration, sorted)
                latest = self._services.latest_start(duration, sorted, earliest)
                critical = self._services.critical_activities(earliest, latest)
                print("------------------------------------------------------")
                for v in sorted:
                    print(
                        f"Act.{str(v)} | Duration: {str(duration[v])} | Earliest: {str(earliest[v])}->{str(earliest[v] + duration[v])} | Latest: {str(latest[v])}->{str(latest[v] + duration[v])} | Interval: {str(earliest[v])}-{str(latest[v])}")
                print("------------------------------------------------------")
                print(f"CRITICAL ACTIVITIES: {str(critical)}")
                print("------------------------------------------------------")
            else:
                print("Bad input.")


if __name__ == "__main__":
    ui = UI()
    ui.menu()
