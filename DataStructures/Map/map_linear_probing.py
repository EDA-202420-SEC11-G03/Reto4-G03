import random
from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
from DataStructures.List import array_list as arl
def new_map(num_elements, load_factor, prime=109345121):
    capacity = mf.next_prime(num_elements//load_factor)
    scale = random.randint(1, prime-1)
    shift = random.randint(0, prime-1)
    hash_table = {'prime': prime,
    'capacity': capacity,
    'scale': scale,
    'shift': shift,
    'table': arl.new_list(),
    'current_factor': 0,
    'limit_factor': load_factor,
    'size': 0,
    'type': 'PROBING'}
    for _ in range(capacity):
        entry = me.new_map_entry(None, None)
        arl.add_last(hash_table['table'], entry)
    return hash_table

def put(my_map, key, value):
    if my_map['size'] + 1 > my_map['capacity'] * my_map['limit_factor']:
        rehash(my_map)

    hash_value = mf.hash_value(my_map, key)
    slot_finded = find_slot(my_map, key, hash_value)
    if slot_finded[0] == False:
        my_map['table']['elements'][slot_finded[1]] = me.new_map_entry(key, value)
        my_map['size'] += 1
    else:
        my_map['table']['elements'][slot_finded[1]] = me.new_map_entry(key,value)
    return my_map

def contains(my_map, key):
    for i in my_map['table']['elements']:
        if i['key'] == key:
            return True
    return False

def get(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    slot_finded = find_slot(my_map, key, hash_value)
    if slot_finded[0] == False:
        return None
    return my_map['table']['elements'][slot_finded[1]]["value"]

def remove(my_map, key):
    index = 0
    sentinel = False
    hash_value = mf.hash_value(my_map, key)
    while True:
        if index == 0 and sentinel == True:
            break
        if my_map['table']['elements'][hash_value + index]['key'] == key:
            my_map['table']['elements'][hash_value + index] = me.new_map_entry('__EMPTY__', '__EMPTY__')
            my_map['size'] -= 1
            break
        if index + hash_value == my_map['capacity'] - 1:
            index = -hash_value
        sentinel = True
        index += 1
    return my_map

def size(my_map):
    return my_map['size']

def is_empty(my_map):
    return my_map['size'] == 0 

def key_set(my_map):
    list = arl.new_list()
    for i in my_map['table']['elements']:
        if i['key'] != None and i['key'] != '__EMPTY__':
            arl.add_last(list, i['key'])
    return list

def value_set(my_map):
    list = arl.new_list()
    for i in my_map['table']['elements']:
        if i['key'] != None and i['key'] != '__EMPTY__':
            arl.add_last(list, i['value'])
    return list

def find_slot(my_map, key, hash_value):
    i = 0
    best = None
    while True:
        if (my_map['table']['elements'][hash_value+i]['key'] == key):
            return (True, hash_value+i)
        elif my_map['table']['elements'][hash_value+i]['key'] == '__EMPTY__' and best == None:
            best = hash_value+i
        elif my_map['table']['elements'][hash_value+i]['key'] == None :
            if best != None:
                return (False, best)
            return (False, hash_value+i)
        if i + hash_value == my_map['capacity']-1:
            i = -hash_value
        i += 1
        
def is_available(table, pos):
    return table['elements'][pos]['key'] == None or table['elements'][pos]['key'] == '__EMPTY__'
    
def rehash(my_map):
    newList = arl.new_list()
    capacity2 = mf.next_prime(my_map['size']*2//my_map['limit_factor'])
    my_map['capacity'] = capacity2
    for _ in range(capacity2):
        entry = me.new_map_entry(None, None)
        arl.add_last(newList, entry)
    old = my_map['table']['elements']
    
    my_map['table'] = newList
    my_map['size'] = 0
    for i in old:
        if i['key'] != None:
            put(my_map, i['key'], i['value'])
    return my_map