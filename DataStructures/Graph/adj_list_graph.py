from DataStructures.List import array_list as ar
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import edge as ed

def new_graph(size=19, directed=False):
    in_degree = None
    if directed:
        in_degree = mp.new_map(size, 0.5)
    
    return {
        "vertices": mp.new_map(size, 0.5),
        "information": mp.new_map(size, 0.5),
        "in_degree": in_degree,
        "edges": 0,
        "directed": directed,
        "type": "ADJ_LIST"
        }
    
def insert_vertex(my_graph, key_vertex, info_vertex):
    mp.put(my_graph["vertices"], key_vertex, ar.new_list())
    mp.put(my_graph["information"], key_vertex, info_vertex)
    return my_graph

def num_vertices(my_graph):
    return mp.size(my_graph["vertices"])

def num_edges(my_graph):
    return my_graph["edges"]

def vertices(my_graph):
    return mp.key_set(my_graph["vertices"])

def add_edge(graph, vertex_a, vertex_b, weight=0):
    a = mp.get(graph['vertices'], vertex_a)
    b = mp.get(graph['vertices'], vertex_b)
    if a == None or b == None:
        return graph
    existe = False
    for i in a['elements']:
        if i['vertex_b'] == vertex_b:
            i['weight'] = weight
            existe = True
            break
    if not existe:
        ar.add_last(a, {'vertex_a': vertex_a, 'vertex_b': vertex_b, 'weight': weight})
        graph['edges'] += 1
        if not graph['directed']:
            ar.add_last(b, {'vertex_a': vertex_b, 'vertex_b': vertex_a, 'weight': weight})
    if graph['directed'] and not existe:
        inde = mp.get(graph['in_degree'], vertex_b)
        if inde == None:
            mp.put(graph['in_degree'], vertex_b, 1)
        else:
            mp.put(graph['in_degree'], vertex_b, inde+1)

    return graph

def edges(my_graph):
    a =  mp.value_set(my_graph['vertices'])
    re = ar.new_list()
    for i in a['elements']:
        for j in i['elements']:
            put = True
            if not my_graph['directed']:
                for h in re['elements']:
                    if h['vertex_a'] == j['vertex_b'] and h['vertex_b'] == j['vertex_a'] and h['weight'] == j['weight']:
                        put = False
                        break
            if put:
                ar.add_last(re, j)
    return re

def degree(my_graph, key_vertex):
    a= mp.get(my_graph['vertices'], key_vertex)
    if a == None:
        return None
    b = 0
    if my_graph['directed']:
        b = mp.get(my_graph['in_degree'], key_vertex)
    return a['size'] + b

def in_degree(my_graph, key_vertex):
    if my_graph['directed'] == True:
        return mp.get(my_graph['in_degree'], key_vertex)
    a = mp.get(my_graph['vertices'], key_vertex)
    if a == None:
        return None
    return a['size']

def adjacent_edges(my_graph, vertex):
    """
    Retorna los vértices adyacentes (los que el vértice dado apunta).
    """
    if vertex in my_graph:
        return my_graph[vertex]  
    return []

def bfs(graph, start_vertex):
    if mp.get(graph["vertices"], start_vertex) is None:
        return {}

    visited = set()
    queue = [start_vertex]
    parents = {start_vertex: None}

    while queue:
        current_vertex = queue.pop(0)
        if current_vertex not in visited:
            visited.add(current_vertex)

            adj_edges = mp.get(graph["vertices"], current_vertex)
            if adj_edges:
                for edge in adj_edges["elements"]:
                    neighbor = edge["vertex_b"]
                    if neighbor not in visited and neighbor not in parents:
                        queue.append(neighbor)
                        parents[neighbor] = current_vertex

    return parents

def create_graph_search():
    """
    Crea la estructura base para almacenar el recorrido DFS.
    """
    return {
        "visited": mp.new_map(19, 0.5),  
        "path_to": mp.new_map(19, 0.5),  
    }

def dfs_vertex(search, my_graph, vertex):
    
    mp.put(search["visited"], vertex, True) 
    adjacent = adjacent_edges(my_graph, vertex)

    for edge in adjacent:
        neighbor = edge["vertex_b"]  
        if not mp.contains(search["visited"], neighbor):  
            mp.put(search["path_to"], neighbor, vertex)  
            dfs_vertex(search, my_graph, neighbor)  

def dfs(my_graph, source):
    
    search = create_graph_search()  
    dfs_vertex(search, my_graph, source)  
    return search

def find_path(parents, start_vertex, target_vertex):
    if target_vertex not in parents:
        return None
    
    path = []
    current_vertex = target_vertex

    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = parents[current_vertex]
    
    if path[-1] != start_vertex:
        return None

    return path[::-1]
