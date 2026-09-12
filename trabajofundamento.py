
def menu_interactivo():

    while True:
        print("\n=== Prueba de viabilidad: menú ===")
        print("1. Validar DNI")
        print("2. Validar RUC")
        print("3. Validar XML reducido")
        print("4. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion in ("1", "2", "3"):
            cadena = input("Escribe la cadena a validar: ")
            probar_cadena(opcion, cadena)
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

#QUE FACIL EL MENU
def probar_cadena(tipo, cadena):

    funciones = {
        "1": ("DNI", validar_dni),
        "2": ("RUC", validar_ruc),
        "3": ("XML reducido", validar_xml_reducido),
    }
    nombre, funcion = funciones[tipo]
    try:
        funcion(cadena)
        print(f"[{nombre}] {cadena!r}: VÁLIDO")
    except (TypeError, ValueError) as error:
        print(f"[{nombre}] {cadena!r}: INVÁLIDO -> {error}")


def validar_dni(dni):

    if not isinstance(dni, str):
        raise TypeError("El DNI debe ser un string")

    dni = dni.strip()
    if not dni.isascii() or not dni.isdigit():
        raise ValueError("El DNI debe contener únicamente dígitos ASCII")
    if len(dni) != 8:
        raise ValueError("El DNI debe tener exactamente 8 dígitos")
    return True


def validar_ruc(ruc):
    
    if not isinstance(ruc, str):
        raise TypeError("El RUC debe ser un string")

    ruc = ruc.strip()
    if not ruc.isascii() or not ruc.isdigit():
        raise ValueError("El RUC debe contener únicamente dígitos ASCII")
    if len(ruc) != 11:
        raise ValueError("El RUC debe tener exactamente 11 dígitos")

    prefijos_validos = ("10", "15", "16", "17", "20")
    if not ruc.startswith(prefijos_validos):
        raise ValueError("El RUC debe iniciar con un prefijo válido (10/15/16/17/20)")

    factores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    base = ruc[:10]
    digito_verificador = int(ruc[-1])

    suma = 0
    for caracter, factor in zip(base, factores):
        suma += int(caracter) * factor

    resto = suma % 11
    digito_calculado = 11 - resto
    if digito_calculado == 10:
        digito_calculado = 0
    elif digito_calculado == 11:
        digito_calculado = 1

    if digito_calculado != digito_verificador:
        raise ValueError("El dígito verificador del RUC (módulo 11) no coincide")

    return True

#CEREBRO EN CRISIS
def validar_xml_reducido(cadena):
   
    if not isinstance(cadena, str):
        raise TypeError("El XML debe ser un string")

    cadena = cadena.strip()
    if not cadena.isascii():
        raise ValueError("El XML reducido debe contener únicamente caracteres ASCII")
    if not cadena.startswith("<") or not cadena.endswith(">"):
        raise ValueError("El XML reducido debe empezar con '<' y terminar con '>'")

    # Separar en: apertura, contenido, cierre
    partes = cadena.split(">", 1)
    if len(partes) != 2:
        raise ValueError("No se encontró una etiqueta de apertura válida")

    etiqueta_apertura = partes[0] + ">"
    resto = partes[1]

    nombre_etiqueta = etiqueta_apertura.strip("<>")
    if len(nombre_etiqueta) == 0:
        raise ValueError("La etiqueta de apertura no puede estar vacía")

    etiqueta_cierre_esperada = "</" + nombre_etiqueta + ">"
    if not resto.endswith(etiqueta_cierre_esperada):
        raise ValueError("La etiqueta de cierre no coincide con la de apertura")

    return True


if __name__ == "__main__":
    menu_interactivo()

#AVECES ME DA GANAS DE CAMBIARME DE CARRERA 