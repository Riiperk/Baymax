import json
import os
from datetime import datetime

# =================================================================
# 1. CONFIGURACIÓN DE RUTAS Y CONSTANTES
# =================================================================
ARCHIVO_MEMORIA = "memoria_paciente.json"
CARPETA_REPORTES = "Reportes_Clinicos"

# Palabras sin valor semántico que Bayx debe ignorar al memorizar temas
STOP_WORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero", 
    "si", "no", "yo", "tu", "el", "ella", "para", "por", "con", "a", "de", 
    "en", "que", "es", "me", "te", "se", "mi", "mis", "su", "sus", "como",
    "estoy", "esta", "estamos", "son", "soy", "al", "del", "lo", "le", "mas"
}

# Nos aseguramos de que exista la carpeta para los escaneos médicos
if not os.path.exists(CARPETA_REPORTES):
    os.makedirs(CARPETA_REPORTES)

# =================================================================
# 2. GESTIÓN DEL PERFIL DEL PACIENTE (Lectura/Escritura JSON)
# =================================================================

def cargar_perfil() -> dict:
    """
    Carga el perfil del paciente desde el disco.
    Si es la primera vez que se enciende Bayx, crea un perfil en blanco.
    """
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except Exception as e:
            print(f"⚠️ [Aviso de Memoria: El archivo de memoria está corrupto. Recreando... {e}]")
            
    # Perfil predeterminado de San Fransokyo
    perfil_base = {
        "nombre": "Paciente",
        "ultimo_sintoma": "Ninguno",
        "temas_hablados": [],
        "sesiones_completadas": 0
    }
    guardar_perfil(perfil_base)
    return perfil_base

def guardar_perfil(perfil: dict):
    """Guarda los cambios de la sesión actual en el disco duro."""
    try:
        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as archivo:
            json.dump(perfil, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ [Error Crítico al escribir en el disco: {e}]")

# =================================================================
# 3. FILTRO SEMÁNTICO (La "Conciencia" de la charla)
# =================================================================

def extraer_palabras_clave(texto: str) -> list:
    """Filtra la oración del paciente y extrae solo conceptos importantes."""
    palabras = texto.lower().split()
    # Limpiamos signos de puntuación pegados a las palabras
    palabras_limpias = [p.strip(".,!?¡¿") for p in palabras]
    
    # Nos quedamos solo con palabras mayores a 3 letras que no sean stop words
    claves = [p for p in palabras_limpias if p not in STOP_WORDS and len(p) > 3]
    return claves

def actualizar_historial_temas(perfil: dict, texto_usuario: str):
    """
    Actualiza la memoria a corto plazo del paciente.
    Mantiene un máximo de 10 conceptos clave para que Ollama sepa el contexto.
    """
    nuevos_temas = extraer_palabras_clave(texto_usuario)
    
    if nuevos_temas:
        # Añadimos los nuevos temas a la lista existente
        temas_actuales = perfil.get("temas_hablados", [])
        
        for tema in nuevos_temas:
            # Evitamos duplicados consecutivos
            if tema not in temas_actuales:
                temas_actuales.append(tema)
                
        # Lógica de "Olvido Sano" (Solo guardamos los últimos 10 temas)
        if len(temas_actuales) > 10:
            temas_actuales = temas_actuales[-10:]
            
        perfil["temas_hablados"] = temas_actuales
        guardar_perfil(perfil)

# =================================================================
# 4. EXPORTACIÓN MÉDICA (El Escaneo Final)
# =================================================================

def generar_reporte_final(perfil: dict, estado) -> str:
    """
    Genera un archivo de texto con el formato de una máquina médica.
    Resume toda la sesión para el registro de salud.
    """
    # Actualizamos el contador de sesiones
    perfil["sesiones_completadas"] = perfil.get("sesiones_completadas", 0) + 1
    guardar_perfil(perfil)

    # Creamos un nombre de archivo único basado en la fecha y hora
    fecha_actual = datetime.now()
    timestamp = fecha_actual.strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"Escaneo_Bayx_{timestamp}.txt"
    ruta_completa = os.path.join(CARPETA_REPORTES, nombre_archivo)
    
    # Formato de la fecha para lectura humana
    fecha_legible = fecha_actual.strftime("%d/%m/%Y a las %H:%M:%S")

    # Construcción de la interfaz de texto (ASCII Art)
    contenido = f"""
=========================================================
  (●—●)  REPORTE MÉDICO OFICIAL - SISTEMA BAYX
=========================================================
FECHA DE ESCANEO : {fecha_legible}
PACIENTE         : {perfil.get('nombre', 'Desconocido')}
ID DE SESIÓN     : #{perfil.get('sesiones_completadas')}
=========================================================

[ DIAGNÓSTICO PRINCIPAL ]
> Anomalía Detectada : {estado.sintoma_actual if estado.sintoma_actual else "Ninguna (Paciente Estable)"}
> Nivel de Dolor     : {estado.nivel_dolor}/10
> Categoría Anatómica: {estado.categoria_actual.upper() if estado.categoria_actual else "N/A"}

[ MONITOREO EMOCIONAL ]
> Estado Químico     : Niveles asociados a '{estado.emocion.upper()}'
> Terapia Musical    : {"Aplicada exitosamente" if estado.musica_reproduciéndose else "No requerida"}
> Interacciones      : {estado.turnos} ciclos de comunicación.

[ MEMORIA NEURONAL A CORTO PLAZO ]
> Últimos conceptos  : {", ".join(perfil.get("temas_hablados", []))}

=========================================================
El paciente ha declarado estar satisfecho con su cuidado.
Sistemas de soporte vital y monitoreo en reposo.
=========================================================
"""
    try:
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        return nombre_archivo
    except Exception as e:
        print(f"❌ [Error al compilar el reporte médico: {e}]")
        return None