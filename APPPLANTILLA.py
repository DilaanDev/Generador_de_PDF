import streamlit as st
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO  # Para manejar el PDF en memoria


# --- Lógica de Generación de PDF (Adaptada para Streamlit) ---
def generate_attendance_pdf(data_entries):
    # Usamos BytesIO para guardar el PDF en memoria y luego ofrecerlo para descarga
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(letter))
    page_width, page_height = landscape(letter)

    # --- Configuración del Logo ---
    # En Streamlit, las imágenes deben estar accesibles o cargadas como bytes.
    # Para simplicidad, si el logo es estático y pequeño, podrías incrustarlo como base64,
    # o pedir al usuario que lo suba, o ponerlo en una carpeta 'static' si despliegas.
    # Por ahora, simularemos que no hay logo si no se encuentra para evitar errores.
    # Si realmente necesitas un logo fijo, tendrías que subirlo al mismo directorio
    # que tu script de Streamlit y referenciarlo.
    logo_path = "logo.png"  # Asume que el logo está en el mismo directorio
    logo_width = 40
    logo_height = 40
    logo_x = 60
    logo_y = page_height - 90

    c.setFont("Helvetica", 8)

    # Dibuja el logo si existe
    try:
        # reportlab.lib.utils.ImageReader es útil para Streamlit si el logo no está en el disco
        # o si quieres cargar directamente bytes de una imagen subida por el usuario.
        # Aquí, asumimos que 'logo.png' está junto al script.
        # Si no lo tienes, puedes comentar esta sección o poner una imagen de marcador de posición.
        from reportlab.lib.utils import ImageReader
        logo_image = ImageReader(logo_path)
        c.drawImage(logo_image, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
    except Exception as e:
        st.warning(
            f"Advertencia: No se pudo cargar el logo '{logo_path}'. Asegúrate de que el archivo existe en el mismo directorio que el script de Streamlit. Error: {e}")

    goleman_text_x = logo_x + logo_width + 5
    goleman_text_y_goleman = page_height - 60
    goleman_text_y_ips = page_height - 70

    c.setFont("Helvetica-Bold", 11)
    c.drawString(goleman_text_x, goleman_text_y_goleman, "Goleman")
    c.setFont("Helvetica", 8)
    c.drawString(goleman_text_x, goleman_text_y_ips, "IPS")

    # --- Main Title (Centered for landscape) ---
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_width / 2, page_height - 60, "FORMATO DE ASISTENCIA ATENCIÓN DOMICILIARIA")

    # --- Header Section (Top Right Box - adjusted for landscape) ---
    header_box_x = page_width - 160
    header_box_y = page_height - 100
    header_box_width = 110
    header_box_height = 50
    c.rect(header_box_x, header_box_y, header_box_width, header_box_height)

    line_spacing = header_box_height / 4
    for i in range(1, 4):
        c.line(header_box_x, header_box_y + i * line_spacing, header_box_x + header_box_width,
               header_box_y + i * line_spacing)
    c.line(header_box_x + 40, header_box_y, header_box_x + 40, header_box_y + header_box_height)

    c.setFont("Helvetica", 7)
    c.drawString(header_box_x + 5, header_box_y + 38, "Código")
    c.drawString(header_box_x + 5, header_box_y + 26, "Fecha")
    c.drawString(header_box_x + 5, header_box_y + 14, "Versión")
    c.drawString(header_box_x + 5, header_box_y + 2, "Página")
    c.drawString(header_box_x + 45, header_box_y + 38, "SIN-PHD-FR-001")
    c.drawString(header_box_x + 45, header_box_y + 26, "15/05/2024")
    c.drawString(header_box_x + 45, header_box_y + 14, "2")
    c.drawString(header_box_x + 45, header_box_y + 2, "1 de 1")

    # --- Section Titles Below Header (adjusted for landscape) ---
    c.setFont("Helvetica-Bold", 8)
    c.drawString(60, page_height - 130, "JORNADA HORARIA:")
    c.drawString(400, page_height - 130, "HOSPITALIZACIÓN DOMICILIARIA")

    # --- Table Structure ---
    table_start_y = page_height - 150
    table_end_y = 60  # Deja espacio para el pie de página si lo hay

    col_x = {
        "fecha": 62, "hora": 125, "documento_de_identidad": 190, "eps": 280,
        "nombre": 360, "procedimiento": 470, "familiar_signature": 580, "collaborator_signature": 700
    }
    col_widths = {
        "fecha": 60, "hora": 60, "documento_de_identidad": 85, "eps": 80,
        "nombre": 110, "procedimiento": 110, "familiar_signature": 110, "collaborator_signature": 80
    }

    left_margin_table = 60
    right_margin_table = page_width - 60

    # Dibujar líneas verticales de la tabla
    c.line(left_margin_table, table_start_y, left_margin_table, table_end_y)
    current_x_line = left_margin_table
    for key in ["fecha", "hora", "documento_de_identidad", "eps", "nombre", "procedimiento", "familiar_signature",
                "collaborator_signature"]:
        current_x_line += col_widths[key]
        c.line(current_x_line, table_start_y, current_x_line, table_end_y)

    # Dibujar líneas horizontales de los encabezados
    c.line(left_margin_table, table_start_y, right_margin_table, table_start_y)
    c.line(left_margin_table, table_start_y - 25, right_margin_table, table_start_y - 25)
    c.line(left_margin_table, table_start_y - 45, right_margin_table, table_start_y - 45)

    # --- Column Headers ---
    c.setFont("Helvetica-Bold", 7)

    def draw_centered_column_text(text, x_start_col, width_col, y_pos):
        c.drawCentredString(x_start_col + width_col / 2, y_pos, text)

    draw_centered_column_text("FECHA", col_x["fecha"], col_widths["fecha"], table_start_y - 12)
    draw_centered_column_text("(DÍA/MES/AÑO)", col_x["fecha"], col_widths["fecha"], table_start_y - 22)
    draw_centered_column_text("HORA", col_x["hora"], col_widths["hora"], table_start_y - 17)
    draw_centered_column_text("DOCUMENTO DE", col_x["documento_de_identidad"], col_widths["documento_de_identidad"],
                              table_start_y - 12)
    draw_centered_column_text("IDENTIDAD", col_x["documento_de_identidad"], col_widths["documento_de_identidad"],
                              table_start_y - 22)
    draw_centered_column_text("EPS", col_x["eps"], col_widths["eps"], table_start_y - 17)
    draw_centered_column_text("NOMBRE", col_x["nombre"], col_widths["nombre"], table_start_y - 17)
    draw_centered_column_text("PROCEDIMIENTO", col_x["procedimiento"], col_widths["procedimiento"], table_start_y - 17)
    draw_centered_column_text("NOMBRE/FIRMA", col_x["familiar_signature"], col_widths["familiar_signature"],
                              table_start_y - 12)
    draw_centered_column_text("FAMILIAR", col_x["familiar_signature"], col_widths["familiar_signature"],
                              table_start_y - 22)
    draw_centered_column_text("NOMBRE/FIRMA", col_x["collaborator_signature"], col_widths["collaborator_signature"],
                              table_start_y - 12)
    draw_centered_column_text("COLABORADOR", col_x["collaborator_signature"], col_widths["collaborator_signature"],
                              table_start_y - 22)

    # --- Función auxiliar para dibujar texto centrado en una columna ---
    def draw_text_in_column(text_canvas, text, x_start_col, width_col, y_pos, font="Helvetica", font_size=8,
                            centered=True):
        text_canvas.setFont(font, font_size)
        if centered:
            text_canvas.drawCentredString(x_start_col + width_col / 2, y_pos, text)
        else:
            text_canvas.drawString(x_start_col + 2, y_pos, text)  # Pequeño margen a la izquierda

    # --- Dynamic Data Rows ---
    c.setFont("Helvetica", 8)
    row_height = 25
    current_y = table_start_y - 45 - (row_height / 2)

    for i, entry in enumerate(data_entries):
        # Dibuja la línea horizontal para la parte inferior de la fila actual
        c.line(left_margin_table, current_y - (row_height / 2), right_margin_table, current_y - (row_height / 2))

        # El chequeo de página nueva debe asegurarse de que haya espacio para la fila
        if current_y - row_height < table_end_y and i < len(data_entries) - 1:
            c.showPage()
            page_width, page_height = landscape(letter)

            # Volver a dibujar elementos fijos en la nueva página (Encabezados y Logo)
            try:
                logo_image = ImageReader(logo_path)
                c.drawImage(logo_image, logo_x, logo_y, width=logo_width, height=logo_height, mask='auto')
            except Exception:
                pass  # Ignorar si el logo no se carga en páginas subsecuentes

            c.setFont("Helvetica-Bold", 11)
            c.drawString(goleman_text_x, goleman_text_y_goleman, "Goleman")
            c.setFont("Helvetica", 8)
            c.drawString(goleman_text_x, goleman_text_y_ips, "IPS")
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(page_width / 2, page_height - 60, "FORMATO DE ASISTENCIA ATENCIÓN DOMICILIARIA")

            # Header section (Top Right Box)
            c.rect(header_box_x, header_box_y, header_box_width, header_box_height)
            for j in range(1, 4):
                c.line(header_box_x, header_box_y + j * line_spacing, header_box_x + header_box_width,
                       header_box_y + j * line_spacing)
            c.line(header_box_x + 40, header_box_y, header_box_x + 40, header_box_y + header_box_height)
            c.setFont("Helvetica", 7)
            c.drawString(header_box_x + 5, header_box_y + 38, "Código")
            c.drawString(header_box_x + 5, header_box_y + 26, "Fecha")
            c.drawString(header_box_x + 5, header_box_y + 14, "Versión")
            c.drawString(header_box_x + 5, header_box_y + 2, "Página")
            c.drawString(header_box_x + 45, header_box_y + 38, "SIN-PHD-FR-001")
            c.drawString(header_box_x + 45, header_box_y + 26, "15/05/2024")
            c.drawString(header_box_x + 45, header_box_y + 14, "2")
            c.drawString(header_box_x + 45, header_box_y + 2,
                         f"1 de {len(data_entries)}")  # Considera un contador de páginas real aquí
            # (Simplificado: para un contador de páginas real tendrías que pre-calcular o usar un callback)

            c.setFont("Helvetica-Bold", 8)
            c.drawString(60, page_height - 130, "JORNADA HORARIA:")
            c.drawString(400, page_height - 130, "HOSPITALIZACIÓN DOMICILIARIA")

            c.setFont("Helvetica", 8)
            current_y = table_start_y - 45 - (row_height / 2)  # Restablecer Y para la nueva página

            # Volver a dibujar líneas verticales de la tabla
            c.line(left_margin_table, table_start_y, left_margin_table, table_end_y)
            current_x_re = left_margin_table
            for key in ["fecha", "hora", "documento_de_identidad", "eps", "nombre", "procedimiento",
                        "familiar_signature", "collaborator_signature"]:
                current_x_re += col_widths[key]
                c.line(current_x_re, table_start_y, current_x_re, table_end_y)

            # Volver a dibujar líneas horizontales de los encabezados
            c.line(left_margin_table, table_start_y, right_margin_table, table_start_y)
            c.line(left_margin_table, table_start_y - 25, right_margin_table, table_start_y - 25)
            c.line(left_margin_table, table_start_y - 45, right_margin_table, table_start_y - 45)

            # Volver a dibujar encabezados de columna
            c.setFont("Helvetica-Bold", 7)
            draw_centered_column_text("FECHA", col_x["fecha"], col_widths["fecha"], table_start_y - 12)
            draw_centered_column_text("(DÍA/MES/AÑO)", col_x["fecha"], col_widths["fecha"], table_start_y - 22)
            draw_centered_column_text("HORA", col_x["hora"], col_widths["hora"], table_start_y - 17)
            draw_centered_column_text("DOCUMENTO DE", col_x["documento_de_identidad"],
                                      col_widths["documento_de_identidad"], table_start_y - 12)
            draw_centered_column_text("IDENTIDAD", col_x["documento_de_identidad"],
                                      col_widths["documento_de_identidad"], table_start_y - 22)
            draw_centered_column_text("EPS", col_x["eps"], col_widths["eps"], table_start_y - 17)
            draw_centered_column_text("NOMBRE", col_x["nombre"], col_widths["nombre"], table_start_y - 17)
            draw_centered_column_text("PROCEDIMIENTO", col_x["procedimiento"], col_widths["procedimiento"],
                                      table_start_y - 17)
            draw_centered_column_text("NOMBRE/FIRMA", col_x["familiar_signature"], col_widths["familiar_signature"],
                                      table_start_y - 12)
            draw_centered_column_text("FAMILIAR", col_x["familiar_signature"], col_widths["familiar_signature"],
                                      table_start_y - 22)
            draw_centered_column_text("NOMBRE/FIRMA", col_x["collaborator_signature"],
                                      col_widths["collaborator_signature"], table_start_y - 12)
            draw_centered_column_text("COLABORADOR", col_x["collaborator_signature"],
                                      col_widths["collaborator_signature"], table_start_y - 22)
            c.setFont("Helvetica", 8)

        text_y_pos = current_y

        draw_text_in_column(c, entry.get("fecha", ""), col_x["fecha"], col_widths["fecha"], text_y_pos, centered=False)
        draw_text_in_column(c, entry.get("hora", ""), col_x["hora"], col_widths["hora"], text_y_pos, centered=False)
        draw_text_in_column(c, entry.get("documento_de_identidad", ""), col_x["documento_de_identidad"],
                            col_widths["documento_de_identidad"], text_y_pos, centered=False)
        draw_text_in_column(c, entry.get("eps", ""), col_x["eps"], col_widths["eps"], text_y_pos, centered=False)
        draw_text_in_column(c, entry.get("nombre", ""), col_x["nombre"], col_widths["nombre"], text_y_pos,
                            centered=False)
        draw_text_in_column(c, entry.get("procedimiento", ""), col_x["procedimiento"], col_widths["procedimiento"],
                            text_y_pos, centered=False)

        familiar_sig_text = entry.get("nombre_firma_familiar", "")
        collaborator_sig_text = entry.get("nombre_firma_colaborador", "")

        draw_text_in_column(c, familiar_sig_text, col_x["familiar_signature"], col_widths["familiar_signature"],
                            text_y_pos)
        draw_text_in_column(c, collaborator_sig_text, col_x["collaborator_signature"],
                            col_widths["collaborator_signature"], text_y_pos)

        current_y -= row_height

    # Dibuja la línea inferior final de la tabla
    c.line(left_margin_table, table_end_y, right_margin_table, table_end_y)

    c.save()
    buffer.seek(0)  # Vuelve al inicio del buffer
    return buffer


# --- Aplicación Streamlit ---

st.set_page_config(layout="wide", page_title="Generador de Asistencia")

st.title("Generador de Formato de Asistencia Domiciliaria")

st.markdown("""
Esta aplicación te permite generar un formato de asistencia para atención domiciliaria.
Ingresa los datos de cada entrada y agrégala a la lista. Cuando estés listo, genera el PDF.
""")

# Inicializar o acceder al estado de la sesión para las entradas de datos
if 'data_entries' not in st.session_state:
    st.session_state.data_entries = []

# --- Sección para agregar una nueva entrada ---
st.header("1. Datos de la Entrada Actual")

# Campos de entrada
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        fecha_input = st.text_input("Fecha (Día/Mes/Año):", value="28/07/2025")
        documento_input = st.text_input("Documento de Identidad:", value="12345678")
        nombre_input = st.text_input("Nombre del Paciente:", value="Paciente Ejemplo")
        familiar_firma_input = st.text_input("Nombre/Firma Familiar:", value="Familiar de Prueba")
    with col2:
        hora_input = st.text_input("Hora:", value="10:00")
        eps_input = st.text_input("EPS:", value="Nueva EPS")
        procedimiento_input = st.text_input("Procedimiento:", value="Terapia Respiratoria")
        colaborador_firma_input = st.text_input("Nombre/Firma Colaborador:", value="Colaborador Prueba")

    if st.button("Agregar Entrada a la Lista", use_container_width=True):
        if fecha_input and documento_input and nombre_input and procedimiento_input:  # Validación básica
            new_entry = {
                "fecha": fecha_input,
                "hora": hora_input,
                "documento_de_identidad": documento_input,
                "eps": eps_input,
                "nombre": nombre_input,
                "procedimiento": procedimiento_input,
                "nombre_firma_familiar": familiar_firma_input,  # Clave corregida
                "nombre_firma_colaborador": colaborador_firma_input  # Clave corregida
            }
            st.session_state.data_entries.append(new_entry)
            st.success("Entrada agregada con éxito.")
            # st.experimental_rerun() # Opcional: para limpiar los campos de entrada inmediatamente
        else:
            st.warning("Por favor, complete al menos Fecha, Documento, Nombre y Procedimiento.")

# --- Sección para ver y gestionar entradas agregadas ---
st.header("2. Entradas Agregadas")

if st.session_state.data_entries:
    # Mostrar las entradas en una tabla para una mejor visualización
    st.dataframe(st.session_state.data_entries, use_container_width=True, hide_index=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Limpiar Todas las Entradas", use_container_width=True):
            if st.session_state.data_entries and st.warning("¿Está seguro de que desea limpiar todas las entradas?"):
                st.session_state.data_entries = []
                st.success("Todas las entradas han sido limpiadas.")
                st.rerun()  # Para actualizar la UI
            elif not st.session_state.data_entries:
                st.info("No hay entradas para limpiar.")

else:
    st.info("Aún no hay entradas agregadas. Usa el formulario de arriba para añadir datos.")

# --- Sección para generar el PDF ---
st.header("3. Generar PDF")

if st.session_state.data_entries:
    # Botón para generar y descargar el PDF
    pdf_buffer = generate_attendance_pdf(st.session_state.data_entries)

    st.download_button(
        label="Descargar PDF de Asistencia",
        data=pdf_buffer,
        file_name="Formato_Asistencia_Domiciliaria.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    st.success("PDF listo para descargar.")
else:
    st.warning("Agrega al menos una entrada para poder generar el PDF.")

st.markdown("---")
st.write("Creado con Streamlit y ReportLab.")