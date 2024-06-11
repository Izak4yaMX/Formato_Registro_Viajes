"""
Este archivo es la entrada principal para la aplicación de generación de nóminas.
Utiliza Flet para la interfaz de usuario y permite a los usuarios seleccionar archivos,
fechas y carpetas para generar un archivo PDF de nómina semanal.

Funciones:
    - main(page: Page):
        Función principal que configura la interfaz de usuario y maneja los eventos.
"""

import flet as ft
import datetime
from flet import Page, Text, ElevatedButton, FilePicker, TextField, DatePicker, Row, Column, Container, colors, ThemeMode
from funciones import on_file_selected, change_date_start, change_date_end, date_picker_dismissed, obtener_semana
from formato import crear_archivo

# Variables globales para almacenar la información seleccionada
empleados_info = []
fecha_inicial = None
fecha_final = None
carpeta_destino = None

def main(page: Page):
    """
    Configura la interfaz de usuario y maneja los eventos para la aplicación de generación de nóminas.

    Parámetros:
        page (Page): La página principal de Flet en la que se construye la interfaz de usuario.

    Retorna:
        None
    """
    page.title = "Generador de Nómina"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_height = 600
    page.window_width = 700
    page.window_resizable = False
    page.window_icon = "assets/icon.ico"
    status_text = Text()

    def handle_file_selected(e):
        """
        Maneja la selección del archivo de empleados.

        Parámetros:
            e (FilePickerResultEvent): Evento que contiene la información del archivo seleccionado.

        Retorna:
            None
        """
        global empleados_info
        empleados_info = on_file_selected(e)
        status_text.value = "Archivo de empleados seleccionado."
        page.update()

    def handle_folder_selected(e):
        """
        Maneja la selección de la carpeta de destino.

        Parámetros:
            e (FilePickerResultEvent): Evento que contiene la información de la carpeta seleccionada.

        Retorna:
            None
        """
        global carpeta_destino
        if e.path:
            carpeta_destino = e.path
            status_text.value = f"Carpeta de destino seleccionada: {carpeta_destino}"
        else:
            status_text.value = "No se seleccionó ninguna carpeta."
        page.update()

    def on_change_date_start(e):
        """
        Actualiza la fecha de inicio seleccionada y muestra el estado.

        Parámetros:
            e (ControlEvent): Evento que contiene la fecha seleccionada.

        Retorna:
            None
        """
        global fecha_inicial
        fecha_inicial = e.control.value
        status_text.value = f"Fecha inicial seleccionada: {fecha_inicial}"
        update_week_number()
        page.update()

    def on_change_date_end(e):
        """
        Actualiza la fecha de finalización seleccionada y muestra el estado.

        Parámetros:
            e (ControlEvent): Evento que contiene la fecha seleccionada.

        Retorna:
            None
        """
        global fecha_final
        fecha_final = e.control.value
        status_text.value = f"Fecha final seleccionada: {fecha_final}"
        update_week_number()
        page.update()

    def update_week_number():
        """
        Actualiza el número de la semana basado en las fechas seleccionadas y muestra el estado.

        Retorna:
            None
        """
        global fecha_inicial, fecha_final
        if fecha_inicial and fecha_final:
            semana, dia_inicio, mes_inicio, dia_final, mes_final, año_final = obtener_semana(fecha_inicial, fecha_final)
            semana_text_field.value = str(semana)
            page.update()

    # Configuración de los selectores de archivos y carpetas
    file_picker = FilePicker(on_result=handle_file_selected)
    filepicker_button = ElevatedButton(
        text="Seleccionar archivo",
        on_click=lambda _: file_picker.pick_files(allow_multiple=False),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor=colors.BLUE_500, color=colors.WHITE)
    )

    folder_picker = FilePicker(on_result=handle_folder_selected)
    folderpicker_button = ElevatedButton(
        text="Seleccionar carpeta de destino",
        on_click=lambda _: folder_picker.get_directory_path(),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor=colors.BLUE_500, color=colors.WHITE)
    )

    # Configuración de los selectores de fechas
    date_picker_start = DatePicker(
        on_change=on_change_date_start,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )
    date_button_start = ElevatedButton(
        text="Selecciona la fecha inicial",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker_start.pick_date(),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor=colors.ORANGE_500, color=colors.WHITE)
    )

    date_picker_end = DatePicker(
        on_change=on_change_date_end,
        on_dismiss=date_picker_dismissed,
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )
    date_button_end = ElevatedButton(
        text="Selecciona la fecha final",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker_end.pick_date(),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor=colors.ORANGE_500, color=colors.WHITE)
    )

    semana_text_field = TextField( 
        label="Número de Semana",
        width=200,
        read_only=False,
        
    )

    def generate_pdf(e):
        """
        Genera el archivo PDF con la información seleccionada y muestra el estado.

        Parámetros:
            e (ControlEvent): Evento que indica que el botón para generar el PDF fue presionado.

        Retorna:
            None
        """
        global fecha_inicial, fecha_final, carpeta_destino
        if empleados_info and fecha_inicial and fecha_final and carpeta_destino:
            semana, dia_inicio, mes_inicio, dia_final, mes_final, año_final = obtener_semana(fecha_inicial, fecha_final)
            semana = semana_text_field.value
            crear_archivo(empleados_info, semana, dia_inicio, mes_inicio, dia_final, mes_final, año_final, carpeta_destino)
            status_text.value = "Archivo PDF generado correctamente."
        else:
            status_text.value = "Faltan datos para generar el PDF: asegúrate de haber seleccionado un archivo, fechas válidas y una carpeta de destino."
        page.update()

    makepdf_button = ElevatedButton(
        text="Generar archivos",
        on_click=generate_pdf,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), bgcolor=colors.GREEN_500, color=colors.WHITE)
    )

    # Añadir elementos a la página
    page.add(
        Column(
            [
                Text("Introduce el archivo con los nombres de los empleados"),
                file_picker,
                filepicker_button,
                Row([
                    Column(
                        [
                            Text("Introduce la fecha inicial"),
                            date_picker_start,
                            date_button_start,
                        ],
                        alignment="center",
                        horizontal_alignment="center",    
                    ),
                    Column(
                        [
                            Text("Introduce la fecha final"),
                            date_picker_end,
                            date_button_end,
                        ],
                        alignment="center",
                        horizontal_alignment="center",
                    ),
                ],
                alignment="center",
                vertical_alignment="center"
                ),
                semana_text_field,
                folder_picker,
                folderpicker_button,
                makepdf_button,
                status_text,  # Añadir el Text para mostrar mensajes de estado
                Text()
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    )
    

# Ejecutar la aplicación
ft.app(target=main, assets_dir="assets")

