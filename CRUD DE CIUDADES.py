
#Implementar al codigo de melva y los grafos correspondientes para su funcionamiento
def agregar_volcan():
    nombre = input("Ingrese el nombre del volcán: ").strip()
    if nombre in ciudades:
        print("El volcán ya existe.")
        return
    descripcion = input("Ingrese una descripción: ").strip()
    ciudades[nombre] = {"descripcion": descripcion}
    guardar_datos()
    print("Volcán agregado correctamente.")

def listar_volcanes():
    print("\nVolcanes ordenados alfabéticamente:")
    lista = list(ciudades.keys())
    quicksort(lista, 0, len(lista) - 1)
    for volcan in lista:
        print(f"- {volcan}")

def buscar_volcan():
    nombre = input("Ingrese el nombre del volcán a buscar: ").strip()
    lista = list(ciudades.keys())
    quicksort(lista, 0, len(lista) - 1)
    index = busqueda_binaria(lista, nombre)
    if index != -1:
        volcan = lista[index]
        print(f"\nVolcán encontrado: {volcan}")
        print(f"Descripción: {ciudades[volcan]['descripcion']}")
    else:
        print("Volcán no encontrado.")

def actualizar_volcan():
    nombre = input("Ingrese el nombre del volcán a actualizar: ").strip()
    if nombre not in ciudades:
        print("El volcán no existe.")
        return
    descripcion = input("Nueva descripción: ").strip()
    ciudades[nombre]['descripcion'] = descripcion
    guardar_datos()
    print("Volcán actualizado correctamente.")

def eliminar_volcan():
    nombre = input("Ingrese el nombre del volcán a eliminar: ").strip()
    if nombre not in ciudades:
        print("El volcán no existe.")
        return
    del ciudades[nombre]
    if nombre in grafo_rutas:
        del grafo_rutas[nombre]
    for origen in grafo_rutas:
        grafo_rutas[origen].pop(nombre, None)
    guardar_datos()
    print("Volcán eliminado correctamente.")

def seleccionar_volcanes():
    print("\nVolcanes disponibles:")
    listar_volcanes()
    seleccion = input("Ingrese los volcanes separados por coma: ").split(',')
    seleccion = [volcan.strip() for volcan in seleccion if volcan.strip() in ciudades]
    if not seleccion:
        print("No se seleccionaron volcanes válidos.")
        return []
    return seleccion

def guardar_itinerario_volcanico():
    volcanes = seleccionar_volcanes()
    if not volcanes:
        return
    nombre_archivo = input("Nombre del archivo de itinerario: ").strip()
    with open(f"itinerario_volcanes_{nombre_archivo}.txt", 'w') as f:
        for volcan in volcanes:
            datos = ciudades[volcan]
            f.write(f"{volcan}|{datos['descripcion']}\n")
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
