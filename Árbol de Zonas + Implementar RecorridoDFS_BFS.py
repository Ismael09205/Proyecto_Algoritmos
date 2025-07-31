from collections import deque

print("Melva Suarez")

# Datos de volcanes organizados en un diccionario
Datos_Volcanes = {
    "Zonas": {
        "Norte": ["Cotopaxi", "Cayambe", "Antisana"],
        "Centro": ["Tungurahua", "Chimborazo", "Altar"],
        "Sur": ["Sangay", "Tungurahua", "Chimborazo"]
    },
    "Ciudades": {
        "Cotopaxi": {
            "zona": "Norte",
            "descripcion": "Volcán activo más alto del mundo (5,897 m). Parque Nacional Cotopaxi."
        },
        "Cayambe": {
            "zona": "Norte",
            "descripcion": "Volcán con glaciar en la línea ecuatorial (5,790 m). Reserva Ecológica Cayambe-Coca."
        },
        "Antisana": {
            "zona": "Norte",
            "descripcion": "Volcán con forma de cono truncado (5,753 m). Reserva Ecológica Antisana."
        },
        "Tungurahua": {
            "zona": "Centro",
            "descripcion": "Volcán activo conocido como 'Gigante Negro' (5,023 m). Parque Nacional Sangay."
        },
        "Chimborazo": {
            "zona": "Centro",
            "descripcion": "Punto más alejado del centro de la Tierra (6,263 m). Reserva de Producción Faunística Chimborazo."
        },
        "Altar": {
            "zona": "Centro",
            "descripcion": "También llamado Capac Urcu, con forma de herradura (5,319 m). Parque Nacional Sangay."
        },
        "Sangay": {
            "zona": "Sur",
            "descripcion": "Uno de los volcanes más activos del mundo (5,230 m). Parque Nacional Sangay."
        }
    },
    "Rutas": [
        ["Cotopaxi", "Antisana", 85, 25.50],
        ["Cotopaxi", "Cayambe", 120, 35.75],
        ["Antisana", "Cayambe", 95, 28.25],
        ["Tungurahua", "Chimborazo", 65, 20.00],
        ["Tungurahua", "Altar", 80, 22.50],
        ["Chimborazo", "Altar", 70, 21.00],
        ["Tungurahua", "Sangay", 110, 32.00],
        ["Chimborazo", "Sangay", 90, 27.50]
    ]
}


ciudades = {}
arbol_zonas = {}
grafo_rutas = {}

def cargar_datos_volcanes():
    if not ciudades:
        for nombre, datos in Datos_Volcanes["Ciudades"].items():
            ciudades[nombre] = datos  # Añade el volcán al diccionario de ciudades
            zona = datos['zona']  # Obtiene la zona del volcán
            
            # Asegura que la zona exista en el árbol
            if zona not in arbol_zonas:
                arbol_zonas[zona] = []  # Crea lista vacía para la zona
                
            # Evita duplicados en la zona
            if nombre not in arbol_zonas[zona]:
                arbol_zonas[zona].append(nombre)  # Añade volcán a su zona
        
        # Carga las rutas entre volcanes
        for ruta in Datos_Volcanes["Rutas"]:
            origen, destino, distancia, costo = ruta
            # Añade conexión bidireccional al grafo
            if origen not in grafo_rutas:
                grafo_rutas[origen] = {}
            if destino not in grafo_rutas:
                grafo_rutas[destino] = {}
            grafo_rutas[origen][destino] = {'distancia': distancia, 'costo': costo}
            grafo_rutas[destino][origen] = {'distancia': distancia, 'costo': costo}
        
        guardar_datos()  
        print("Datos de la Ruta de los Volcanes cargados exitosamente.")

def mostrar_zonas():
    print("\n--------------- ZONAS ----------------")
    

    print("\n1. Recorrido tradicional (for):")
    for zona in sorted(arbol_zonas.keys()):  
        print(f"\nZona: {zona}")
        for ciudad in sorted(arbol_zonas[zona]):
            print(f"  - {ciudad}")
    

    print("\n2. Recorrido BFS (por niveles):")
    recorrido_bfs()  # Llama a la función BFS
    

    print("\n3. Recorrido DFS (en profundidad):")
    recorrido_dfs()  
def recorrido_bfs():
    if not arbol_zonas:  
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

            for ciudad in sorted(arbol_zonas.get(zona_actual, [])):
                print(f"  - {ciudad}")
        
        nivel += 1

def recorrido_dfs():
    if not arbol_zonas:  # Validación de datos
        print("No hay zonas registradas.")
        return
    
    visitados = set()  # Nodos visitados
    pila = []         # Pila para manejar el orden de visita
    

    for zona in sorted(arbol_zonas.keys()):
        if zona not in visitados:
            pila.append(zona)  
            visitados.add(zona)
            
            while pila:
                zona_actual = pila.pop()  
                print(f"\nZona: {zona_actual}")
                

                for ciudad in sorted(arbol_zonas.get(zona_actual, [])):
                    print(f"  - {ciudad}")

def explorar_zonas():
    print("\n--- EXPLORAR ZONAS ---")  # Muestra lista de zonas disponibles
    print("Zonas disponibles:")
    for zona in sorted(arbol_zonas.keys()):
        print(f"- {zona}")
    
    print("\nOpciones de exploración:")
    print("1. Ver ciudades de una zona")
    print("2. Recorrido en profundidad")
    print("3. Recorrido por niveles")
    
    opcion = input("\nSeleccione una opción 1-3: ").strip()
    
    if opcion == "1": 
        zona = input("\nSeleccione una zona: ").strip()
        if zona in arbol_zonas:
            print(f"\nLugares en {zona}:")
            for ciudad in sorted(arbol_zonas[zona]):
                print(f"- {ciudad}: {ciudades[ciudad]['descripcion']}")
        else:
            print("Zona no válida.")
    elif opcion == "2": 
        print("\nRecorrido DFS de todas las zonas:")
        recorrido_dfs_exploratorio()
    elif opcion == "3":
        print("\nRecorrido BFS de todas las zonas:")
        recorrido_bfs_exploratorio()
    else:
        print("Opción no válida.")

def recorrido_dfs_exploratorio():
    visitados = set()
    pila = []
    
    for zona in sorted(arbol_zonas.keys()):  # Apila tuplas (tipo, nombre) para diferenciar zonas/ciudades
        if zona not in visitados:
            pila.append(("zona", zona))
            visitados.add(zona)
            
            while pila:
                tipo, actual = pila.pop()
                if tipo == "zona":
                    print(f"\nExplorando Zona: {actual}")  # Apilar ciudades en orden inverso para procesar en orden correcto
                    for ciudad in reversed(sorted(arbol_zonas.get(actual, []))):
                        pila.append(("ciudad", ciudad))
                else:
                    print(f"- {actual}: {ciudades[actual]['descripcion']}")

def recorrido_bfs_exploratorio():
    visitados = set()
    cola = deque()
    
    for zona in sorted(arbol_zonas.keys()):
        if zona not in visitados:

            cola.append(("zona", zona))
            visitados.add(zona)
    
    nivel = 0
    while cola:
        print(f"\nNivel {nivel}:")
        nivel_size = len(cola)
        
        for _ in range(nivel_size):
            tipo, actual = cola.popleft()
            
            if tipo == "zona":
                print(f"Zona: {actual}")

                for ciudad in sorted(arbol_zonas.get(actual, [])):
                    cola.append(("ciudad", ciudad))
            else:  
                print(f"- {actual}: {ciudades[actual]['descripcion']}")
        
        nivel += 1

def main():
    cargar_datos() 
    cargar_datos_volcanes()
    crear_admin_por_defecto()
    mostrar_menu_principal()
