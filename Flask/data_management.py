import json
import os

#Abrir arcjivo JSON.
def open_file(file_path):
    if os.path.getsize(file_path) == 0:
        return []  # Si el file no existe, devuelve na lista vacía.
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data


#Escribir Dict en archivo.
def write_file (file_path, data):
    with open(file_path,'w') as f:
        json.dump(data, f, indent=2)

