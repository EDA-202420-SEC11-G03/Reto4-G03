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
    catalog = {"conexiones": al.new_graph(), "info": mp.new_map(100, 0.5)}
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename1, filename2):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    with open(filename1, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        info = [row for row in reader]
    with open(filename2, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        conexiones = [row for row in reader]
    numconex=0
    numusuarios=0
    numbasic=0
    numpremium=0
    dicnumciudades = {}
    prom=0
    for usuario in info:
        dicnumciudades[usuario["CITY"]]=0
        if usuario["USER_TYPE"]=="basic":
            numbasic+=1
        else:
            numpremium+=1
        numusuarios+=1
        usuario["seguidores"]=0
        usuario["lista de seguidores"]= ar.new_list()
        usuario["personas que sigue"]= ar.new_list()
        for conexion in conexiones:
            if float(usuario["USER_ID"])== float(conexion["FOLLOWED_ID"]):
                usuario["seguidores"]+=1
                ar.add_last(usuario["lista de seguidores"], conexion["FOLLOWER_ID"])
            elif float(usuario["USER_ID"])== float(conexion["FOLLOWER_ID"]): 
                ar.add_last(usuario["personas que sigue"],conexion["FOLLOWED_ID"])
         
    for usuario in info:
        prom+=usuario["seguidores"]
        dicnumciudades[usuario["CITY"]]+=1
        mp.put(catalog["info"], float(usuario["USER_ID"]), usuario)
    for conexion in conexiones:
        al.insert_vertex(catalog["conexiones"], float(conexion["FOLLOWER_ID"]), conexion)
        al.add_edge(catalog["conexiones"], float(conexion["FOLLOWER_ID"]), float(conexion["FOLLOWED_ID"]))
        numconex+=1
    prom = prom/numusuarios
    ciudad = max(dicnumciudades, key=dicnumciudades.get)
    return (numusuarios, numconex, numbasic, numpremium, prom, ciudad)
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


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog, id, amigos):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    info = mp.get(catalog["info"], float(id))
    
    i=0
    lista = ar.new_list()
    listaamigos = ar.new_list()
    for seguido in info["personas que sigue"]["elements"]:
        if seguido in info["lista de seguidores"]["elements"]:
            ar.add_last(listaamigos, seguido)

    while lista["size"]<= float(amigos) and i< listaamigos["size"]:
         
        infoseguido = mp.get(catalog["info"], float(listaamigos["elements"][i]))
        if infoseguido["personas que sigue"]["size"]>1:

            dicseguido = {"id": infoseguido["USER_ID"], "nombre": infoseguido["USER_NAME"], "seguidores": infoseguido["seguidores"]}
            ar.add_last(lista, dicseguido)
        i+=1        
    return lista
        
def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


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
        infovert = mp.get(catalog["info"], float(vertice))
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
