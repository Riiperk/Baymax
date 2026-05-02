# ==============================================================================
# MODULO_MEMORIA.PY - SISTEMA DE MEMORIA INTELIGENTE BAYX (V21.0)
# ==============================================================================
# INNOVACIÓN V21.0: Memoria persistente con patrones médicos reales.
# Bayx ahora recuerda síntomas frecuentes, emociones recurrentes y
# puede hacer seguimiento entre sesiones como un médico de cabecera.
# ==============================================================================

import json
import os
from datetime import datetime, timedelta
from collections import Counter

ARCHIVO_MEMORIA = "memoria_paciente.json"
CARPETA_REPORTES = "Reportes_Clinicos"

# Palabras sin valor médico que NO deben guardarse
STOP_WORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero",
    "si", "no", "yo", "tu", "el", "ella", "para", "por", "con", "a", "de",
    "en", "que", "es", "me", "te", "se", "mi", "mis", "su", "sus", "como",
    "estoy", "esta", "estamos", "son", "soy", "al", "del", "lo", "le", "mas",
    "noooo", "pues", "aja", "bueno", "entonces", "algo", "nada", "todo",
    "muy", "bien", "mal", "asi", "aca", "alla", "aqui", "hay", "hoy",
    "tomahawk", "parece", "siento", "puedo", "tengo", "quiero", "voy",
    "hacer", "decir", "ver", "saber", "poder", "tener", "estar", "ser"
}

# Síntomas válidos que SÍ deben guardarse en el historial
SINTOMAS_VALIDOS = [
    "cabeza", "migraña", "jaqueca", "mareo", "vertigo",
    "ojo", "ojos", "vista", "vision",
    "oido", "oidos", "zumbido", "sordera",
    "diente", "muela", "boca", "encias",
    "pecho", "corazon", "taquicardia", "palpitacion",
    "tos", "garganta", "gripe", "resfriado", "asma",
    "estomago", "nausea", "vomito", "diarrea", "gastritis",
    "espalda", "lumbar", "columna", "cuello",
    "brazo", "hombro", "codo", "muñeca", "mano",
    "pierna", "rodilla", "tobillo", "pie", "calambre",
    "piel", "alergia", "sarpullido", "quemadura",
    "fiebre", "escalofrio", "temperatura",
    "sueño", "insomnio", "cansancio", "fatiga",
    "tristeza", "ansiedad", "estres", "depresion"
]

if not os.path.exists(CARPETA_REPORTES):
    os.makedirs(CARPETA_REPORTES)

# ==============================================================================
# 1. CARGA Y GUARDADO DEL PERFIL
# ==============================================================================
def cargar_perfil() -> dict:
    if os.path.exists(ARCHIVO_MEMORIA):
        try:
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
                perfil = json.load(f)
                # Migramos perfiles viejos al nuevo formato
                return migrar_perfil(perfil)
        except Exception as e:
            print(f"⚠️ [Memoria corrupta, recreando... {e}]")

    perfil_base = crear_perfil_base()
    guardar_perfil(perfil_base)
    return perfil_base

def crear_perfil_base() -> dict:
    """Crea un perfil nuevo con la estructura inteligente completa."""
    return {
        "nombre": "Paciente",
        "sesiones_completadas": 0,
        "fecha_primera_sesion": datetime.now().strftime("%Y-%m-%d"),
        "ultima_sesion": datetime.now().strftime("%Y-%m-%d"),

        # Historial médico real
        "historial_sintomas": [],  # Lista de {sintoma, fecha, nivel_dolor}
        "sintomas_frecuentes": {},  # {sintoma: cantidad_de_veces}
        "ultimo_sintoma": "Ninguno",

        # Seguimiento emocional
        "historial_emociones": [],  # Lista de {emocion, fecha}
        "emocion_frecuente": "NEUTRAL",

        # Memoria de contexto (solo palabras médicas relevantes)
        "temas_hablados": [],

        # Patrones detectados por Bayx
        "patrones": {
            "sintoma_recurrente": None,  # Síntoma que aparece más de 2 veces
            "emocion_recurrente": None,  # Emoción dominante
            "sesiones_este_mes": 0
        }
    }

def migrar_perfil(perfil_viejo: dict) -> dict:
    """Convierte perfiles del formato viejo al nuevo sin perder datos."""
    perfil_nuevo = crear_perfil_base()

    # Conservamos datos del perfil viejo
    perfil_nuevo["nombre"] = perfil_viejo.get("nombre", "Paciente")
    perfil_nuevo["sesiones_completadas"] = perfil_viejo.get("sesiones_completadas", 0)
    perfil_nuevo["ultimo_sintoma"] = perfil_viejo.get("ultimo_sintoma", "Ninguno")

    # Si ya tiene el nuevo formato, lo usamos directamente
    if "historial_sintomas" in perfil_viejo:
        return perfil_viejo

    return perfil_nuevo

def guardar_perfil(perfil: dict):
    try:
        with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump(perfil, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"❌ [Error al guardar perfil: {e}]")

# ==============================================================================
# 2. REGISTRO DE SÍNTOMAS Y EMOCIONES
# ==============================================================================
def registrar_sintoma(perfil: dict, sintoma: str, nivel_dolor: int = 0):
    """Guarda el síntoma en el historial y actualiza los patrones."""
    if not sintoma or sintoma == "NINGUNO":
        return

    entrada = {
        "sintoma": sintoma,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "nivel_dolor": nivel_dolor
    }

    # Agregamos al historial
    historial = perfil.get("historial_sintomas", [])
    historial.append(entrada)

    # Mantenemos solo los últimos 50 registros
    if len(historial) > 50:
        historial = historial[-50:]
    perfil["historial_sintomas"] = historial

    # Actualizamos frecuencias
    frecuencias = perfil.get("sintomas_frecuentes", {})
    frecuencias[sintoma] = frecuencias.get(sintoma, 0) + 1
    perfil["sintomas_frecuentes"] = frecuencias

    # Actualizamos último síntoma
    perfil["ultimo_sintoma"] = sintoma

    # Detectamos patrones
    actualizar_patrones(perfil)
    guardar_perfil(perfil)

def registrar_emocion(perfil: dict, emocion: str):
    """Guarda el estado emocional en el historial."""
    if not emocion or emocion == "NEUTRAL":
        return

    entrada = {
        "emocion": emocion,
        "fecha": datetime.now().strftime("%Y-%m-%d")
    }

    historial = perfil.get("historial_emociones", [])
    historial.append(entrada)

    if len(historial) > 30:
        historial = historial[-30:]
    perfil["historial_emociones"] = historial

    guardar_perfil(perfil)

def actualizar_patrones(perfil: dict):
    """Analiza el historial y detecta patrones médicos importantes."""
    frecuencias = perfil.get("sintomas_frecuentes", {})

    # Detectamos síntoma recurrente (más de 2 veces)
    if frecuencias:
        sintoma_top = max(frecuencias, key=frecuencias.get)
        if frecuencias[sintoma_top] >= 2:
            perfil["patrones"]["sintoma_recurrente"] = sintoma_top

    # Detectamos emoción dominante
    historial_emociones = perfil.get("historial_emociones", [])
    if historial_emociones:
        emociones = [e["emocion"] for e in historial_emociones[-10:]]
        if emociones:
            emocion_top = Counter(emociones).most_common(1)[0][0]
            perfil["patrones"]["emocion_recurrente"] = emocion_top

# ==============================================================================
# 3. GENERACIÓN DEL SALUDO INTELIGENTE
# ==============================================================================
def generar_saludo_inteligente(perfil: dict) -> str:
    """
    Genera un saludo personalizado basado en el historial del paciente.
    Esto es lo que hace que Bayx parezca que realmente recuerda al paciente.
    """
    patrones = perfil.get("patrones", {})
    historial = perfil.get("historial_sintomas", [])
    sesiones = perfil.get("sesiones_completadas", 0)
    ultimo_sintoma = perfil.get("ultimo_sintoma", "Ninguno")
    sintoma_recurrente = patrones.get("sintoma_recurrente")
    emocion_recurrente = patrones.get("emocion_recurrente")

    # Primera sesión
    if sesiones == 0:
        return None  # Usa el saludo estándar de main.py

    # Síntoma recurrente detectado
    if sintoma_recurrente and perfil.get("sintomas_frecuentes", {}).get(sintoma_recurrente, 0) >= 3:
        return (
            f"Hola de nuevo. Mis registros muestran que has reportado molestias en tu "
            f"{sintoma_recurrente} en {perfil['sintomas_frecuentes'][sintoma_recurrente]} ocasiones. "
            f"¿Cómo está esa zona hoy?"
        )

    # Seguimiento del último síntoma reciente (menos de 3 días)
    if historial:
        ultima_entrada = historial[-1]
        fecha_ultima = datetime.strptime(ultima_entrada["fecha"], "%Y-%m-%d")
        dias_transcurridos = (datetime.now() - fecha_ultima).days

        if dias_transcurridos <= 3 and ultima_entrada["sintoma"] != "NINGUNO":
            return (
                f"Hola de nuevo. En mi última sesión registré molestias en tu "
                f"{ultima_entrada['sintoma']}. Han pasado {dias_transcurridos} día(s). "
                f"¿Cómo te encuentras hoy?"
            )

    # Patrón emocional detectado
    if emocion_recurrente and emocion_recurrente in ["TRISTEZA", "ANSIEDAD"]:
        return (
            f"Hola de nuevo. He notado que en sesiones recientes has experimentado "
            f"estados de {emocion_recurrente.lower()}. ¿Cómo te sientes emocionalmente hoy?"
        )

    # Saludo estándar con memoria de sesiones
    if ultimo_sintoma and ultimo_sintoma != "Ninguno":
        return (
            f"Hola de nuevo. En mi último escaneo registré una anomalía en tu "
            f"{ultimo_sintoma}. ¿Cómo te sientes el día de hoy?"
        )

    return None

# ==============================================================================
# 4. FILTRO SEMÁNTICO MEJORADO
# ==============================================================================
def extraer_palabras_clave(texto: str) -> list:
    """Filtra y extrae SOLO conceptos médicamente relevantes."""
    palabras = texto.lower().split()
    palabras_limpias = [p.strip(".,!?¡¿") for p in palabras]

    # Solo guardamos palabras que están en la lista de síntomas válidos
    # o que son mayores a 4 letras y no son stop words
    claves = []
    for p in palabras_limpias:
        if p in SINTOMAS_VALIDOS:
            claves.append(p)
        elif len(p) > 4 and p not in STOP_WORDS:
            claves.append(p)

    return claves

def actualizar_historial_temas(perfil: dict, texto_usuario: str):
    """Actualiza la memoria de contexto solo con palabras relevantes."""
    nuevos_temas = extraer_palabras_clave(texto_usuario)

    if nuevos_temas:
        temas_actuales = perfil.get("temas_hablados", [])

        for tema in nuevos_temas:
            if tema not in temas_actuales:
                temas_actuales.append(tema)

        # Máximo 15 temas relevantes
        if len(temas_actuales) > 15:
            temas_actuales = temas_actuales[-15:]

        perfil["temas_hablados"] = temas_actuales
        guardar_perfil(perfil)

# ==============================================================================
# 5. EXPORTACIÓN MÉDICA
# ==============================================================================
def generar_reporte_final(perfil: dict, estado) -> str:
    """Genera el reporte clínico final con toda la información de la sesión."""
    perfil["sesiones_completadas"] = perfil.get("sesiones_completadas", 0) + 1
    perfil["ultima_sesion"] = datetime.now().strftime("%Y-%m-%d")

    # Registramos el síntoma y emoción de esta sesión
    if estado.sintoma_actual and estado.sintoma_actual != "NINGUNO":
        registrar_sintoma(perfil, estado.sintoma_actual, estado.nivel_dolor)
    if estado.emocion and estado.emocion != "NEUTRAL":
        registrar_emocion(perfil, estado.emocion)

    guardar_perfil(perfil)

    fecha_actual = datetime.now()
    timestamp = fecha_actual.strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"Escaneo_Bayx_{timestamp}.txt"
    ruta_completa = os.path.join(CARPETA_REPORTES, nombre_archivo)
    fecha_legible = fecha_actual.strftime("%d/%m/%Y a las %H:%M:%S")

    # Análisis de patrones para el reporte
    sintoma_recurrente = perfil.get("patrones", {}).get("sintoma_recurrente", "Ninguno")
    emocion_recurrente = perfil.get("patrones", {}).get("emocion_recurrente", "NEUTRAL")
    frecuencias = perfil.get("sintomas_frecuentes", {})
    top_sintomas = sorted(frecuencias.items(), key=lambda x: x[1], reverse=True)[:3]

    contenido = f"""
=========================================================
  (●—●)  REPORTE MÉDICO OFICIAL - SISTEMA BAYX V21.0
=========================================================
FECHA DE ESCANEO  : {fecha_legible}
PACIENTE          : {perfil.get('nombre', 'Desconocido')}
ID DE SESIÓN      : #{perfil.get('sesiones_completadas')}
PRIMERA SESIÓN    : {perfil.get('fecha_primera_sesion', 'N/A')}
=========================================================

[ DIAGNÓSTICO DE ESTA SESIÓN ]
> Anomalía Detectada  : {estado.sintoma_actual if estado.sintoma_actual != "NINGUNO" else "Ninguna"}
> Nivel de Malestar   : {estado.nivel_dolor}/10
> Categoría Anatómica : {estado.categoria_actual.upper()}

[ MONITOREO EMOCIONAL ]
> Estado Esta Sesión  : {estado.emocion}
> Emoción Recurrente  : {emocion_recurrente}
> Terapia Musical     : {"Aplicada" if estado.musica_reproduciéndose else "No requerida"}
> Interacciones       : {estado.turnos} ciclos

[ HISTORIAL MÉDICO - PATRONES DETECTADOS ]
> Síntoma Recurrente  : {sintoma_recurrente if sintoma_recurrente else "Sin patrón detectado aún"}
> Top Síntomas        : {", ".join([f"{s}({c}x)" for s,c in top_sintomas]) if top_sintomas else "Primera sesión"}

[ MEMORIA NEURONAL ]
> Conceptos Clave     : {", ".join(perfil.get("temas_hablados", []))}
> Total Sesiones      : {perfil.get('sesiones_completadas')}

=========================================================
Sistemas de soporte vital y monitoreo en reposo.
=========================================================
"""
    try:
        with open(ruta_completa, "w", encoding="utf-8") as f:
            f.write(contenido)
        return nombre_archivo
    except Exception as e:
        print(f"❌ [Error al compilar el reporte: {e}]")
        return None