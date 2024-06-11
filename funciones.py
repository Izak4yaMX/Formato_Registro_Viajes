"""
Este archivo contiene funciones auxiliares para la aplicación de generación de nóminas.
Las funciones incluyen la selección de archivos, manejo de fechas, y cálculo de la semana
basada en rangos de fechas seleccionados.

Funciones:
    - on_file_selected(e):
        Maneja la selección de un archivo de Excel y extrae la información de empleados.
    - change_date_start(date_picker):
        Actualiza la fecha de inicio seleccionada.
    - change_date_end(date_picker):
        Actualiza la fecha de finalización seleccionada y calcula la semana si ambas fechas están disponibles.
    - date_picker_dismissed(date_picker):
        Maneja el evento de cierre del selector de fechas.
    - obtener_semana(fecha_inicial, fecha_final):
        Calcula el número de la semana, los días de inicio y fin, los meses, y el año a partir de un rango de fechas.
"""

import flet as ft
import pandas as pd

fecha_inicial = None
fecha_final = None

def on_file_selected(e):
    """
    Maneja la selección de un archivo de Excel y extrae la información de empleados.

    Parámetros:
        e (FilePickerResultEvent): Evento que contiene la información del archivo seleccionado.

    Retorna:
        list: Lista de información de empleados si se selecciona un archivo, de lo contrario, una lista vacía.
    """
    if e.files:
        file_path = e.files[0].path
        data = pd.read_excel(file_path)
        print(data.head())
        empleados_info = data[["No. Empleado", "Nombre"]].values.tolist()
        return empleados_info
    else:
        print("No se seleccionó ningún archivo")
        return []

def change_date_start(date_picker: ft.DatePicker):
    """
    Actualiza la fecha de inicio seleccionada.

    Parámetros:
        date_picker (DatePicker): El selector de fecha que contiene la fecha seleccionada.

    Retorna:
        None
    """
    global fecha_inicial
    fecha_inicial = date_picker.value
    print(f"Fecha inicial seleccionada: {fecha_inicial}")

def change_date_end(date_picker: ft.DatePicker):
    """
    Actualiza la fecha de finalización seleccionada y calcula la semana si ambas fechas están disponibles.

    Parámetros:
        date_picker (DatePicker): El selector de fecha que contiene la fecha seleccionada.

    Retorna:
        None
    """
    global fecha_final
    fecha_final = date_picker.value
    print(f"Fecha final seleccionada: {fecha_final}")
    if fecha_inicial and fecha_final:
        obtener_semana(fecha_inicial, fecha_final)

def date_picker_dismissed(date_picker: ft.DatePicker):
    """
    Maneja el evento de cierre del selector de fechas.

    Parámetros:
        date_picker (DatePicker): El selector de fecha que fue cerrado.

    Retorna:
        None
    """
    print(f"Date picker dismissed, value is {date_picker.value}")

def obtener_semana(fecha_inicial, fecha_final):
    """
    Calcula el número de la semana, los días de inicio y fin, los meses, y el año a partir de un rango de fechas.

    Parámetros:
        fecha_inicial (datetime.date): La fecha de inicio del rango.
        fecha_final (datetime.date): La fecha final del rango.

    Retorna:
        tuple: Una tupla que contiene el número de la semana, los días de inicio y fin, los meses, y el año.
    """
    semana_inicial = fecha_inicial.isocalendar()[1]
    semana_final = fecha_final.isocalendar()[1]
    dia_inicio = fecha_inicial.day
    mes_inicio = fecha_inicial.strftime("%B")
    dia_final = fecha_final.day
    mes_final = fecha_final.strftime("%B")
    año_final = fecha_final.year

    if semana_inicial == semana_final:
        semana = semana_inicial
        print(f"El rango seleccionado pertenece a la semana {semana} del año.")
    else:
        semana = f"{semana_inicial}-{semana_final}"
        print(f"El rango seleccionado abarca desde la semana {semana_inicial} hasta la semana {semana_final} del año.")

    return semana, dia_inicio, mes_inicio, dia_final, mes_final, año_final
