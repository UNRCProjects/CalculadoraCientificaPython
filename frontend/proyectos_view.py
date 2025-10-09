import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def render_activos():
    """Vista para proyectos activos"""
    st.header("🤝 Proyectos de Servicio Social Activos")
    
    # Simulación de proyectos activos
    proyectos_data = [
        {
            'proyecto': 'Desarrollo de plataforma educativa',
            'empresa': 'Secretaría de Educación Pública',
            'estudiante': 'Juan Pérez García',
            'matricula': 'LCDN2025001',
            'fecha_inicio': '2025-01-15',
            'fecha_fin': '2025-07-15',
            'horas_completadas': 120,
            'horas_totales': 480,
            'estatus': 'En progreso',
            'modalidad': 'Híbrido'
        },
        {
            'proyecto': 'Análisis de datos demográficos',
            'empresa': 'Instituto Nacional de Estadística',
            'estudiante': 'María González López',
            'matricula': 'LCDN2025002',
            'fecha_inicio': '2025-01-10',
            'fecha_fin': '2025-05-10',
            'horas_completadas': 200,
            'horas_totales': 480,
            'estatus': 'En progreso',
            'modalidad': 'Presencial'
        }
    ]
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        empresa_filter = st.selectbox("Filtrar por empresa", ["Todas", "Secretaría de Educación Pública", "Instituto Nacional de Estadística"])
    
    with col2:
        estatus_filter = st.selectbox("Filtrar por estatus", ["Todos", "En progreso", "Completado", "Pausado"])
    
    with col3:
        modalidad_filter = st.selectbox("Filtrar por modalidad", ["Todas", "Presencial", "Híbrido", "Remoto"])
    
    # Lista de proyectos
    for i, proyecto in enumerate(proyectos_data):
        with st.expander(f"📋 {proyecto['proyecto']} - {proyecto['estatus']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Empresa:** {proyecto['empresa']}")
                st.write(f"**Estudiante:** {proyecto['estudiante']}")
                st.write(f"**Matrícula:** {proyecto['matricula']}")
                st.write(f"**Modalidad:** {proyecto['modalidad']}")
            
            with col2:
                st.write(f"**Fecha inicio:** {proyecto['fecha_inicio']}")
                st.write(f"**Fecha fin:** {proyecto['fecha_fin']}")
                st.write(f"**Horas completadas:** {proyecto['horas_completadas']}/{proyecto['horas_totales']}")
                
                # Barra de progreso
                progreso = proyecto['horas_completadas'] / proyecto['horas_totales']
                st.progress(progreso)
                st.write(f"Progreso: {progreso:.1%}")
            
            # Acciones
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button(f"📊 Ver reportes", key=f"reportes_{i}"):
                    st.info("📊 Redirigiendo a reportes del proyecto...")
            
            with col2:
                if st.button(f"📝 Registrar horas", key=f"horas_{i}"):
                    st.info("📝 Abriendo formulario de registro de horas...")
            
            with col3:
                if st.button(f"📧 Contactar", key=f"contactar_{i}"):
                    st.info("📧 Abriendo cliente de correo...")
    
    # Estadísticas generales
    st.subheader("📊 Estadísticas Generales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Proyectos Activos", len(proyectos_data))
    
    with col2:
        total_horas = sum([p['horas_completadas'] for p in proyectos_data])
        st.metric("Horas Completadas", total_horas)
    
    with col3:
        promedio_progreso = sum([p['horas_completadas']/p['horas_totales'] for p in proyectos_data]) / len(proyectos_data)
        st.metric("Progreso Promedio", f"{promedio_progreso:.1%}")
    
    with col4:
        proyectos_completados = len([p for p in proyectos_data if p['estatus'] == 'Completado'])
        st.metric("Proyectos Completados", proyectos_completados)

def render_nuevo():
    """Vista para crear nuevo proyecto"""
    st.header("➕ Nuevo Proyecto de Servicio Social")
    
    st.markdown("""
    ### 📝 Crear un nuevo proyecto de vinculación
    Complete la información para crear un nuevo proyecto de servicio social.
    """)
    
    with st.form("nuevo_proyecto_form"):
        st.subheader("📋 Información del Proyecto")
        
        titulo = st.text_input("Título del proyecto *", value="Desarrollo de sistema de gestión educativa")
        descripcion = st.text_area("Descripción detallada *", value="Desarrollo de una plataforma web para la gestión de proyectos educativos, incluyendo módulos de seguimiento y reportes.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            empresa = st.selectbox("Empresa *", ["Secretaría de Educación Pública", "Instituto Nacional de Estadística", "Fundación Televisa"])
            modalidad = st.selectbox("Modalidad *", ["Presencial", "Híbrido", "Remoto"])
            duracion = st.selectbox("Duración *", ["3 meses", "4 meses", "6 meses", "8 meses", "12 meses"])
        
        with col2:
            ubicacion = st.text_input("Ubicación *", value="CDMX")
            horario = st.text_input("Horario de trabajo", value="9:00 AM - 5:00 PM")
            fecha_inicio = st.date_input("Fecha de inicio *", value=datetime.now().date())
        
        st.subheader("👨‍🎓 Información del Estudiante")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_estudiante = st.text_input("Nombre del estudiante *", value="Juan Pérez García")
            matricula = st.text_input("Matrícula *", value="LCDN2025001")
            carrera = st.text_input("Carrera *", value="Licenciatura en Ciencia de Datos para Negocios")
        
        with col2:
            semestre = st.number_input("Semestre *", min_value=1, max_value=12, value=8)
            promedio = st.number_input("Promedio", min_value=0.0, max_value=10.0, value=8.5)
            telefono = st.text_input("Teléfono", value="55-1234-5678")
        
        st.subheader("📋 Requisitos y Objetivos")
        
        objetivos = st.text_area("Objetivos del proyecto *", value="1. Desarrollar una plataforma web funcional\n2. Implementar sistema de reportes\n3. Capacitar al personal en el uso del sistema")
        requisitos = st.text_area("Requisitos técnicos", value="Conocimientos en Python, SQL, desarrollo web")
        entregables = st.text_area("Entregables esperados", value="1. Plataforma web funcional\n2. Manual de usuario\n3. Documentación técnica")
        
        st.subheader("📊 Configuración de Horas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            horas_totales = st.number_input("Horas totales del proyecto *", min_value=1, value=480)
            horas_semanales = st.number_input("Horas por semana", min_value=1, value=20)
        
        with col2:
            dias_semana = st.number_input("Días por semana", min_value=1, max_value=7, value=5)
            horas_dia = st.number_input("Horas por día", min_value=1, value=4)
        
        # Configuración de seguimiento
        st.subheader("📈 Configuración de Seguimiento")
        
        reportes_mensuales = st.checkbox("Requiere reportes mensuales", value=True)
        supervisor = st.text_input("Supervisor del proyecto", value="María González López")
        email_supervisor = st.text_input("Correo del supervisor", value="maria.gonzalez@empresa.com")
        
        crear_proyecto = st.form_submit_button("🚀 Crear Proyecto")
        
        if crear_proyecto:
            st.success("✅ Proyecto creado exitosamente")
            st.info("📧 Se enviará notificación al estudiante y supervisor")

def render_historial():
    """Vista para historial de proyectos"""
    st.header("📚 Historial de Proyectos")
    
    # Simulación de historial
    historial_data = [
        {
            'proyecto': 'Desarrollo de aplicación móvil',
            'empresa': 'Fundación Televisa',
            'estudiante': 'Ana Martínez',
            'fecha_inicio': '2024-06-01',
            'fecha_fin': '2024-12-01',
            'horas_totales': 480,
            'estatus': 'Completado',
            'calificacion': 9.5
        },
        {
            'proyecto': 'Análisis de datos de salud',
            'empresa': 'Secretaría de Salud',
            'estudiante': 'Carlos López',
            'fecha_inicio': '2024-03-01',
            'fecha_fin': '2024-09-01',
            'horas_totales': 480,
            'estatus': 'Completado',
            'calificacion': 9.0
        }
    ]
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        año_filter = st.selectbox("Filtrar por año", ["Todos", "2024", "2025"])
    
    with col2:
        estatus_filter = st.selectbox("Filtrar por estatus", ["Todos", "Completado", "Cancelado", "En progreso"])
    
    with col3:
        empresa_filter = st.selectbox("Filtrar por empresa", ["Todas", "Fundación Televisa", "Secretaría de Salud"])
    
    # Tabla de historial
    df = pd.DataFrame(historial_data)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        # Estadísticas del historial
        st.subheader("📊 Estadísticas del Historial")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Proyectos", len(historial_data))
        
        with col2:
            completados = len([p for p in historial_data if p['estatus'] == 'Completado'])
            st.metric("Proyectos Completados", completados)
        
        with col3:
            promedio_calificacion = sum([p['calificacion'] for p in historial_data]) / len(historial_data)
            st.metric("Calificación Promedio", f"{promedio_calificacion:.1f}")
        
        with col4:
            total_horas = sum([p['horas_totales'] for p in historial_data])
            st.metric("Total Horas", total_horas)
    else:
        st.info("No hay proyectos en el historial aún.")





