# Importación de módulos necesarios
import re  # Para expresiones regulares (validación)
from collections import defaultdict  # Para diccionarios con valores por defecto
# ESTRUCTURAS DE DATOS GLOBALES

usuarios = {}  # Diccionario para almacenar usuarios {email: datos}
ciudades = {}  # Diccionario para almacenar ciudades {nombre: datos}
grafo_rutas = defaultdict(dict)  # Grafo para conexiones entre ciudades
arbol_zonas = defaultdict(list)  # Árbol para organizar ciudades por zonas

Archivo_clientes = "usuarios.txt"  # Archivo para guardar usuarios
Archivo_RutasT = "rutas.txt"  # Archivo para guardar rutas y ciudades


def main():
    # Inicializa el sistema cargando datos y creando admin si no existe
    cargar_datos()  
    crear_admin_por_defecto()  
    
    # Muestra el menú principal
    mostrar_menu_principal()  

def cargar_datos():
    # Carga usuarios desde archivo txt
    try:
        with open(Archivo_clientes, 'r') as f:
            for linea in f:
                # Formato: email|nombre|apellido|id|edad|password|rol
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
        pass  # Si no existe el archivo, continúa sin datos
    
    # Carga ciudades y rutas desde archivo txt
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
                        # Formato: nombre|zona|descripcion
                        datos = linea.split('|')
                        if len(datos) >= 3:
                            ciudades[datos[0]] = {
                                'zona': datos[1],
                                'descripcion': '|'.join(datos[2:])
                            }
                    elif seccion == "rutas":
                        # Formato: origen|destino|distancia|costo
                        datos = linea.split('|')
                        if len(datos) == 4:
                            grafo_rutas[datos[0]][datos[1]] = {
                                'distancia': int(datos[2]),
                                'costo': float(datos[3])
                            }
                    elif seccion == "zonas":
                        # Formato: zona|ciudad1,ciudad2,...
                        datos = linea.split('|')
                        if len(datos) == 2:
                            arbol_zonas[datos[0]] = datos[1].split(',')
    except FileNotFoundError:
        pass  # Si no existe el archivo, continúa sin datos

def guardar_datos():
    # Guarda usuarios en archivo txt
    with open(Archivo_clientes, 'w') as f:
        for email, datos in usuarios.items():
            linea = f"{email}|{datos['nombre']}|{datos['apellido']}|{datos['identificacion']}|{datos['edad']}|{datos['password']}|{datos['rol']}\n"
            f.write(linea)
    
    # Guarda ciudades y rutas en archivo txt
    with open(Archivo_RutasT, 'w') as f:
        # Sección de ciudades
        f.write("[CIUDADES]\n")
        for ciudad, datos in ciudades.items():
            linea = f"{ciudad}|{datos['zona']}|{datos['descripcion']}\n"
            f.write(linea)
        
        # Sección de rutas
        f.write("\n[RUTAS]\n")
        for origen, destinos in grafo_rutas.items():
            for destino, datos in destinos.items():
                linea = f"{origen}|{destino}|{datos['distancia']}|{datos['costo']}\n"
                f.write(linea)
        
        # Sección de zonas
        f.write("\n[ZONAS]\n")
        for zona, lista_ciudades in arbol_zonas.items():
            linea = f"{zona}|{','.join(lista_ciudades)}\n"
            f.write(linea)

#Ingreso y validación de Administrador
def crear_admin_por_defecto():
    # Crea un usuario admin si no existe ninguno
    if not any(user.get('rol') == 'admin' for user in usuarios.values()):
        usuarios["admin@admin.com"] = {
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'identificacion': '0000000000',
            'edad': '30',
            'password': 'Admin123',  # Contraseña por defecto
            'rol': 'admin'
        }
        guardar_datos()

def registrar_usuario():
    # Registra un nuevo usuario
    print("\n--------- REGISTRO DE USUARIO ---------")
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    
    # Validación de email
    while True:
        email = input("Email: ").strip().lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("Formato de email inválido. Ejemplo: usuario@dominio.com")
            continue
        if email in usuarios:
            print("Este email ya está registrado.")
            continue
        break
    
    # Validación de contraseña segura
    while True:
        password = input("Contraseña debe tener 8+ caracteres, 1 mayúscula, 1 minúscula, 1 número: ")
        if (len(password) >= 8 and 
            any(c.isupper() for c in password) and 
            any(c.islower() for c in password) and 
            any(c.isdigit() for c in password)):
            break
        print("La contraseña no cumple los requisitos de seguridad.")
    
    # Guardar nuevo usuario
    usuarios[email] = {
        'nombre': nombre,
        'apellido': apellido,
        'identificacion': input("Identificación: ").strip(),
        'edad': input("Edad: ").strip(),
        'password': password,
        'rol': 'cliente'
    }
    
    guardar_datos()
    print(f"\nUsuario registrado exitosamente: {email}")

def iniciar_sesion():
    # Autenticación de usuarios
    print("\n------- INICIO DE SESIÓN -----------")
    email = input("Email: ").strip().lower()
    password = input("Contraseña: ")
    
    # Verificar credenciales
    if email in usuarios and usuarios[email]['password'] == password:
        print(f"\nBienvenido, {usuarios[email]['nombre']}!")
        if usuarios[email]['rol'] == 'admin':
            mostrar_menu_admin()
        else:
            mostrar_menu_cliente()
    else:
        print("Credenciales incorrectas.")

#Pagina Inicial del Sistema 
#Registro del Clinte o para inicio de sesión del Administrador
def mostrar_menu_principal():
    # Menú principal del sistema
    while True:
        print("\nBienvenidos al sistema de Rutas Turísticas")
        
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ").strip()
        print("\n\nSistema Creado por: ")
        
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            guardar_datos()
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

def mostrar_menu_admin():
    # Menú para administradores
    while True:
        print("\n*************** MENÚ ADMINISTRADOR *******************")
        print("1. Agregar ciudad")
        print("2. Listar ciudades")
        print("3. Buscar ciudad")
        print("4. Actualizar ciudad")
        print("5. Eliminar ciudad")
        print("6. Mostrar conexiones")
        print("7. Mostrar zonas")
        print("8. Regresar")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            agregar_ciudad()
        elif opcion == "2":
            listar_ciudades()
        elif opcion == "3":
            buscar_ciudad()
        elif opcion == "4":
            actualizar_ciudad()
        elif opcion == "5":
            eliminar_ciudad()
        elif opcion == "6":
            mostrar_conexiones()
        elif opcion == "7":
            mostrar_zonas()
        elif opcion == "8":
            break
        else:
            print("Opción no válida.")

def mostrar_menu_cliente():
    # Menú para clientes
    seleccion = []  # Lugares seleccionados para visitar
    
    while True:
        print("\n=== MENÚ CLIENTE ===")
        print("1. Ver mapa turístico")
        print("2. Consultar ruta óptima")
        print("3. Explorar por zonas")
        print("4. Seleccionar lugares")
        print("5. Ver mi selección")
        print("6. Guardar itinerario")
        print("7. Regresar")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            ver_mapa_turistico()
        elif opcion == "2":
            consultar_ruta_optima()
        elif opcion == "3":
            explorar_zonas()
        elif opcion == "4":
            seleccionar_lugares(seleccion)
        elif opcion == "5":
            ver_seleccion(seleccion)
        elif opcion == "6":
            guardar_itinerario(seleccion)
        elif opcion == "7":
            break
        else:
            print("Opción no válida.")

#Función que realiza el administrador 
def agregar_ciudad():
    # Agrega una nueva ciudad al sistema
    print("\n--- AGREGAR CIUDAD ---")
    nombre = input("Nombre: ").strip()
    
    if nombre in ciudades:
        print("Esta ciudad ya existe.")
        return
    
    zona = input("Zona: ").strip()
    descripcion = input("Descripción: ").strip()
    
    # Guardar ciudad
    ciudades[nombre] = {'zona': zona, 'descripcion': descripcion}
    
    # Agregar a zona
    if zona not in arbol_zonas:
        arbol_zonas[zona] = []
    arbol_zonas[zona].append(nombre)
    
    # Agregar conexiones
    while True:
        if input("\n¿Agregar conexión? (s/n): ").strip().lower() != 's':
            break
            
        destino = input("Ciudad destino: ").strip()
        if destino not in ciudades:
            print("La ciudad destino no existe.")
            continue
            
        try:
            distancia = int(input("Distancia (km): ").strip())
            costo = float(input("Costo: ").strip())
        except ValueError:
            print("Valores inválidos.")
            continue
        
        # Guardar conexión bidireccional
        grafo_rutas[nombre][destino] = {'distancia': distancia, 'costo': costo}
        grafo_rutas[destino][nombre] = {'distancia': distancia, 'costo': costo}
    
    guardar_datos()
    print(f"{nombre} agregada exitosamente.")

def listar_ciudades():
    # Lista todas las ciudades ordenadas
    print("\n----------- LISTA DE CIUDADES -------------")
    for ciudad in sorted(ciudades.keys()):
        datos = ciudades[ciudad]
        print(f"\n{ciudad}:")
        print(f"Zona: {datos['zona']}")
        print(f"Descripción: {datos['descripcion']}")
        
        # Mostrar conexiones
        if ciudad in grafo_rutas:
            print("Conexiones:")
            for destino, info in sorted(grafo_rutas[ciudad].items()):
                print(f"  - {destino}: {info['distancia']} km, ${info['costo']:.2f}")

def buscar_ciudad():
    # Busca ciudades por nombre
    print("\n---------- BUSCAR CIUDAD ---------")
    termino = input("Ingrese nombre o parte: ").strip().lower()
    
    encontradas = False
    for ciudad in ciudades:
        if termino in ciudad.lower():
            datos = ciudades[ciudad]
            print(f"\n{ciudad}:")
            print(f"Zona: {datos['zona']}")
            print(f"Descripción: {datos['descripcion']}")
            encontradas = True
    
    if not encontradas:
        print("No se encontraron ciudades.")

def actualizar_ciudad():
    # Actualiza datos de una ciudad
    print("\n------------- ACTUALIZAR CIUDAD ---------")
    nombre = input("Nombre de la ciudad: ").strip()
    
    if nombre not in ciudades:
        print("Ciudad no encontrada.")
        return
    
    datos = ciudades[nombre]
    print("\nDatos actuales:")
    print(f"Zona: {datos['zona']}")
    print(f"Descripción: {datos['descripcion']}")
    
    # Actualizar zona
    nueva_zona = input("\nNueva zona dejar vacío si premiere mantener la zona ").strip()
    if nueva_zona:
        # Actualizar árbol de zonas
        zona_anterior = datos['zona']
        arbol_zonas[zona_anterior].remove(nombre)
        
        if nueva_zona not in arbol_zonas:
            arbol_zonas[nueva_zona] = []
        arbol_zonas[nueva_zona].append(nombre)
        
        datos['zona'] = nueva_zona
    
    # Actualizar descripción
    nueva_desc = input("Nueva descripción dejar vacío para no cambiar: ").strip()
    if nueva_desc:
        datos['descripcion'] = nueva_desc
    
    guardar_datos()
    print("Ciudad actualizada.")

def eliminar_ciudad():
    # Elimina una ciudad del sistema
    print("\n----------- ELIMINAR CIUDAD -------------")
    nombre = input("Nombre de la ciudad: ").strip()
    
    if nombre not in ciudades:
        print("Ciudad no encontrada.")
        return
    
    # Eliminar de ciudades
    del ciudades[nombre]
    
    # Eliminar de zonas
    for zona, lista_ciudades in list(arbol_zonas.items()):
        if nombre in lista_ciudades:
            lista_ciudades.remove(nombre)
            if not lista_ciudades:
                del arbol_zonas[zona]
    
    # Eliminar conexiones
    if nombre in grafo_rutas:
        for destino in list(grafo_rutas[nombre].keys()):
            del grafo_rutas[destino][nombre]
        del grafo_rutas[nombre]
    
    guardar_datos()
    print("Ciudad eliminada.")

def mostrar_conexiones():
    # Muestra todas las conexiones entre ciudades
    print("\n--------- CONEXIONES-----------")
    for origen in sorted(grafo_rutas.keys()):
        for destino in sorted(grafo_rutas[origen].keys()):
            info = grafo_rutas[origen][destino]
            print(f"{origen} <-> {destino}: {info['distancia']} km, ${info['costo']:.2f}")

def mostrar_zonas():
    # Muestra el árbol de zonas y ciudades
    print("\n--------------- ZONAS ----------------")
    for zona in sorted(arbol_zonas.keys()):
        print(f"\nZona: {zona}")
        for ciudad in sorted(arbol_zonas[zona]):
            print(f"  - {ciudad}")

# Función para acceso de Clientes
def ver_mapa_turistico():
    # Muestra el mapa de lugares turísticos
    print("\n---------- MAPA TURÍSTICO ---------")
    print("Ciudades disponibles:")
    for ciudad in sorted(ciudades.keys()):
        print(f"- {ciudad}")
    
    print("\nConexiones:")
    mostrar_conexiones()

def consultar_ruta_optima():
    # Encuentra la ruta más económica entre dos ciudades (Dijkstra)
    print("\n--- RUTA ÓPTIMA ---")
    origen = input("Origen: ").strip()
    destino = input("Destino: ").strip()
    
    if origen not in ciudades or destino not in ciudades:
        print("Una o ambas ciudades no existen.")
        return
    
    # Inicialización
    distancias = {ciudad: float('inf') for ciudad in ciudades}
    predecesores = {ciudad: None for ciudad in ciudades}
    distancias[origen] = 0
    visitados = set()
    
    # Algoritmo de Dijkstra
    while True:
        # Ciudad no visitada con menor distancia
        ciudad_actual = None
        min_dist = float('inf')
        
        for ciudad in ciudades:
            if ciudad not in visitados and distancias[ciudad] < min_dist:
                min_dist = distancias[ciudad]
                ciudad_actual = ciudad
        
        if ciudad_actual is None or ciudad_actual == destino:
            break
        
        visitados.add(ciudad_actual)
        
        # Actualizar distancias de vecinos
        for vecino, info in grafo_rutas.get(ciudad_actual, {}).items():
            nueva_dist = distancias[ciudad_actual] + info['costo']
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                predecesores[vecino] = ciudad_actual
    
    # Reconstruir ruta
    if predecesores[destino] is None and origen != destino:
        print("No hay ruta disponible.")
        return
    
    ruta = []
    ciudad = destino
    while ciudad is not None:
        ruta.append(ciudad)
        ciudad = predecesores[ciudad]
    ruta.reverse()
    
    # Mostrar resultados
    print(f"\nRuta óptima de {origen} a {destino}:")
    print(" -> ".join(ruta))
    print(f"Costo total: ${distancias[destino]:.2f}")

def explorar_zonas():
    # Explora lugares por zonas
    print("\n--- EXPLORAR ZONAS ---")
    print("Zonas disponibles:")
    for zona in sorted(arbol_zonas.keys()):
        print(f"- {zona}")
    
    zona = input("\nSeleccione una zona: ").strip()
    if zona in arbol_zonas:
        print(f"\nLugares en {zona}:")
        for ciudad in sorted(arbol_zonas[zona]):
            print(f"- {ciudad}: {ciudades[ciudad]['descripcion']}")
    else:
        print("Zona no válida.")

def seleccionar_lugares(seleccion):
    # Selecciona lugares para visitar
    print("\n--- SELECCIONAR LUGARES ---")
    print("Lugares disponibles:")
    for ciudad in sorted(ciudades.keys()):
        print(f"- {ciudad}")
    
    while True:
        lugar = input("\nIngrese un lugar (o 'fin' para terminar): ").strip()
        if lugar.lower() == 'fin':
            break
        if lugar not in ciudades:
            print("Lugar no válido.")
            continue
        if lugar in seleccion:
            print("Ya está seleccionado.")
        else:
            seleccion.append(lugar)
            print(f"{lugar} agregado.")
    
    print("\nSelección actual:")
    ver_seleccion(seleccion)

def ver_seleccion(seleccion):
    # Muestra la selección actual de lugares
    if not seleccion:
        print("No ha seleccionado ningún lugar.")
        return
    
    print("\nLugares seleccionados:")
    for i, lugar in enumerate(sorted(seleccion), 1):
        print(f"{i}. {lugar}")

def guardar_itinerario(seleccion):
    # Guarda el itinerario en un archivo
    if len(seleccion) < 2:
        print("Seleccione al menos 2 lugares.")
        return
    
    email = input("Ingrese su email: ").strip().lower()
    if email not in usuarios:
        print("Email no registrado.")
        return
    
    # Calcular costo total
    costo_total = 0
    rutas = []
    
    for i in range(len(seleccion)-1):
        origen = seleccion[i]
        destino = seleccion[i+1]
        
        if origen in grafo_rutas and destino in grafo_rutas[origen]:
            costo = grafo_rutas[origen][destino]['costo']
            costo_total += costo
            rutas.append(f"{origen} -> {destino}: ${costo:.2f}")
        else:
            rutas.append(f"{origen} -> {destino}: No hay conexión directa")
    
    # Crear archivo de itinerario
    nombre_archivo = f"itinerario_{email.replace('@', '_')}.txt"
    with open(nombre_archivo, 'w') as f:
        f.write("------------- ITINERARIO DE VIAJE --------\n\n")
        f.write(f"Cliente: {usuarios[email]['nombre']}\n")
        f.write(f"Email: {email}\n\n")
        f.write("Lugares a visitar:\n")
        for lugar in sorted(seleccion):
            f.write(f"- {lugar}\n")
        
        f.write("\nRutas:\n")
        for ruta in rutas:
            f.write(f"{ruta}\n")
        
        f.write(f"\nCosto total estimado: ${costo_total:.2f}\n")
    
    print(f"Itinerario guardado en {nombre_archivo}")
    
main() 