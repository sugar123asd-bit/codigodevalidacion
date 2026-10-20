import os

from datetime import datetime


def menu_principal(usuario):

  while True:

    limpiar_pantalla()

    print("=" * 40)

    print("CAJA - MENÚ PRINCIPAL".center(40))

    print(f"Sesión: {usuario}".center(40))

    print("=" * 40)

    print("1. Registrar producto")

    print("2. Ver stock")

    print("3. Vender producto")

    print("4. Cerrar sesión / Salir")

    opcion = input("\nElige una opción: ").strip()



    if opcion == "1":

      registrar_producto()

    elif opcion == "2":

      ver_stock()

    elif opcion == "3":

      menu_venta()

    elif opcion == "4":

      print("\nSesión cerrada. ¡Hasta luego!")

      break

    else:

      print("Opción no válida.")

      pausar()




CARPETA_COMPROBANTES = "comprobantes"



USUARIOS = {

  "admin": "1234",

}



productos = {} 

siguiente_codigo = 1



contador_boleta = 1

contador_factura = 1



historial = [] # 




def limpiar_pantalla():

  os.system("cls" if os.name == "nt" else "clear")


def pausar():

  input("\nPresiona Enter para continuar...")


def pedir_texto(mensaje):

  while True:

    valor = input(mensaje).strip()

    if valor:

      return valor

    print(" -> Este campo no puede estar vacío.")





def pedir_numero(mensaje, positivo=True, entero=False):

  while True:

    valor = input(mensaje).strip()

    try:

      numero = int(valor) if entero else float(valor)

      if positivo and numero <= 0:

        print(" -> Ingresa un número mayor a 0.")

        continue

      return numero

    except ValueError:

      print(" -> Ingresa un número válido.")





def validar_dni(dni):

  return dni.isdigit() and len(dni) == 8





def validar_ruc(ruc):

  return ruc.isdigit() and len(ruc) == 11


def iniciar_sesion():

  intentos = 3

  while intentos > 0:

    limpiar_pantalla()

    print("=" * 40)

    print("INICIO DE SESIÓN".center(40))

    print("=" * 40)

    usuario = input("Usuario: ").strip()

    contrasena = input("Contraseña: ").strip()



    if USUARIOS.get(usuario) == contrasena:

      print(f"\nBienvenido, {usuario}.")

      pausar()

      return usuario



    intentos -= 1

    print(f"\nUsuario o contraseña incorrectos. Intentos restantes: {intentos}")

    pausar()



  print("\nDemasiados intentos fallidos. Cerrando programa.")

  return None



def registrar_producto():

  global siguiente_codigo

  print("\n--- REGISTRAR PRODUCTO ---")

  nombre = pedir_texto("Nombre del producto: ")

  precio = pedir_numero("Precio unitario (S/): ")

  stock = pedir_numero("Stock inicial: ", entero=True)



  codigo = siguiente_codigo

  productos[codigo] = {"nombre": nombre, "precio": precio, "stock": stock}

  siguiente_codigo += 1



  print(f"\nProducto registrado con código {codigo}.")

  pausar()





def ver_stock():

  print("\n--- STOCK DE PRODUCTOS ---")

  if not productos:

    print("Todavía no hay productos registrados.")

  else:

    print(f"{'Cód.':<6}{'Producto':<25}{'Precio':>10}{'Stock':>10}")

    print("-" * 51)

    for codigo, datos in productos.items():

      print(

        f"{codigo:<6}{datos['nombre']:<25}"

        f"{datos['precio']:>10.2f}{datos['stock']:>10}"

      )

  pausar()





# Proceso de venta 



def elegir_productos_para_venta():

  """Permite armar el carrito eligiendo productos por código."""

  carrito = []

  while True:

    limpiar_pantalla()

    print("--- VENTA: elige un producto (0 para terminar) ---\n")

    if not productos:

      print("No hay productos registrados todavía.")

      pausar()

      return carrito



    print(f"{'Cód.':<6}{'Producto':<25}{'Precio':>10}{'Stock':>10}")

    print("-" * 51)

    for codigo, datos in productos.items():

      print(

        f"{codigo:<6}{datos['nombre']:<25}"

        f"{datos['precio']:>10.2f}{datos['stock']:>10}"

      )



    codigo = pedir_numero("\nCódigo del producto (0 para terminar): ", positivo=False, entero=True)

    if codigo == 0:

      if not carrito:

        print(" -> Debes agregar al menos un producto.")

        pausar()

        continue

      break



    if codigo not in productos:

      print(" -> Código no válido.")

      pausar()

      continue



    producto = productos[codigo]

    if producto["stock"] <= 0:

      print(" -> Este producto no tiene stock disponible.")

      pausar()

      continue



    cantidad = pedir_numero(

      f"Cantidad de '{producto['nombre']}' (stock disponible: {producto['stock']}): ",

      entero=True,

    )

    if cantidad > producto["stock"]:

      print(" -> No hay suficiente stock para esa cantidad.")

      pausar()

      continue



    carrito.append({

      "codigo": codigo,

      "nombre": producto["nombre"],

      "cantidad": cantidad,

      "precio_unitario": producto["precio"],

      "subtotal": cantidad * producto["precio"],

    })

    print(f" -> Agregado: {cantidad} x {producto['nombre']}")

    pausar()



  return carrito





def elegir_tipo_comprobante():

  while True:

    print("\n¿Qué comprobante necesitas?")

    print("1. Boleta (DNI)")

    print("2. Factura (RUC)")

    opcion = input("Elige una opción: ").strip()

    if opcion == "1":

      return "boleta"

    if opcion == "2":

      return "factura"

    print(" -> Opción no válida.")





def elegir_metodo_pago(total):

  """Devuelve un dict con el método de pago y, si es efectivo,

  el monto entregado por el cliente y el vuelto a dar."""

  metodos = {

    "1": "Yape/Plin",

    "2": "Efectivo",

    "3": "Tarjeta",

  }

  while True:

    print(f"\nTotal a pagar: S/ {total:.2f}")

    print("¿Cómo pagará el cliente?")

    print("1. Yape/Plin")

    print("2. Efectivo")

    print("3. Tarjeta")

    opcion = input("Elige una opción: ").strip()

    if opcion in metodos:

      metodo = metodos[opcion]

      break

    print(" -> Opción no válida.")



  if metodo != "Efectivo":

    return {"metodo": metodo, "monto_pagado": None, "vuelto": None}



  while True:

    monto_pagado = pedir_numero("Monto entregado por el cliente (S/): ")

    if monto_pagado < total:

      print(f" -> El monto no cubre el total. Falta S/ {total - monto_pagado:.2f}.")

      continue

    vuelto = monto_pagado - total

    return {"metodo": metodo, "monto_pagado": monto_pagado, "vuelto": vuelto}





def pedir_datos_cliente(tipo):

  if tipo == "boleta":

    nombre = pedir_texto("Nombre del cliente: ")

    while True:

      dni = pedir_texto("DNI (8 dígitos): ")

      if validar_dni(dni):

        break

      print(" -> El DNI debe tener 8 dígitos numéricos.")

    return nombre, dni

  else:

    nombre = pedir_texto("Razón social / Nombre: ")

    while True:

      ruc = pedir_texto("RUC (11 dígitos): ")

      if validar_ruc(ruc):

        break

      print(" -> El RUC debe tener 11 dígitos numéricos.")

    return nombre, ruc





def generar_numero(tipo):

  global contador_boleta, contador_factura

  if tipo == "boleta":

    numero = f"B001-{contador_boleta:06d}"

    contador_boleta += 1

  else:

    numero = f"F001-{contador_factura:06d}"

    contador_factura += 1

  return numero





def construir_comprobante(tipo, nombre, documento, carrito, pago):

  total = sum(item["subtotal"] for item in carrito)

  numero = generar_numero(tipo)

  fecha = datetime.now().strftime("%d/%m/%Y %H:%M")



  etiqueta_doc = "DNI" if tipo == "boleta" else "RUC"

  titulo = "BOLETA DE VENTA" if tipo == "boleta" else "FACTURA"



  lineas = []

  lineas.append("=" * 40)

  lineas.append(titulo.center(40))

  lineas.append(f"N° {numero}".center(40))

  lineas.append("=" * 40)

  lineas.append(f"Fecha   : {fecha}")

  lineas.append(f"Cliente  : {nombre}")

  lineas.append(f"{etiqueta_doc}    : {documento}")

  lineas.append(f"Pago    : {pago['metodo']}")

  lineas.append("-" * 40)

  lineas.append(f"{'Cant.':<6}{'Descripción':<20}{'Importe':>14}")

  lineas.append("-" * 40)

  for item in carrito:

    desc = item["nombre"][:20]

    lineas.append(

      f"{item['cantidad']:<6}{desc:<20}{item['subtotal']:>14.2f}"

    )

  lineas.append("-" * 40)

  lineas.append(f"{'TOTAL A PAGAR:':<26}{total:>14.2f}")

  if pago["metodo"] == "Efectivo":

    lineas.append(f"{'Monto entregado:':<26}{pago['monto_pagado']:>14.2f}")

    lineas.append(f"{'VUELTO:':<26}{pago['vuelto']:>14.2f}")
      
  lineas.append("=" * 40)



  texto = "\n".join(lineas)



  registro = {

    "tipo": tipo,

    "numero": numero,

    "fecha": fecha,

    "cliente": nombre,

    "documento": documento,

    "metodo_pago": pago["metodo"],

    "monto_pagado": pago["monto_pagado"],

    "vuelto": pago["vuelto"],

    "items": carrito,

    "total": total,

    "texto": texto,

  }

  return registro

def guardar_comprobante(registro):

  os.makedirs(CARPETA_COMPROBANTES, exist_ok=True)
  nombre_archivo = f"{registro['numero']}.txt"
  ruta = os.path.join(CARPETA_COMPROBANTES, nombre_archivo)
  with open(ruta, "w", encoding="utf-8") as f:
    f.write(registro["texto"])
      
  return ruta

def descontar_stock(carrito):

  for item in carrito:
    productos[item["codigo"]]["stock"] -= item["cantidad"]

def menu_venta():

  limpiar_pantalla()
  print("=" * 40)
  print("NUEVA VENTA".center(40))
  print("=" * 40)

  carrito = elegir_productos_para_venta()

  if not carrito:

    return 


  tipo = elegir_tipo_comprobante()

  nombre, documento = pedir_datos_cliente(tipo)
  total = sum(item["subtotal"] for item in carrito)
  pago = elegir_metodo_pago(total)
  registro = construir_comprobante(tipo, nombre, documento, carrito, pago)
  descontar_stock(carrito)
  historial.append(registro)
  ruta = guardar_comprobante(registro)
    
  limpiar_pantalla()

  print(registro["texto"])

  if registro["metodo_pago"] == "Efectivo":

    print(f"\n>>> VUELTO A ENTREGAR: S/ {registro['vuelto']:.2f} <<<")

  print(f"\nComprobante guardado en: {ruta}")

  pausar()

if __name__ == "__main__":
  usuario_actual = iniciar_sesion()
  if usuario_actual:
    menu_principal(usuario_actual)
