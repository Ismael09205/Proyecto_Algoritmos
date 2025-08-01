
import heapq
from collections import defaultdict, deque


usuarios = {}
ciudades = {}
grafo_rutas = defaultdict(dict)
arbol_zonas = defaultdict(list)

# Archivos para persistencia
Archivo_clientes = "usuarios.txt"
Archivo_RutasT = "rutas.txt"

# Datos de los volcanes de Ecuador
DATOS_VOLCANES = {
    "Zonas": {
        "Norte": ["Cotacachi", "Imbabura", "Chiles"],
        "Centro": ["Cotopaxi", "Antisana", "Tungurahua"],
        "Sur": ["Chimborazo", "Sangay", "Altar"]
    },
    "Ciudades": {
        "Chiles": {
            "zona": "Norte",
            "descripcion": "Volcán en la frontera con Colombia. Altura: 4,723 m",
            "altura": 4723
        },
        "Cotacachi": {
            "zona": "Norte",
            "descripcion": "Volcán en la reserva ecológica. Altura: 4,944 m",
            "altura": 4944
        },
        "Imbabura": {
            "zona": "Norte",
            "descripcion": "Volcán inactivo conocido como 'Taita Imbabura'. Altura: 4,630 m",
            "altura": 4630
        },
        "Cotopaxi": {
            "zona": "Centro",
            "descripcion": "Volcán activo más alto del mundo. Altura: 5,897 m",
            "altura": 5897
        },
        "Antisana": {
            "zona": "Centro",
            "descripcion": "Volcán con glaciar importante. Altura: 5,753 m",
            "altura": 5753
        },
        "Tungurahua": {
            "zona": "Centro",
            "descripcion": "Volcán activo conocido como 'Gigante Negro'. Altura: 5,023 m",
            "altura": 5023
        },
        "Chimborazo": {
            "zona": "Sur",
            "descripcion": "Punto más alejado del centro de la Tierra. Altura: 6,263 m",
            "altura": 6263
        },
        "Sangay": {
            "zona": "Sur",
            "descripcion": "Uno de los volcanes más activos del mundo. Altura: 5,230 m",
            "altura": 5230
        },
        "Altar": {
            "zona": "Sur",
            "descripcion": "También llamado Capac Urcu. Altura: 5,319 m",
            "altura": 5319
        }
    },
    "Rutas": [
        ["Chiles", "Imbabura", 160.2],
        ["Chiles", "Cotacachi", 233.9],
        ["Cotacachi", "Imbabura", 25.1],
        ["Cotopaxi", "Antisana", 70],
        ["Cotopaxi", "Chimborazo", 125.1],
        ["Tungurahua", "Altar", 122.7],
        ["Sangay", "Altar", 60],
        ["Sangay", "Chimborazo", 144],
        ["Antisana", "Tungurahua", 140]
    ]
}

def cargar_datos():
    """Carga datos desde archivos"""
    try:
        with open(Archivo_clientes, 'r') as f:
            for linea in f:
                datos = linea.strip().split('|')
                if len(datos) == 7:
                    usuarios[datos[0]] = {
                        'nombre': datos[1], 'apellido': datos[2],
                        'identificacion': datos[3], 'edad': datos[4],
                        'password': datos[5], 'rol': datos[6]
                    }
    except FileNotFoundError:
        pass

    try:
        with open(Archivo_RutasT, 'r') as f:
            seccion = None
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                if linea == "[CIUDADES]":
                    seccion = "ciudades"
                elif linea == "[RUTAS]":
                    seccion = "rutas"
                elif linea == "[ZONAS]":
                    seccion = "zonas"
                else:
                    if seccion == "ciudades":
                        datos = linea.split('|')
                        if len(datos) >= 3:
                            ciudades[datos[0]] = {
                                'zona': datos[1],
                                'descripcion': '|'.join(datos[2:])
                            }
                    elif seccion == "rutas":
                        datos = linea.split('|')
                        if len(datos) == 4:
                            origen, destino, distancia, costo = datos
                            grafo_rutas[origen][destino] = {
                                'distancia': float(distancia),
                                'costo': float(costo)
                            }
                    elif seccion == "zonas":
                        datos = linea.split('|')
                        if len(datos) == 2:
                            arbol_zonas[datos[0]] = datos[1].split(',')
    except FileNotFoundError:
        pass

def guardar_datos():
    """Guarda datos en archivos"""
    with open(Archivo_clientes, 'w') as f:
        for email, datos in usuarios.items():
            linea = f"{email}|{datos['nombre']}|{datos['apellido']}|{datos['identificacion']}|{datos['edad']}|{datos['password']}|{datos['rol']}\n"
            f.write(linea)
    
    with open(Archivo_RutasT, 'w') as f:
        f.write("[CIUDADES]\n")
        for ciudad, datos in ciudades.items():
            linea = f"{ciudad}|{datos['zona']}|{datos['descripcion']}\n"
            f.write(linea)
        
        f.write("\n[RUTAS]\n")
        for origen, destinos in grafo_rutas.items():
            for destino, info in destinos.items():
                linea = f"{origen}|{destino}|{info['distancia']}|{info['costo']}\n"
                f.write(linea)
        
        f.write("\n[ZONAS]\n")
        for zona, lista_ciudades in arbol_zonas.items():
            linea = f"{zona}|{','.join(lista_ciudades)}\n"
            f.write(linea)

def cargar_datos_volcanes():
    """Carga datos iniciales de volcanes si no existen"""
    if not ciudades:
        for nombre, datos in DATOS_VOLCANES["Ciudades"].items():
            ciudades[nombre] = datos
            zona = datos['zona']
            if zona not in arbol_zonas:
                arbol_zonas[zona] = []
            if nombre not in arbol_zonas[zona]:
                arbol_zonas[zona].append(nombre)
        
        for ruta in DATOS_VOLCANES["Rutas"]:
            origen, destino, distancia = ruta
            costo = distancia * 0.3  # Costo estimado basado en distancia
            grafo_rutas[origen][destino] = {'distancia': distancia, 'costo': costo}
            grafo_rutas[destino][origen] = {'distancia': distancia, 'costo': costo}
        
        guardar_datos()
        print("Datos de la Ruta de los Volcanes cargados exitosamente.")

def dijkstra(origen, destino):
    """Implementación del algoritmo de Dijkstra para rutas óptimas"""
    distancias = {ciudad: float('inf') for ciudad in ciudades}
    predecesores = {ciudad: None for ciudad in ciudades}
    distancias[origen] = 0
    cola = [(0, origen)]
    
    while cola:
        distancia_actual, ciudad_actual = heapq.heappop(cola)
        
        if ciudad_actual == destino:
            break
        
        if distancia_actual > distancias[ciudad_actual]:
            continue
        
        for vecino, datos in grafo_rutas.get(ciudad_actual, {}).items():
            distancia = distancia_actual + datos['costo']
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                predecesores[vecino] = ciudad_actual
                heapq.heappush(cola, (distancia, vecino))
    
    # Reconstruir ruta
    if predecesores[destino] is None and origen != destino:
        return None, float('inf')
    
    ruta = []
    ciudad = destino
    while ciudad is not None:
        ruta.append(ciudad)
        ciudad = predecesores[ciudad]
    ruta.reverse()
    
    return ruta, distancias[destino]

def recorrido_bfs():
    """Recorrido Breadth-First Search del árbol de zonas"""
    if not arbol_zonas:
        print("No hay zonas registradas.")
        return
    
    visitados = set()
    cola = deque()
    
    for zona in sorted(arbol_zonas.keys()):
        if zona not in visitados:
            cola.append(zona)
            visitados.add(zona)
    
    nivel = 0
    while cola:
        print(f"\nNivel {nivel}:")
        nivel_size = len(cola)
        
        for _ in range(nivel_size):
            zona_actual = cola.popleft()
            print(f"Zona: {zona_actual}")
            
            for ciudad in sorted(arbol_zonas[zona_actual]):
                print(f"  - {ciudad}")
        
        nivel += 1

def recorrido_dfs():
    """Recorrido Depth-First Search del árbol de zonas"""
    if not arbol_zonas:
        print("No hay zonas registradas.")
        return
    
    visitados = set()
    pila = []
    
    for zona in sorted(arbol_zonas.keys()):
        if zona not in visitados:
            pila.append(zona)
            visitados.add(zona)
            
            while pila:
                zona_actual = pila.pop()
                print(f"\nZona: {zona_actual}")
                
                for ciudad in sorted(arbol_zonas[zona_actual]):
                    print(f"  - {ciudad}")

def mostrar_menu_volcanes():
    """Menú específico para la Ruta de los Volcanes"""
    while True:
        print("\n=== RUTA DE LOS VOLCANES ===")
        print("1. Ver volcanes por zona")
        print("2. Recorrido BFS por zonas")
        print("3. Recorrido DFS por zonas")
        print("4. Consultar ruta óptima entre volcanes")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\nVolcanes por zona:")
            for zona in sorted(arbol_zonas.keys()):
                print(f"\nZona {zona}:")
                for volcan in sorted(arbol_zonas[zona]):
                    print(f"- {volcan} ({ciudades[volcan]['altura']} m)")
        
        elif opcion == "2":
            print("\nRecorrido BFS:")
            recorrido_bfs()
        
        elif opcion == "3":
            print("\nRecorrido DFS:")
            recorrido_dfs()
        
        elif opcion == "4":
            print("\nVolcanes disponibles:")
            for volcan in sorted(ciudades.keys()):
                print(f"- {volcan}")
            
            origen = input("\nIngrese el volcán de origen: ").strip()
            destino = input("Ingrese el volcán de destino: ").strip()
            
            if origen in ciudades and destino in ciudades:
                ruta, costo = dijkstra(origen, destino)
                if ruta:
                    print(f"\nRuta óptima: {' -> '.join(ruta)}")
                    print(f"Costo total estimado: ${costo:.2f}")
                else:
                    print("No hay ruta disponible entre estos volcanes.")
            else:
                print("Uno o ambos volcanes no existen en el sistema.")
        
        elif opcion == "5":
            break
        
        else:
            print("Opción no válida.")


def main():
    
    cargar_datos()
    cargar_datos_volcanes()
    
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

#  Algoritmo de ordenamiento manual: QuickSort
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
