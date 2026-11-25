# -*- coding: utf-8 -*-
"""
===============================================================================
 Universidad Nacional Abierta y a Distancia - UNAD
 Curso: Fundamentos de Programación (213022)
 Fase 5 - Evaluación Final POA - Problema 1

 Herramienta: Evaluador del nivel de compromiso de sesiones de clientes
 Autora: María Claudia Ramírez Wilches

 Descripción:
   Una matriz almacena sesiones de clientes de una plataforma digital con el
   formato por fila: [ID del cliente, Duración (segundos), Número de clics].
   El programa clasifica cada sesión como "Alto", "Medio" o "Bajo" según las
   reglas de negocio y muestra un informe con el ID del cliente y su
   clasificación final de compromiso.

 Reglas de negocio:
   - "Alto"  si Duración > 180 segundos  Y  Clics > 8
   - "Bajo"  si Duración < 60 segundos   O  Clics < 3
   - "Medio" en cualquier otro caso

 Ejecución:  python compromiso_sesiones.py
 Requisitos: Python 3.8 o superior (tkinter viene incluido con Python).
===============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


# =============================================================================
# 1. CONSTANTES DEL PROBLEMA
# =============================================================================

# Umbrales de la lógica de negocio (constantes: no cambian durante la ejecución)
DURACION_MINIMA_ALTO = 180   # segundos: la duración debe ser MAYOR que este valor
CLICS_MINIMOS_ALTO = 8       # la cantidad de clics debe ser MAYOR que este valor
DURACION_MAXIMA_BAJO = 60    # segundos: duración MENOR que este valor -> Bajo
CLICS_MAXIMOS_BAJO = 3       # clics MENORES que este valor -> Bajo

# Posiciones (columnas) de cada dato dentro de una fila de la matriz
COL_ID = 0
COL_DURACION = 1
COL_CLICS = 2

NIVELES = ["Alto", "Medio", "Bajo"]

# Datos iniciales: matriz con 8 sesiones (el problema exige al menos 5).
# Se incluyen casos límite (180 s, 60 s, 8 clics, 3 clics) para comprobar
# que los operadores ">" y "<" se aplican tal como lo pide el enunciado.
MATRIZ_INICIAL = [
    ["C001", 245, 12],
    ["C002", 45, 10],
    ["C003", 120, 5],
    ["C004", 300, 2],
    ["C005", 190, 9],
    ["C006", 180, 15],
    ["C007", 60, 3],
    ["C008", 200, 8],
]


# =============================================================================
# 2. FUNCIONES DE LÓGICA DE NEGOCIO (no dependen de la interfaz gráfica)
# =============================================================================

def clasificar_compromiso(duracion, clics):
    """Devuelve la clasificación de compromiso de una sesión.

    Parámetros:
        duracion (int): duración de la sesión en segundos.
        clics (int): número de clics realizados en la sesión.
    Retorna:
        str: "Alto", "Bajo" o "Medio".
    """
    if duracion > DURACION_MINIMA_ALTO and clics > CLICS_MINIMOS_ALTO:
        clasificacion = "Alto"
    elif duracion < DURACION_MAXIMA_BAJO or clics < CLICS_MAXIMOS_BAJO:
        clasificacion = "Bajo"
    else:
        clasificacion = "Medio"
    return clasificacion


def generar_informe(matriz):
    """Recorre la matriz de sesiones y construye el informe.

    Retorna una lista de filas con el formato:
        [ID del cliente, Duración, Clics, Clasificación]
    """
    informe = []
    for fila in matriz:  # estructura repetitiva: una vuelta por cada sesión
        id_cliente = fila[COL_ID]
        duracion = fila[COL_DURACION]
        clics = fila[COL_CLICS]
        nivel = clasificar_compromiso(duracion, clics)
        informe.append([id_cliente, duracion, clics, nivel])
    return informe


def contar_por_nivel(informe):
    """Cuenta cuántas sesiones hay en cada nivel de compromiso."""
    conteo = {"Alto": 0, "Medio": 0, "Bajo": 0}
    for fila in informe:
        nivel = fila[3]
        conteo[nivel] = conteo[nivel] + 1
    return conteo


def existe_id(matriz, id_cliente):
    """Indica si un ID de cliente ya está registrado en la matriz.

    Usa un ciclo while que se detiene apenas encuentra el ID
    (búsqueda secuencial), sin recorrer el resto de la matriz.
    """
    i = 0
    encontrado = False
    while i < len(matriz) and not encontrado:
        if matriz[i][COL_ID].upper() == id_cliente.upper():
            encontrado = True
        i = i + 1
    return encontrado


def validar_entero_no_negativo(texto, nombre_campo):
    """Convierte un texto a entero >= 0.

    Retorna una tupla (valor, mensaje_error). Si el dato es válido,
    mensaje_error es una cadena vacía.
    """
    texto = texto.strip()
    if texto == "":
        return None, "El campo '" + nombre_campo + "' es obligatorio."
    if not texto.isdigit():
        return None, ("El campo '" + nombre_campo +
                      "' debe ser un número entero mayor o igual a cero.")
    return int(texto), ""


def validar_sesion(matriz, id_texto, duracion_texto, clics_texto):
    """Valida los datos de una nueva sesión antes de agregarla a la matriz.

    Retorna (fila, mensaje_error). Si hay error, fila es None.
    """
    id_cliente = id_texto.strip().upper()
    if id_cliente == "":
        return None, "El campo 'ID del cliente' es obligatorio."
    if existe_id(matriz, id_cliente):
        return None, "El ID '" + id_cliente + "' ya está registrado."

    duracion, error = validar_entero_no_negativo(duracion_texto, "Duración")
    if error != "":
        return None, error

    clics, error = validar_entero_no_negativo(clics_texto, "Número de clics")
    if error != "":
        return None, error

    return [id_cliente, duracion, clics], ""


def informe_como_texto(informe):
    """Construye el informe en texto plano (para consola y para exportar)."""
    lineas = []
    lineas.append("=" * 58)
    lineas.append("   INFORME DE COMPROMISO DE SESIONES DE CLIENTES")
    lineas.append("   Generado: " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    lineas.append("=" * 58)
    lineas.append("{:<6}{:<14}{:>14}{:>10}{:>14}".format(
        "N°", "ID Cliente", "Duración (s)", "Clics", "Compromiso"))
    lineas.append("-" * 58)
    numero = 1
    for fila in informe:
        lineas.append("{:<6}{:<14}{:>14}{:>10}{:>14}".format(
            numero, fila[0], fila[1], fila[2], fila[3]))
        numero = numero + 1
    lineas.append("-" * 58)

    conteo = contar_por_nivel(informe)
    lineas.append("Total de sesiones evaluadas: " + str(len(informe)))
    for nivel in NIVELES:
        lineas.append("  Compromiso " + nivel + ": " + str(conteo[nivel]))
    lineas.append("=" * 58)
    return "\n".join(lineas)


def mostrar_informe_consola(matriz):
    """Imprime en la consola el informe con el ID y la clasificación."""
    print(informe_como_texto(generar_informe(matriz)))


# =============================================================================
# 3. INTERFAZ GRÁFICA (tkinter)
# =============================================================================

# Paleta de colores de la interfaz
COLOR_PRIMARIO = "#1F3A5F"
COLOR_FONDO = "#F4F6F9"
COLOR_TARJETA = "#FFFFFF"
COLOR_TEXTO = "#1E2A38"
COLOR_TEXTO_SUAVE = "#5B6B7F"
COLORES_NIVEL = {
    "Alto": {"fuerte": "#1E8449", "suave": "#E3F4EA"},
    "Medio": {"fuerte": "#B9770E", "suave": "#FDF2DC"},
    "Bajo": {"fuerte": "#C0392B", "suave": "#FBE5E3"},
}

# La matriz de trabajo empieza como una copia de los datos iniciales
matriz_sesiones = [fila[:] for fila in MATRIZ_INICIAL]

# Diccionario donde se guardan los controles de la ventana que se reutilizan
ui = {}


def refrescar_tabla():
    """Vuelve a generar el informe y lo muestra en la tabla y en las tarjetas."""
    tabla = ui["tabla"]
    for item in tabla.get_children():
        tabla.delete(item)

    informe = generar_informe(matriz_sesiones)
    numero = 1
    for fila in informe:
        tabla.insert("", "end",
                     values=(numero, fila[0], fila[1], fila[2], fila[3]),
                     tags=(fila[3],))
        numero = numero + 1

    conteo = contar_por_nivel(informe)
    ui["tarjeta_total"].config(text=str(len(informe)))
    for nivel in NIVELES:
        ui["tarjeta_" + nivel].config(text=str(conteo[nivel]))


def mostrar_estado(mensaje):
    """Muestra un mensaje en la barra de estado inferior."""
    ui["estado"].config(text=mensaje)


def limpiar_formulario():
    ui["entrada_id"].delete(0, "end")
    ui["entrada_duracion"].delete(0, "end")
    ui["entrada_clics"].delete(0, "end")
    ui["entrada_id"].focus_set()


def actualizar_vista_previa(*_):
    """Muestra en vivo la clasificación que tendría la sesión del formulario."""
    duracion, error_d = validar_entero_no_negativo(
        ui["var_duracion"].get(), "Duración")
    clics, error_c = validar_entero_no_negativo(
        ui["var_clics"].get(), "Número de clics")
    etiqueta = ui["vista_previa"]
    if error_d == "" and error_c == "":
        nivel = clasificar_compromiso(duracion, clics)
        etiqueta.config(text="Clasificación: " + nivel,
                        fg=COLORES_NIVEL[nivel]["fuerte"],
                        bg=COLORES_NIVEL[nivel]["suave"])
    else:
        etiqueta.config(text="Clasificación: —",
                        fg=COLOR_TEXTO_SUAVE, bg=COLOR_FONDO)


def agregar_sesion(*_):
    fila, error = validar_sesion(matriz_sesiones,
                                 ui["entrada_id"].get(),
                                 ui["entrada_duracion"].get(),
                                 ui["entrada_clics"].get())
    if error != "":
        messagebox.showwarning("Dato no válido", error)
        return
    matriz_sesiones.append(fila)
    refrescar_tabla()
    nivel = clasificar_compromiso(fila[COL_DURACION], fila[COL_CLICS])
    mostrar_estado("Sesión " + fila[COL_ID] + " agregada. Compromiso: " + nivel)
    limpiar_formulario()


def eliminar_seleccion():
    seleccion = ui["tabla"].selection()
    if len(seleccion) == 0:
        messagebox.showinfo("Eliminar sesión",
                            "Seleccione en la tabla la sesión que desea eliminar.")
        return
    ids_a_borrar = []
    for item in seleccion:
        ids_a_borrar.append(ui["tabla"].item(item, "values")[1])
    texto = ", ".join(ids_a_borrar)
    if not messagebox.askyesno("Eliminar sesión",
                               "¿Eliminar la(s) sesión(es) " + texto + "?"):
        return
    # Se recorre la matriz de atrás hacia adelante para borrar sin saltar filas
    for i in range(len(matriz_sesiones) - 1, -1, -1):
        if matriz_sesiones[i][COL_ID] in ids_a_borrar:
            del matriz_sesiones[i]
    refrescar_tabla()
    mostrar_estado("Sesión(es) eliminada(s): " + texto)


def restablecer_datos():
    if not messagebox.askyesno("Restablecer datos",
                               "Se perderán los cambios y se cargarán las "
                               "8 sesiones iniciales. ¿Desea continuar?"):
        return
    matriz_sesiones.clear()
    for fila in MATRIZ_INICIAL:
        matriz_sesiones.append(fila[:])
    refrescar_tabla()
    mostrar_estado("Se restablecieron los datos iniciales.")


def exportar_informe():
    if len(matriz_sesiones) == 0:
        messagebox.showinfo("Exportar informe", "No hay sesiones para exportar.")
        return
    ruta = filedialog.asksaveasfilename(
        title="Guardar informe",
        defaultextension=".txt",
        initialfile="informe_compromiso.txt",
        filetypes=[("Archivo de texto", "*.txt")])
    if ruta == "":
        return
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(informe_como_texto(generar_informe(matriz_sesiones)))
        mostrar_estado("Informe guardado en: " + ruta)
    except OSError as error:
        messagebox.showerror("Exportar informe",
                             "No se pudo guardar el archivo:\n" + str(error))


def crear_estilos(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("Treeview", rowheight=30, font=("Segoe UI", 10),
                     background=COLOR_TARJETA, fieldbackground=COLOR_TARJETA,
                     foreground=COLOR_TEXTO, borderwidth=0)
    estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                     background=COLOR_PRIMARIO, foreground="white",
                     relief="flat", padding=6)
    estilo.map("Treeview.Heading", background=[("active", "#2C5282")])
    estilo.map("Treeview", background=[("selected", "#BFD7F5")],
               foreground=[("selected", COLOR_TEXTO)])
    estilo.configure("Primario.TButton", font=("Segoe UI", 10, "bold"),
                     background=COLOR_PRIMARIO, foreground="white",
                     padding=8, borderwidth=0)
    estilo.map("Primario.TButton", background=[("active", "#2C5282")])
    estilo.configure("Secundario.TButton", font=("Segoe UI", 10),
                     background="#E2E8F0", foreground=COLOR_TEXTO,
                     padding=7, borderwidth=0)
    estilo.map("Secundario.TButton", background=[("active", "#CBD5E0")])


def crear_tarjeta(padre, titulo, color_fuerte, color_suave, columna):
    """Crea una tarjeta de resumen y devuelve la etiqueta del número."""
    marco = tk.Frame(padre, bg=color_suave, padx=14, pady=8,
                     highlightbackground=color_fuerte, highlightthickness=1)
    marco.grid(row=0, column=columna, sticky="nsew", padx=5)
    tk.Label(marco, text=titulo, bg=color_suave, fg=color_fuerte,
             font=("Segoe UI", 9, "bold")).pack(anchor="w")
    numero = tk.Label(marco, text="0", bg=color_suave, fg=color_fuerte,
                      font=("Segoe UI", 22, "bold"))
    numero.pack(anchor="w")
    return numero


def crear_campo(padre, texto, variable=None):
    tk.Label(padre, text=texto, bg=COLOR_TARJETA, fg=COLOR_TEXTO,
             font=("Segoe UI", 10)).pack(anchor="w", pady=(8, 2))
    entrada = ttk.Entry(padre, font=("Segoe UI", 11), textvariable=variable)
    entrada.pack(fill="x", ipady=3)
    return entrada


def construir_ventana():
    ventana = tk.Tk()
    ventana.title("Evaluador de Compromiso de Sesiones - UNAD Fase 5")
    ventana.geometry("1080x720")
    ventana.minsize(960, 700)
    ventana.configure(bg=COLOR_FONDO)
    crear_estilos(ventana)

    # ---------------- Encabezado ----------------
    encabezado = tk.Frame(ventana, bg=COLOR_PRIMARIO, padx=24, pady=14)
    encabezado.pack(fill="x")
    tk.Label(encabezado, text="Evaluador de Compromiso de Sesiones",
             bg=COLOR_PRIMARIO, fg="white",
             font=("Segoe UI", 18, "bold")).pack(anchor="w")
    tk.Label(encabezado,
             text="Clasificación del nivel de compromiso de clientes en la "
                  "plataforma digital  ·  Fundamentos de Programación (213022)",
             bg=COLOR_PRIMARIO, fg="#C9D6E8",
             font=("Segoe UI", 10)).pack(anchor="w")

    cuerpo = tk.Frame(ventana, bg=COLOR_FONDO, padx=18, pady=14)
    cuerpo.pack(fill="both", expand=True)

    # ---------------- Panel izquierdo: formulario ----------------
    panel = tk.Frame(cuerpo, bg=COLOR_TARJETA, padx=18, pady=16, width=300,
                     highlightbackground="#DDE3EA", highlightcolor="#DDE3EA",
                     highlightthickness=1)
    panel.pack(side="left", fill="y", padx=(0, 14))
    panel.pack_propagate(False)

    tk.Label(panel, text="Registrar sesión", bg=COLOR_TARJETA,
             fg=COLOR_PRIMARIO, font=("Segoe UI", 13, "bold")).pack(anchor="w")

    ui["var_duracion"] = tk.StringVar()
    ui["var_clics"] = tk.StringVar()
    ui["entrada_id"] = crear_campo(panel, "ID del cliente")
    ui["entrada_duracion"] = crear_campo(panel, "Duración de la sesión (segundos)",
                                         ui["var_duracion"])
    ui["entrada_clics"] = crear_campo(panel, "Número de clics", ui["var_clics"])
    ui["var_duracion"].trace_add("write", actualizar_vista_previa)
    ui["var_clics"].trace_add("write", actualizar_vista_previa)

    ui["vista_previa"] = tk.Label(panel, text="Clasificación: —",
                                  bg=COLOR_FONDO, fg=COLOR_TEXTO_SUAVE,
                                  font=("Segoe UI", 10, "bold"), pady=6)
    ui["vista_previa"].pack(fill="x", pady=(12, 8))

    ttk.Button(panel, text="Agregar sesión", style="Primario.TButton",
               command=agregar_sesion).pack(fill="x")

    # Criterios de clasificación (recordatorio para el usuario)
    tk.Label(panel, text="Criterios de clasificación", bg=COLOR_TARJETA,
             fg=COLOR_PRIMARIO, font=("Segoe UI", 11, "bold")).pack(
                 anchor="w", pady=(18, 4))
    criterios = [
        ("Alto", "Duración > " + str(DURACION_MINIMA_ALTO) +
         " s  y  clics > " + str(CLICS_MINIMOS_ALTO)),
        ("Bajo", "Duración < " + str(DURACION_MAXIMA_BAJO) +
         " s  o  clics < " + str(CLICS_MAXIMOS_BAJO)),
        ("Medio", "Cualquier otro caso"),
    ]
    for nivel, regla in criterios:
        fila = tk.Frame(panel, bg=COLOR_TARJETA)
        fila.pack(fill="x", pady=2)
        tk.Label(fila, text=" " + nivel + " ", width=6,
                 bg=COLORES_NIVEL[nivel]["fuerte"], fg="white",
                 font=("Segoe UI", 9, "bold")).pack(side="left")
        tk.Label(fila, text=" " + regla, bg=COLOR_TARJETA, fg=COLOR_TEXTO,
                 font=("Segoe UI", 9)).pack(side="left")

    # Botones de acciones
    acciones = tk.Frame(panel, bg=COLOR_TARJETA)
    acciones.pack(side="bottom", fill="x")
    ttk.Button(acciones, text="Exportar informe (.txt)",
               style="Secundario.TButton",
               command=exportar_informe).pack(fill="x", pady=3)
    ttk.Button(acciones, text="Eliminar sesión seleccionada",
               style="Secundario.TButton",
               command=eliminar_seleccion).pack(fill="x", pady=3)
    ttk.Button(acciones, text="Restablecer datos iniciales",
               style="Secundario.TButton",
               command=restablecer_datos).pack(fill="x", pady=3)

    # ---------------- Panel derecho: resumen e informe ----------------
    derecho = tk.Frame(cuerpo, bg=COLOR_FONDO)
    derecho.pack(side="left", fill="both", expand=True)

    tarjetas = tk.Frame(derecho, bg=COLOR_FONDO)
    tarjetas.pack(fill="x", pady=(0, 12))
    for columna in range(4):
        tarjetas.columnconfigure(columna, weight=1, uniform="tarjetas")
    ui["tarjeta_total"] = crear_tarjeta(tarjetas, "TOTAL SESIONES",
                                        COLOR_PRIMARIO, "#E6ECF4", 0)
    columna = 1
    for nivel in NIVELES:
        ui["tarjeta_" + nivel] = crear_tarjeta(
            tarjetas, "COMPROMISO " + nivel.upper(),
            COLORES_NIVEL[nivel]["fuerte"], COLORES_NIVEL[nivel]["suave"],
            columna)
        columna = columna + 1

    tk.Label(derecho, text="Informe de compromiso por cliente",
             bg=COLOR_FONDO, fg=COLOR_PRIMARIO,
             font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 6))

    marco_tabla = tk.Frame(derecho, bg=COLOR_TARJETA,
                           highlightbackground="#DDE3EA",
                           highlightcolor="#DDE3EA", highlightthickness=1)
    marco_tabla.pack(fill="both", expand=True)

    columnas = ("numero", "id", "duracion", "clics", "nivel")
    tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings",
                         selectmode="extended")
    encabezados = [("numero", "N°", 50), ("id", "ID Cliente", 140),
                   ("duracion", "Duración (s)", 130), ("clics", "Clics", 100),
                   ("nivel", "Compromiso", 140)]
    for clave, titulo, ancho in encabezados:
        tabla.heading(clave, text=titulo)
        tabla.column(clave, width=ancho, anchor="center")
    for nivel in NIVELES:
        tabla.tag_configure(nivel, background=COLORES_NIVEL[nivel]["suave"],
                            foreground=COLORES_NIVEL[nivel]["fuerte"])

    barra = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=barra.set)
    tabla.pack(side="left", fill="both", expand=True)
    barra.pack(side="right", fill="y")
    ui["tabla"] = tabla

    # ---------------- Barra de estado ----------------
    ui["estado"] = tk.Label(ventana, text="Listo. Se cargaron las sesiones iniciales.",
                            bg="#E2E8F0", fg=COLOR_TEXTO_SUAVE, anchor="w",
                            padx=12, pady=4, font=("Segoe UI", 9))
    ui["estado"].pack(fill="x", side="bottom")

    # Atajos de teclado: Enter agrega la sesión, Supr elimina la selección
    for clave in ("entrada_id", "entrada_duracion", "entrada_clics"):
        ui[clave].bind("<Return>", agregar_sesion)
    tabla.bind("<Delete>", lambda evento: eliminar_seleccion())

    refrescar_tabla()
    ui["entrada_id"].focus_set()
    return ventana


# =============================================================================
# 4. PROGRAMA PRINCIPAL
# =============================================================================

def main():
    # Salida en consola con el informe de los datos iniciales
    mostrar_informe_consola(matriz_sesiones)
    # Interfaz gráfica
    ventana = construir_ventana()
    ventana.mainloop()


if __name__ == "__main__":
    main()
