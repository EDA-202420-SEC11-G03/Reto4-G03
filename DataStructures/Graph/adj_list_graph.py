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
    if vertex in my_graph:
        return my_graph[vertex]
    else:
        return []
def contains_vertex(my_graph, key_vertex):
    return key_vertex in my_graph

def contains_edge(my_graph, origin_vertex, destination_vertex):
    if origin_vertex in my_graph:
        # Verificar si destination está en la lista de nodos adyacentes de source
        return destination_vertex in my_graph[origin_vertex]
    return False