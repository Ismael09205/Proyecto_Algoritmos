import heapq
from collections import defaultdict, deque

# Diccionarios globales
usuarios = {}
ciudades = {}
grafo_rutas = defaultdict(dict)
arbol_zonas = defaultdict(list)

# Archivos para persistencia
Archivo_clientes = "usuarios.txt"
Archivo_RutasT = "rutas.txt"

# Datos de volcanes (tu estructura original)
DATOS_VOLCANES = {
    "Chiles":[("Imbabura",160.2),("Cerro Negro",233.9)],
    "Cerro Negro":[("Chile",233.9),("Cotacachi",63.1)],
    "Cotacachi":[("Cerro Negro",63.1),("Imbabura",25.1),("Pululahua",85.3)],
    "Imbabura":[("Cotacachi",25.1),("Rucu Pichinca",104.2),("Chiles",160.2),("Reventado",165)],
    "Pululahua":[("Cotacachi",85.3),("Rucu Pichinca",25)],
    "Rucu Pichinca":[("Pululahua",25),("Imbabura",104.2),("Reventador",90),("Cotopaxi",100),("Guagua Pichincha",13)],
    "Guagua Pichincha":[("Rucu Pichinca",13),("Cotopaxi",109.8)],
    "Cotopaxi":[("Antisana",70),("Chimborazo",125.1),("Rucu Pichincha",100),("Guagua Pichincha",109.8)],
    "Reventador":[("Imbabura",165),("Rucu Pichinca",90),("Sumaco",77)],
    "Antisana":[("Cotopaxi",80),("Tungurahua",140),("Sumaco",50)],
    "Sumaco":[("Sumaco",50),("Tungurahua",170),("Reventador",77)],
    "Tungurahua":[("Altar",122.7),("Antisana",140),("Sumaco",170)],
    "Altar":[("Sangay",60),("Tungurahua",122.7)],
    "Sangay":[("Chimborazo",144),("Altar",60)],
    "Chimborazo":[("Cotopaxi",125.1),("Sangay",144)]
}

# === FUNCIONES PARA USUARIOS ===

def cargar_usuarios():
    try:
        with open(Archivo_clientes, 'r') as archivo_usuarios:
            for linea in archivo_usuarios:
                datos = linea.strip().split('|')
                if len(datos) == 7:
                    usuarios[datos[0]] = {
                        'nombre': datos[1],
                        'apellido': datos[2],    
                        'identificacion': datos[3],
                        'edad': datos[4],
                        'password': datos[5],
                        'rol': datos[6]
                    }
    except FileNotFoundError:
        pass

def guardar_usuarios():                          
    with open(Archivo_clientes, 'w') as archivo_usuarios:
        for email, datos in usuarios.items():
            linea = f"{email}|{datos['nombre']}|{datos['apellido']}|{datos['identificacion']}|{datos['edad']}|{datos['password']}|{datos['rol']}\n"
            archivo_usuarios.write(linea)

def es_contrasena_segura(password):
    tiene_mayuscula = any(c.isupper() for c in password)
    tiene_minuscula = any(c.islower() for c in password)
    tiene_numero = any(c.isdigit() for c in password)
    return len(password) >= 8 and tiene_mayuscula and tiene_minuscula and tiene_numero

def crear_admin_por_defecto():
    if "admin@admin.com" not in usuarios:
        usuarios["admin@admin.com"] = {
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'identificacion': '0000000000',
            'edad': '30',
            'password': 'Admin123',
            'rol': 'admin'
        }
        guardar_usuarios()

def registrar_usuario():
    print("\n--------- REGISTRO DE USUARIO ---------")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    while True:
        email = input("Email (ej. usuario@dominio.com): ").strip().lower()
        if "@" not in email or "." not in email:
            print("Email inválido. Debe contener '@' y '.'.")
            continue
        if email in usuarios:
            print("Este email ya está registrado.")
            continue
        break
    while True:
        password = input("Contraseña (mínimo 8 caracteres, una mayúscula, una minúscula, un número): ").strip()
        if es_contrasena_segura(password):
            break
        print("La contraseña no cumple los requisitos de seguridad.")
    identificacion = input("Identificación: ").strip()
    edad = input("Edad: ").strip()
    usuarios[email] = {
        'nombre': nombre,
        'apellido': apellido,
        'identificacion': identificacion,
        'edad': edad,
        'password': password,
        'rol': 'cliente'
    }
    guardar_usuarios()
    print(f"\nUsuario registrado exitosamente: {email}")
    input("Presiona ENTER para continuar...")

def iniciar_sesion():
    print("\n------- INICIO DE SESIÓN -----------")
    email = input("Email: ").strip().lower()
    password = input("Contraseña: ").strip()
    if email in usuarios and usuarios[email]['password'] == password:
        print(f"\nBienvenido, {usuarios[email]['nombre']}!")
        if usuarios[email]['rol'] == 'admin':
            mostrar_menu_admin()
        else:
            mostrar_menu_cliente()
    else:
        print("Credenciales incorrectas.")
        input("Presiona ENTER para continuar...")

def mostrar_menu_admin():
    print("Accediste como administrador (demo).")
    # Aquí puedes poner opciones de admin para manejar volcanes, rutas, usuarios...

def mostrar_menu_cliente():
    print("Accediste como cliente (demo).")
    # Opciones para clientes...

# === FUNCIONES PARA VOLCANES Y RUTAS ===

def cargar_datos():
    # Carga datos de volcanes, ciudades, rutas y zonas desde archivo
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

def guardar_datos_volcanes():
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
    if not ciudades:
        # Carga los volcanes desde DATOS_VOLCANES
        for volcan, conexiones in DATOS_VOLCANES.items():
            if volcan not in ciudades:
                ciudades[volcan] = {"zona": "Zona1", "descripcion": "Volcán en Ecuador"}
            for vecino, distancia in conexiones:
                costo = distancia * 0.3
                grafo_rutas[volcan][vecino] = {'distancia': distancia, 'costo': costo}
        guardar_datos_volcanes()
        print("Datos de la Ruta de los Volcanes cargados exitosamente.")

# === NUEVAS FUNCIONES DE VOLCANES ===

def agregar_volcan():
    nombre = input("Ingrese el nombre del volcán: ").strip()
    if nombre in ciudades:
        print("El volcán ya existe.")
        return
    descripcion = input("Ingrese una descripción: ").strip()
    ciudades[nombre] = {"zona": "Zona1", "descripcion": descripcion}
    guardar_datos_volcanes()
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
    guardar_datos_volcanes()
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
    guardar_datos_volcanes()
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

def ruta_mas_corta():
    if not grafo_rutas:
        print("No hay rutas cargadas.")
        return

    print("\n--- Ruta más corta entre volcanes ---")
    listar_volcanes()
    origen = input("Ingrese el volcán de origen: ").strip()
    destino = input("Ingrese el volcán de destino: ").strip()

    if origen not in grafo_rutas or destino not in ciudades:
        print("Uno o ambos volcanes no existen.")
        return

    # Algoritmo de Dijkstra
    distancias = {volcan: float('inf') for volcan in ciudades}
    anteriores = {volcan: None for volcan in ciudades}
    distancias[origen] = 0
    heap = [(0, origen)]

    while heap:
        distancia_actual, actual = heapq.heappop(heap)

        if actual == destino:
            break

        for vecino, datos in grafo_rutas.get(actual, {}).items():
            nueva_distancia = distancia_actual + datos['distancia']
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                anteriores[vecino] = actual
                heapq.heappush(heap, (nueva_distancia, vecino))

    if distancias[destino] == float('inf'):
        print("No hay ruta disponible entre los volcanes.")
        return

    # Reconstruir el camino
    camino = []
    actual = destino
    while actual:
        camino.insert(0, actual)
        actual = anteriores[actual]

    print("\nRuta más corta encontrada:")
    print(" -> ".join(camino))
    print(f"Distancia total: {distancias[destino]:.2f} km")
    
    # Costo total
    costo_total = sum(grafo_rutas[camino[i]][camino[i+1]]['costo'] for i in range(len(camino) - 1))
    print(f"Costo total aproximado: ${costo_total:.2f}")

def mostrar_menu_admin():
    while True:
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Agregar volcán")
        print("2. Listar volcanes")
        print("3. Buscar volcán")
        print("4. Actualizar volcán")
        print("5. Eliminar volcán")
        print("6. Guardar itinerario")
        print("7. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            agregar_volcan()
        elif opcion == "2":
            listar_volcanes()
        elif opcion == "3":
            buscar_volcan()
        elif opcion == "4":
            actualizar_volcan()
        elif opcion == "5":
            eliminar_volcan()
        elif opcion == "6":
            guardar_itinerario_volcanico()
        elif opcion == "7":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")

def mostrar_menu_cliente():
    while True:
        print("\n--- MENÚ CLIENTE ---")
        print("1. Ver lista de volcanes")
        print("2. Buscar volcán")
        print("3. Guardar itinerario")
        print("4. Ver ruta más corta entre volcanes")
        print("5. Cerrar sesión")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            listar_volcanes()
        elif opcion == "2":
            buscar_volcan()
        elif opcion == "3":
            guardar_itinerario_volcanico()
        elif opcion == "4":
            ruta_mas_corta()
        elif opcion == "5":
            print("Sesión cerrada.")
            break
        else:
            print("Opción no válida.")


def main():
    cargar_usuarios()
    crear_admin_por_defecto()
    cargar_datos()
    cargar_datos_volcanes()

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Iniciar sesión")
        print("2. Registrar usuario")
        print("3. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            iniciar_sesion()
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
