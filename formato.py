"""
Se utiliza la biblioteca ReportLab para generar un archivo PDF con la nómina semanal
de empleados. Los datos de los empleados, así como la semana, las fechas de inicio y fin, y la
carpeta de destino, se pasan a la función principal `crear_archivo`.

Funciones:
    - crear_archivo(empleados_info, semana, dia_inicio, mes_inicio, dia_final, mes_final, año_final, carpeta_destino):
        Genera un archivo PDF con la información proporcionada.
    - add_lines_to_observations(canvas, doc):
        Añade líneas para observaciones en cada página del documento PDF.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import inch

def crear_archivo(empleados_info, semana, dia_inicio, mes_inicio, dia_final, mes_final, año_final, carpeta_destino):
    """
    Genera un archivo PDF con la nómina semanal de los empleados.

    Parámetros:
        empleados_info (list): Lista de información de empleados.
        semana (int): Número de la semana.
        dia_inicio (int): Día de inicio de la semana.
        mes_inicio (str): Mes de inicio de la semana.
        dia_final (int): Día final de la semana.
        mes_final (str): Mes final de la semana.
        año_final (int): Año final de la semana.
        carpeta_destino (str): Ruta de la carpeta donde se guardará el PDF.

    Retorna:
        None
    """
    # Ruta completa del archivo PDF
    pdf_path = os.path.join(carpeta_destino, "Nomina_Semanal.pdf")

    #Ruta del logo que aparece en la esquina del documento
    logo_path = "assets/logotipo.png"
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=0.5 * inch, leftMargin=0.5 * inch, topMargin=0.1 * inch, bottomMargin=0.1 * inch)

    #Estilos utilizados en el documento
    styles = getSampleStyleSheet()
    styleN = ParagraphStyle(name="Normal", fontSize=7)
    styleH = ParagraphStyle(name="Heading1", fontSize=15, leading=10, alignment=1)

    #Es el array que almacena los elementos del documento
    elements = []

    #Por cada elemento en el archivo excel se ejecuta lo siguiente:
    for empleado in empleados_info:
        #Se aplica el logo
        logo = Image(logo_path)
        logo.drawHeight = 0.5 * inch
        logo.drawWidth = 1.0 * inch
        #Se aplica el titulo del documento
        encabezado = [[logo, Paragraph("<b>Transporte, CBL</b>", styleH)]]
        table_encabezado = Table(encabezado, colWidths=[1.0 * inch, 6.0 * inch])
        table_encabezado.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 30),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        #Se aplica el subtiulo del documento
        encabezado2 = [[Paragraph('<b>NOMINA SEMANAL</b>', styleH)]]
        table_encabezado2 = Table(encabezado2, colWidths=[7 * inch])
        table_encabezado2.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        # Se muestran los datos del numero de la semana y el rango de fechas
        info_semana = [["SEMANA   ", f" {semana} ", "DEL", dia_inicio, "DE", mes_inicio, "AL", dia_final, "DE", mes_final, "DEL", año_final]]
        table_info_semana = Table(info_semana, colWidths=[0.65 * inch] * 12)
        table_info_semana.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("TOPPADDING", (0, 0), (-1, -1), 2), 
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BACKGROUND", (0, 0), (1, 0), colors.lightgrey),
        ]))

        # Se muestra el numero de empleado y el chofer, esta info se obtiene del archivo de excel
        numero_empleado = empleado[0]
        nombre_empleado = empleado[1]
        info_chofer = [["No EMPLEADO", numero_empleado, "NOMBRE DE CHOFER", nombre_empleado]]
        table_info_chofer = Table(info_chofer, colWidths=[1 * inch, 1 * inch, 1.5 * inch, 3.5 * inch])
        table_info_chofer.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("TOPPADDING", (0, 0), (-1, -1), 2), 
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2), 
            ("FONTSIZE", (0, 0), (-1, -1), 7), 
        ]))

        #Se definen los titulos de las columnas de la tabla principal
        data = [["FECHA", "No. ORDEN", "CLIENTE", "TON / M3", "TRACTOR", "REMOLQUE", "TIPO DE VIAJE"]]
        for i in range(35):
            data.append(["" for _ in range(7)])

        table = Table(data, colWidths=[0.8 * inch, 1.2 * inch, 2 * inch, 0.8 * inch, 0.8 * inch, 0.8 * inch, 1.4 * inch])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.beige),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 3),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 1), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 1),
        ]))

        # Aqui se agregan todos los elementos del documento
        elements.extend([
            table_encabezado,
            Spacer(1, 3),
            table_encabezado2,
            Spacer(1, 3),
            table_info_semana,
            Spacer(1, 5),
            table_info_chofer,
            Spacer(1, 5),
            table,
            Spacer(1, 8),
            Paragraph("OBSERVACIONES:", styleN),
            Spacer(1, 15)
        ])

        # Se usa para crear una pagina nueva al terminar de agregar todos los elementos
        elements.append(PageBreak())

    #funcion para construir el archivo y guardarlo en un path dado
    pdf.build(elements, onFirstPage=add_lines_to_observations, onLaterPages=add_lines_to_observations)
    print(f"Archivo PDF generado correctamente en {pdf_path}.")

def add_lines_to_observations(canvas, doc):
    """
    Añade líneas para observaciones en cada página del documento PDF.

    Parámetros:
        canvas (Canvas): El lienzo sobre el que se dibuja el PDF.
        doc (Document): El documento PDF.

    Retorna:
        None
    """
    canvas.saveState()
    line_height = 12
    start_x = 0.5 * inch
    end_x = 8.0 * inch
    start_y = 1.25 * inch
    for i in range(5):
        canvas.line(start_x, start_y - i * line_height, end_x, start_y - i * line_height)
    canvas.restoreState()
