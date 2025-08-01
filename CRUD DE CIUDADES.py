#Implementar al codigo de melva y los grafos correspondientes para su funcionamiento
def agregar_ciudad():
    nombre = input("Ingrese el nombre de la ciudad: ").strip()
    if nombre in ciudades:
        print("La ciudad ya existe.")
        return
    zona = input("Ingrese la zona (Norte/Centro/Sur): ").strip()
    descripcion = input("Ingrese una descripción: ").strip()
    ciudades[nombre] = {"zona": zona, "descripcion": descripcion}
    arbol_zonas[zona].append(nombre)
    guardar_datos()
    print("Ciudad agregada correctamente.")


def listar_ciudades():
    print("\nCiudades ordenadas alfabéticamente:")
    lista = list(ciudades.keys())
    quicksort(lista, 0, len(lista) - 1)
    for ciudad in lista:
        print(f"- {ciudad} ({ciudades[ciudad]['zona']})")


def buscar_ciudad():
    nombre = input("Ingrese el nombre de la ciudad a buscar: ").strip()
    lista = list(ciudades.keys())
    quicksort(lista, 0, len(lista) - 1)
    index = busqueda_binaria(lista, nombre)
    if index != -1:
        ciudad = lista[index]
        print(f"\nCiudad encontrada: {ciudad}")
        print(f"Zona: {ciudades[ciudad]['zona']}")
        print(f"Descripción: {ciudades[ciudad]['descripcion']}")
    else:
        print("Ciudad no encontrada.")


def actualizar_ciudad():
    nombre = input("Ingrese el nombre de la ciudad a actualizar: ").strip()
    if nombre not in ciudades:
        print("La ciudad no existe.")
        return
    zona = input("Nueva zona (Norte/Centro/Sur): ").strip()
    descripcion = input("Nueva descripción: ").strip()
    ciudades[nombre] = {"zona": zona, "descripcion": descripcion}
    if nombre in arbol_zonas[ciudades[nombre]['zona']]:
        arbol_zonas[ciudades[nombre]['zona']].remove(nombre)
    arbol_zonas[zona].append(nombre)
    guardar_datos()
    print("Ciudad actualizada correctamente.")


def eliminar_ciudad():
    nombre = input("Ingrese el nombre de la ciudad a eliminar: ").strip()
    if nombre not in ciudades:
        print("La ciudad no existe.")
        return
    zona = ciudades[nombre]['zona']
    del ciudades[nombre]
    if nombre in arbol_zonas[zona]:
        arbol_zonas[zona].remove(nombre)
    if nombre in grafo_rutas:
        del grafo_rutas[nombre]
    for origen in grafo_rutas:
        grafo_rutas[origen].pop(nombre, None)
    guardar_datos()
    print("Ciudad eliminada correctamente.")


def seleccionar_lugares():
    print("\nCiudades disponibles:")
    listar_ciudades()
    seleccion = input("Ingrese las ciudades separadas por coma: ").split(',')
    seleccion = [ciudad.strip() for ciudad in seleccion if ciudad.strip() in ciudades]
    if not seleccion:
        print("No se seleccionaron ciudades válidas.")
        return []
    return seleccion


def guardar_itinerario():
    lugares = seleccionar_lugares()
    if not lugares:
        return
    nombre_archivo = input("Nombre del archivo de itinerario: ").strip()
    with open(f"itinerario_{nombre_archivo}.txt", 'w') as f:
        for ciudad in lugares:
            datos = ciudades[ciudad]
            f.write(f"{ciudad}|{datos['zona']}|{datos['descripcion']}\n")
    print("Itinerario guardado correctamente.")

# === Algoritmo de ordenamiento manual: QuickSort ===
def quicksort(arr, low, high):
    if low < high:
        pi = particion(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, pi + 1, high)

def particion(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j].lower() <= pivot.lower():
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

# === Algoritmo de búsqueda binaria ===
def busqueda_binaria(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio].lower() == objetivo.lower():
            return medio
        elif lista[medio].lower() < objetivo.lower():
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1
