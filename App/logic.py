import time
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import adj_list_graph as al
from DataStructures.List import array_list as ar
import csv
import folium
from math import radians, sin, cos, sqrt, atan2
def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {"conexiones": al.new_graph(19, True), "info": mp.new_map(100, 0.5)}
    return catalog

# Funciones para la carga de datos

def agregar_amigos(catalog, info):
    """
    Agrega los amigos de cada usuario
    """
    catalog["amigos"] = mp.new_map(100, 0.5)
    for user in info:
        amigos = ar.new_list()
        
        lista_seguidos_arcos = mp.get(catalog["conexiones"]["vertices"], float(user["USER_ID"]))["elements"]
        lista_seguidores = catalog["followers"][float(user["USER_ID"])]
        
        lista_seguidos = []
        
        for seguido in lista_seguidos_arcos:
            lista_seguidos.append(seguido["vertex_b"])
        
        for seguido in lista_seguidos:
            if seguido in lista_seguidores:
                ar.add_last(amigos, seguido)
        mp.put(catalog["amigos"], float(user["USER_ID"]), amigos)



def load_data(catalog, filename1, filename2):
    """
    Carga los datos del reto
    """
    import csv  # Asegúrate de importar csv

    with open(filename1, mode='r', encoding='latin-1') as file:
        reader = csv.DictReader(file, delimiter=';')
        info = [row for row in reader]
    with open(filename2, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        conexiones = [row for row in reader]
        
    numconex = 0
    numusuarios = 0
    numbasic = 0
    numpremium = 0
    dicnumciudades = {}
    total_seguidores = 0
    catalog["followers"] = ar.new_list()
    
    for user in info:
        if user["USER_TYPE"] == "basic":
            numbasic += 1
        else:
            numpremium += 1
        numusuarios += 1
        if user["CITY"] in dicnumciudades:
            dicnumciudades[user["CITY"]] += 1
        else:
            dicnumciudades[user["CITY"]] = 1
            
        if user["USER_ID"] != "" and user["USER_ID"] != None:
            al.insert_vertex(catalog["conexiones"], float(user["USER_ID"]), user)
            mp.put(catalog["info"], float(user["USER_ID"]), user)
        else:
            al.insert_vertex(catalog["conexiones"], (user["USER_ID"]), user)
            mp.put(catalog["info"], float(user["USER_ID"]), user)
            
        catalog["followers"]["USER_ID"] = []
            
    
    for conexion in conexiones:
        follower_id = float(conexion["FOLLOWER_ID"])
        followed_id = float(conexion["FOLLOWED_ID"])
        al.add_edge(catalog["conexiones"], follower_id, followed_id, conexion["START_DATE"])
        numconex += 1
        
        if mp.get(catalog["conexiones"]["in_degree"], followed_id) is None:
            mp.put(catalog["conexiones"]["in_degree"], followed_id, 1)
        else:
            grado = mp.get(catalog["conexiones"]["in_degree"], followed_id)
            mp.put(catalog["conexiones"]["in_degree"], followed_id, grado + 1)
            
        if followed_id in catalog["followers"]:
            catalog["followers"][followed_id].append(follower_id)
        else:
            catalog["followers"][followed_id] = [follower_id]
        
        if mp.get(catalog["info"], followed_id) is not None:
            total_seguidores += 1

    prom_seguidores = total_seguidores / numusuarios if numusuarios > 0 else 0
    
    ciudad_mas_usuarios = max(dicnumciudades, key=dicnumciudades.get)
    
    agregar_amigos(catalog, info)
    print(mp.value_set(catalog["amigos"]))
    
    return [numusuarios, numconex, numbasic, numpremium, prom_seguidores, ciudad_mas_usuarios]

# Funciones de consulta sobre el catálogo

def get_data(catalog, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Consulta en las Llamar la función del modelo para obtener un dato
    pass


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog, id): #Implementado por Nicorodv
    """
    Retorna el resultado del requerimiento 3
    """
    start = get_time()
    info_user = mp.get(catalog["info"], float(id))
    amigos = ar.new_list()
    amigo_mas_seguido = {}
    mayor_following = 0
         
    for usuario in al.adjacent_edges(catalog["conexiones"], ("USER_ID")):
        
        if al.contains_edge(catalog["conexiones"], usuario, float("USER_ID")):
            ar.add_last(amigos, usuario)
    print(amigos)               
    for amigo in amigos["elements"]:
        
        amigo_info = mp.get(catalog["info"], amigo)
        
        if amigo_info != None:
            followers_actual = mp.get(catalog["conexiones"]["in_degree"], amigo)
            
            if followers_actual > mayor_following:
                mayor_following = followers_actual
                amigo_mas_seguido = {
                    "id": amigo,
                    "nombre": amigo_info["value"]["USER_NAME"],
                    "followers": mayor_following
                }
                
      
    #r = "El amigo mas popular es: " + amigo_mas_seguido["nombre"] + " con " + amigo_mas_seguido["followers"]
    end = get_time()
    delta = delta_time(start, end)
    
    return  delta

def req_4(catalog, id1, id2):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start = get_time()
    amigos1 = mp.get(catalog["amigos"], float(id1))
    amigos2 = mp.get(catalog["amigos"], float(id2))
    
    print(amigos1, amigos2)
    
    amigos_comunes = ar.new_list()
    
    for amigo in amigos1["elements"]:
        if amigo in amigos2["elements"]:
            ar.add_last(amigos_comunes, amigo)

    end = get_time()
    delta = delta_time(start, end)
    return [amigos_comunes, delta]


def req_5(catalog, id, amigos):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    info = mp.get(catalog["conexiones"]["vertices"], float(id))
    
    i=0
    lista = ar.new_list()
    listaamigos = ar.new_list()
    
    
    for seguido in info["elements"]:
        id_seguido = seguido["vertex_b"]
        seguidosseguidor =  mp.get(catalog["conexiones"]["vertices"], id_seguido)
        for seguido2 in seguidosseguidor["elements"]:
            if seguido2["vertex_b"]== float(id):
                ar.add_last(listaamigos, id_seguido)

        
    

    while lista["size"]<= float(amigos) and i< listaamigos["size"]:
         
        infoamigo = mp.get(catalog["conexiones"]["vertices"], listaamigos["elements"][i])
        if infoamigo["size"]>1:
            amigo = mp.get(catalog["conexiones"]["information"], listaamigos["elements"][i])
            dicseguido = {"id": amigo["USER_ID"], "nombre": amigo["USER_NAME"], "seguidores": al.in_degree(catalog["conexiones"], listaamigos["elements"][i])}
            ar.add_last(lista, dicseguido)
        i+=1        
    return lista
        
def req_6(catalog, number):
    """
    Retorna el resultado del requerimiento 6
    """
    
    lista_filtro = ar.new_list()
    
    for user in catalog["info"]["table"]["elements"]:
        if user["value"] != None:
            if user["value"]["seguidores"] != None:
                if user["value"]["seguidores"] > int(number):
                    ar.add_last(lista_filtro, user)
    print(lista_filtro)


def req_7(catalog):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    pass

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
def req_8(catalog, latitud, longitud, radio):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    latitud = float(latitud)
    longitud = float(longitud)
    radio = float(radio)
    vertices = al.vertices(catalog["conexiones"])
    m = folium.Map(location=[latitud, longitud], zoom_start=12)

    folium.Circle(
        location=[latitud, longitud],
        radius=radio * 1000,  
        color="blue",
        fill=True,
        fill_opacity=0.2
    ).add_to(m)
    for vertice in vertices["elements"]:
        infovert = mp.get(catalog["conexiones"]["information"], float(vertice))
        if infovert is not None:
        
            distancia = haversine(latitud, longitud, float(infovert["LATITUDE"]), float(infovert["LONGITUDE"]))
            if distancia<= radio:
                folium.Marker(
                location=[float(infovert["LATITUDE"]), float(infovert["LONGITUDE"])],
                popup=f"{infovert["USER_NAME"]} - {distancia:.2f} km",
                icon=folium.Icon(color="green")
            ).add_to(m)
    m.save("mapa_usuarios.html")        
        


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
