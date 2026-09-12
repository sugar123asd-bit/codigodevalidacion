"""
Prueba de viabilidad del componente más incierto
Validaciones: DNI, RUC (académico, con dígito verificador módulo 11)
y XML reducido.

Solo se usan las "instrucciones básicas" indicadas en el informe:
strip(), split(), isinstance(), isascii(), isdigit(), len(),
startswith() / endswith()asdasdasdasdasfadfdsbgf hxbvhbfsduifbwdjfbnvjscbvhsdbfjdsbjhvcfvbschgbcvjwsdbfjusd
"""


def validar_dni(dni):
    """Valida un DNI peruano: exactamente 8 dígitos ASCII."""
    if not isinstance(dni, str):
        raise TypeError("El DNI debe ser un string")

    dni = dni.strip()
    if not dni.isascii() or not dni.isdigit():
        raise ValueError("El DNI debe contener únicamente dígitos ASCII")
    if len(dni) != 8:
        raise ValueError("El DNI debe tener exactamente 8 dígitos")
    return True


def validar_ruc(ruc):
    """
    Valida un RUC peruano:
    - 11 dígitos ASCII.
    - Comienza con un prefijo válido (10, 15, 16, 17 o 20).
    - El dígito verificador (módulo 11) debe coincidir con el último dígito.
    """
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

    # Cálculo del dígito verificador (módulo 11)
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


def validar_xml_reducido(cadena):
    """
    Valida una cadena XML reducida con la forma: <etiqueta>contenido</etiqueta>
    No valida XML general ni UBL 2.1 (fuera del alcance del informe).
    """
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


def ejecutar_pruebas_automaticas():
    """Corre una tanda fija de casos y muestra el resultado (evidencia solicitada)."""
    casos_dni = ["12345678", "1234567", "1234567a", " 12345678 "]
    casos_ruc = ["20000000001", "20123456789", "30123456789", "2012345678a"]
    casos_xml = ["<factura>123</factura>", "<a>texto</b>", "sin etiquetas"]

    print("--- Pruebas DNI ---")
    for caso in casos_dni:
        try:
            validar_dni(caso)
            print(f"{caso!r}: VÁLIDO")
        except (TypeError, ValueError) as error:
            print(f"{caso!r}: INVÁLIDO -> {error}")

    print("\n--- Pruebas RUC ---")
    for caso in casos_ruc:
        try:
            validar_ruc(caso)
            print(f"{caso!r}: VÁLIDO")
        except (TypeError, ValueError) as error:
            print(f"{caso!r}: INVÁLIDO -> {error}")

    print("\n--- Pruebas XML reducido ---")
    for caso in casos_xml:
        try:
            validar_xml_reducido(caso)
            print(f"{caso!r}: VÁLIDO")
        except (TypeError, ValueError) as error:
            print(f"{caso!r}: INVÁLIDO -> {error}")


def probar_cadena(tipo, cadena):
    """Llama a la función de validación correspondiente y muestra el resultado."""
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


def menu_interactivo():
    """Menú por consola para probar cadenas manualmente contra las funciones."""
    while True:
        print("\n=== Prueba de viabilidad: menú ===")
        print("1. Validar DNI")
        print("2. Validar RUC")
        print("3. Validar XML reducido")
        print("4. Ejecutar pruebas automáticas (casos de ejemplo)")
        print("5. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion in ("1", "2", "3"):
            cadena = input("Escribe la cadena a validar: ")
            probar_cadena(opcion, cadena)
        elif opcion == "4":
            ejecutar_pruebas_automaticas()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    menu_interactivo()