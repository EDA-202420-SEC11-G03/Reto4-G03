import time
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import adj_list_graph as al
from DataStructures.List import array_list as ar
import csv
def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    catalog = {"conexiones": al.new_graph(19, True), "info": mp.new_map(100, 0.5)}
    return catalog

# Funciones para la carga de datos

def agregar_amigos(catalog, info, conexiones):
    """
    Agrega una llave 'amigos' al catálogo con la información de los amigos de cada usuario.
    """
    catalog["amigos"] = mp.new_map()

    for conexion in conexiones:
        follower_id = float(conexion["FOLLOWER_ID"])
        followed_id = float(conexion["FOLLOWED_ID"])

        if mp.contains(catalog["info"], follower_id) and mp.contains(catalog["info"], followed_id):
            follower_info = mp.get(catalog["info"], follower_id)["value"]
            followed_info = mp.get(catalog["info"], followed_id)["value"]

            if mp.contains(catalog["amigos"], follower_id):
                amigos_list = mp.get(catalog["amigos"], follower_id)["value"]
            else:
                amigos_list = ar.new_list()
                mp.put(catalog["amigos"], follower_id, amigos_list)

            ar.add_last(amigos_list, followed_info)

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
            
        al.insert_vertex(catalog["conexiones"], float(user["USER_ID"]), user)
        mp.put(catalog["info"], float(user["USER_ID"]), user)
    
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
        
        if mp.get(catalog["info"], followed_id) is not None:
            total_seguidores += 1

    prom_seguidores = total_seguidores / numusuarios if numusuarios > 0 else 0
    
    ciudad_mas_usuarios = max(dicnumciudades, key=dicnumciudades.get)

    agregar_amigos(catalog, info, conexiones)
    
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


def req_8(catalog):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


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
