# Diccionario global para almacenar los usuarios registrados, usando el email como clave
usuarios = {}

# Nombre del archivo donde se guardarán los datos de los usuarios
Archivo_clientes = "usuarios.txt"

# Función para cargar los usuarios existentes desde el archivo
def cargar_datos():
    try:
        # Abre el archivo en modo lectura
        with open(Archivo_clientes, 'r') as archivo_usuarios:
            # Lee cada línea del archivo
            for linea in archivo_usuarios:
                # Divide la línea por el carácter separador "|"
                datos = linea.strip().split('|')
                # Verifica que haya exactamente 7 datos por línea
                if len(datos) == 7:
                    # Agrega al diccionario 'usuarios' con email como clave
                    usuarios[datos[0]] = {
                        'nombre': datos[1],
                        'apellido': datos[2],    
                        'identificacion': datos[3],
                        'edad': datos[4],
                        'password': datos[5],
                        'rol': datos[6]
                    }
    # Si el archivo no existe aún, se ignora el error y continúa
    except FileNotFoundError:
        pass
                              
# Función para guardar los usuarios actuales en el archivo
def guardar_datos():                            
    # Abre el archivo en modo escritura (sobrescribe)
    with open(Archivo_clientes, 'w') as archivo_usuarios:
        # Recorre cada usuario guardado en el diccionario
        for email, datos in usuarios.items():
            # Construye la línea de texto con formato específico
            linea = f"{email}|{datos['nombre']}|{datos['apellido']}|{datos['identificacion']}|{datos['edad']}|{datos['password']}|{datos['rol']}\n"
            # Escribe la línea en el archivo
            archivo_usuarios.write(linea)

# Función que verifica si una contraseña es segura
def es_contrasena_segura(password):
    # Variables auxiliares para verificar requisitos de seguridad
    tiene_mayuscula = False
    tiene_minuscula = False
    tiene_numero = False

    # Recorre cada carácter de la contraseña
    for c in password:
        if c.isupper():
            tiene_mayuscula = True
        elif c.islower():
            tiene_minuscula = True
        elif c.isdigit():
            tiene_numero = True

    # Devuelve True si cumple todos los requisitos
    return len(password) >= 8 and tiene_mayuscula and tiene_minuscula and tiene_numero

# Función que crea un administrador por defecto si no existe ya
def crear_admin_por_defecto():
    # Verifica si el admin con email "admin@admin.com" ya está creado
    if "admin@admin.com" not in usuarios:
        # Si no está, se lo agrega al diccionario con datos por defecto
        usuarios["admin@admin.com"] = {
            'nombre': 'Admin',
            'apellido': 'Sistema',
            'identificacion': '0000000000',
            'edad': '30',
            'password': 'Admin123',
            'rol': 'admin'
        }
        # Guarda en el archivo
        guardar_datos()

# Función para registrar un nuevo usuario (cliente)
def registrar_usuario():
    print("\n--------- REGISTRO DE USUARIO ---------")
    # Solicita nombre y apellido del usuario
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()

    # Solicita y valida el email
    while True:
        email = input("Email (ej. usuario@dominio.com): ").strip().lower()
        # Verificación básica del formato (contiene "@" y ".")
        if "@" not in email or "." not in email:
            print("Email inválido. Debe contener '@' y '.'.")
            continue
        # Verifica si ya existe ese email registrado
        if email in usuarios:
            print("Este email ya está registrado.")
            continue
        break  # Sale del ciclo si el email es válido

    # Solicita y valida la contraseña
    while True:
        password = input("Contraseña (mínimo 8 caracteres, una mayúscula, una minúscula, un número): ").strip()
        if es_contrasena_segura(password):
            break  # Sale del ciclo si la contraseña es segura
        print("La contraseña no cumple los requisitos de seguridad.")

    # Solicita la identificación y edad
    identificacion = input("Identificación: ").strip()
    edad = input("Edad: ").strip()

    # Se almacena el nuevo usuario en el diccionario
    usuarios[email] = {
        'nombre': nombre,
        'apellido': apellido,
        'identificacion': identificacion,
        'edad': edad,
        'password': password,
        'rol': 'cliente'
    }

    # Guarda el usuario en el archivo
    guardar_datos()
    print(f"\n✅ Usuario registrado exitosamente: {email}")
    input("Presiona ENTER para continuar...")

# Función que permite iniciar sesión
def iniciar_sesion():
    print("\n------- INICIO DE SESIÓN -----------")
    # Solicita credenciales
    email = input("Email: ").strip().lower()
    password = input("Contraseña: ").strip()

    # Verifica si el email existe y la contraseña es correcta
    if email in usuarios and usuarios[email]['password'] == password:
        # Muestra mensaje de bienvenida
        print(f"\nBienvenido, {usuarios[email]['nombre']}!")
        # Según el rol, redirige a menú de admin o cliente
        if usuarios[email]['rol'] == 'admin':
            mostrar_menu_admin()
        else:
            mostrar_menu_cliente()
    else:
        print("Credenciales incorrectas.")
        input("Presiona ENTER para continuar...")

# Menú simulado para administrador
def mostrar_menu_admin():
    print("Accediste como administrador (demo).")

# Menú simulado para cliente
def mostrar_menu_cliente():               
    print("Accediste como cliente (demo).")