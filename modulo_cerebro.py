import re
import requests
import difflib
import time
import random
import spacy
nlp = spacy.load("es_core_news_md")
print("✅ [CEREBRO]: Modelo de lenguaje spaCy cargado.")
from dataclasses import dataclass, field

# ==============================================================================
# 1. ENLACE CON LA INFRAESTRUCTURA DE DATOS MÉDICOS
# ==============================================================================
# Importamos la base de datos de tratamientos y el sistema de memoria persistente.
# El cerebro depende de que estos módulos existan para funcionar al 100%.
try:
    from tratamiento import generar_respuesta_medica, obtener_pregunta_seguimiento, obtener_respuesta_detalle, PROTOCOLOS_MAESTROS
    from modulo_memoria import actualizar_historial_temas, guardar_perfil
except ImportError as e:
    print(f"❌ [CEREBRO - ERROR DE ENLACE]: No se pudo localizar un módulo vital: {e}")

# ==============================================================================
# 2. DEFINICIÓN DEL ESTADO DE CONCIENCIA (DATACLASSE DE ESTADO)
# ==============================================================================
@dataclass
class EstadoSesion:
    """
    Representa la unidad de almacenamiento volátil de Bayx.
    Contiene todas las banderas y variables necesarias para el reporte final.
    ADVERTENCIA: No eliminar atributos; el generador de reportes los requiere.
    """
    # --- Datos de Identidad y Sesión ---
    historial: list = field(default_factory=list)
    turnos: int = 0
    cerrado: bool = False
    
    # --- Variables de Diagnóstico Médico ---
    esperando_escala: bool = False
    esperando_seguimiento: bool = False
    indice_pregunta: int = 0
    sintoma_actual: str = "NINGUNO"
    categoria_actual: str = "GENERAL"  # Crucial para el reporte .txt
    nivel_dolor: int = 0
    
    # --- Monitoreo Químico-Emocional ---
    emocion: str = "NEUTRAL"          # Crucial para el análisis emocional del reporte
    contador_abrazos: int = 0
    
    # --- Control de Actuadores Acústicos ---
    musica_reproduciéndose: bool = False
    modo_alerta_nombre: bool = False
    
    # --- Flags Cinematográficos (Easter Eggs) ---
    esperando_explicacion_punos: bool = False
    modo_bateria_baja: bool = False
    en_estado_alerta: bool = False
    detecto_gato: bool = False

# ==============================================================================
# 3. MATRICES DE PATRONES LINGÜÍSTICOS Y SENTIMIENTOS
# ==============================================================================
PALABRA_CLAVE = "bayx"

# Protocolos de Desactivación Oficial
PATRONES_CIERRE = [
    "estoy satisfecho con mi cuidado", "estoy satisfecha con mi cuidado",
    "estoy satisfecho con tu cuidado", "estoy satisfecha con tu cuidado",
    "estoy satisfecho", "estoy satisfecha",
    "toy satisfecho", "toy satisfecha",
    "satisfecho con", "satisfecha con",
    "ya estoy bien", "puedes irte", "desconectate", "apagate", "chau bayx"
]

# Control Semántico de Terapia Musical
PATRONES_STOP_MUSICA = ["detente", "para la musica", "deten la musica", "silencio", "stop", "apaga la musica", "silencia"]
PATRONES_MUSICA_ANIMO = ["ponme musica", "musica para animarme", "musica de animo", "alegre", "feliz", "animame"]
PATRONES_MUSICA_RELAJAR = ["relajar", "dormir", "calmar", "musica suave", "estoy estresado", "musica relajante", "relax"]

# Easter Eggs y Guion Cinematográfico
PATRONES_MASCOTA = ["gato", "perro", "mascota", "gatito", "perrito", "michi", "hairy baby", "bebe peludo"]
PATRONES_PUNOS = ["choca los puños", "chocar los puños", "choca el puño", "choque de puños"]
PATRONES_ABRAZO = ["dame un abrazo", "quiero un abrazo", "abrazame", "necesito un abrazo"]

# Clasificador de Emociones para el Reporte Clínico
MAPA_EMOCIONES = {
    "ANSIEDAD": ["miedo", "asustado", "preocupado", "nervioso", "ansiedad", "estres", "panico", "asustada"],
    "TRISTEZA": ["triste", "mal", "desanimado", "cansado", "deprimido", "solo", "soledad", "llorar", "lagrimas"],
    "ALEGRIA": ["feliz", "bien", "excelente", "emocionado", "contento", "genial", "super", "alegre"],
    "DOLOR": ["duele", "dolor", "anomalia", "golpe", "herida", "punzada", "quemazon"]
}

# Generación dinámica del diccionario de síntomas desde la matriz de tratamiento.py
TODOS_LOS_SINTOMAS = []
for grupo in PROTOCOLOS_MAESTROS.keys():
    for sinonimo in grupo:
        TODOS_LOS_SINTOMAS.append(sinonimo)

# ==============================================================================
# 4. MOTOR DE PROCESAMIENTO DE LENGUAJE (PNL)
# ==============================================================================
def corregir_fonetica(texto: str) -> str:
    """Ajusta errores comunes en el reconocimiento de voz del nombre 'Bayx'."""
    variaciones = [r"\bbakes\b", r"\bbeiks\b", r"\bbaiks\b", r"\bbaics\b", r"\bvaiks\b", r"\bbaymax\b"]
    for patron in variaciones:
        texto = re.sub(patron, "bayx", texto, flags=re.IGNORECASE)
    return texto

def normalizar_texto(texto: str) -> str:
    """Limpia el string eliminando ruidos, tildes y caracteres especiales."""
    if not texto: return ""
    texto = texto.lower().strip()
    texto = corregir_fonetica(texto)
    # Remplazo manual de caracteres para evitar fallos por codificación
    remplazos = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ñ", "n"))
    for a, b in remplazos:
        texto = texto.replace(a, b)
    # Regex para mantener solo palabras y espacios
    return re.sub(r'[^\w\s]', '', texto)

def analizar_estado_emocional(texto_norm: str, estado: EstadoSesion) -> None:
    """
    Escanea la entrada del paciente para actualizar el monitoreo emocional del sistema.
    Este dato se verá reflejado en el reporte .txt al finalizar la sesión.
    """
    for emocion_id, palabras_clave in MAPA_EMOCIONES.items():
        if any(p in texto_norm for p in palabras_clave):
            estado.emocion = emocion_id
            break

def extraer_escala_dolor(texto: str) -> int:
    """Convierte la respuesta del usuario (letra o dígito) a un entero de 0 a 10."""
    dic_num = {
        'diez':10, 'nueve':9, 'ocho':8, 'siete':7, 'seis':6, 'cinco':5, 
        'cuatro':4, 'tres':3, 'dos':2, 'uno':1, 'cero':0
    }
    # Búsqueda de palabras
    encontrados = [val for pal, val in dic_num.items() if re.search(rf'\b{pal}\b', texto)]
    # Búsqueda de dígitos
    digitos = [int(d) for d in re.findall(r"\b\d+\b", texto) if 0 <= int(d) <= 10]
    encontrados.extend(digitos)
    
    return max(encontrados) if encontrados else None

def identificar_patologia(texto_norm: str):
    """
    Niveles de búsqueda:
    1. Exacta: busca la palabra directamente (rápido)
    2. Semántica: usa spaCy para entender sinónimos y conjugaciones
       Ejemplo: "doliendo" → "doler" → encuentra "dolor"
    """
    # Nivel 1: búsqueda exacta (igual que antes)
    for grupo_sinonimos, respuesta in PROTOCOLOS_MAESTROS.items():
        for sinonimo in grupo_sinonimos:
            if sinonimo in texto_norm:
                return sinonimo, grupo_sinonimos[0].upper()

    # Nivel 2: búsqueda con spaCy (nueva)
    # Convertimos el texto a sus formas base (lemas)
    # Ejemplo: "brazos doliendo" → ["brazo", "doler"]
    doc = nlp(texto_norm)
    lemas_texto = [token.lemma_ for token in doc if not token.is_stop and len(token.text) > 2]

    for grupo_sinonimos, respuesta in PROTOCOLOS_MAESTROS.items():
        for sinonimo in grupo_sinonimos:
            doc_sinonimo = nlp(sinonimo)
            lemas_sinonimo = [token.lemma_ for token in doc_sinonimo]
            if any(lema in lemas_texto for lema in lemas_sinonimo):
                return sinonimo, grupo_sinonimos[0].upper()

    return None, None

# ==============================================================================
# 5. INTEGRACIÓN CON RED NEURONAL EXTERNA (OLLAMA PHI-3)
# ==============================================================================
def consultar_ollama(prompt_usuario: str, estado: EstadoSesion, perfil: dict) -> str:
    """Se conecta al LLM local para generar respuestas de acompañamiento."""
    if estado.musica_reproduciéndose: 
        return "" # Prioridad de silencio durante la musicoterapia activa
        
    url = "http://localhost:11434/api/generate"
    # Instrucciones de comportamiento para mantener la esencia de Baymax
    system_prompt = (
        "Eres Bayx, un robot de asistencia médica de diseño inflable. "
        "Tu tono es calmado, profesional, servicial y extremadamente literal. "
        "No tienes emociones, pero tu objetivo es el bienestar del paciente. "
        "Responde de forma breve (máximo 2 oraciones) y siempre en español."
    )
    
    try:
        payload = {
            "model": "phi3", 
            "prompt": f"{system_prompt}\nPaciente: {prompt_usuario}\nBayx:", 
            "stream": False
        }
        res = requests.post(url, json=payload, timeout=12)
        return res.json().get("response", "").strip()
    except Exception as e:
        print(f"⚠️ [CEREBRO - OLLAMA]: Falló el enlace de datos generativo: {e}")
        return "Mis procesos de lenguaje presentan latencia. Recomiendo esperar."

# ==============================================================================
# 6. CÓRTEX DE DECISIÓN (LÓGICA DE PROCESAMIENTO PRINCIPAL)
# ==============================================================================
def procesar_pensamiento(texto_bruto: str, estado: EstadoSesion, perfil: dict):
    """
    Analiza la entrada del paciente, evalúa el contexto y activa los protocolos correspondientes.
    """
    estado.turnos += 1
    texto_entrada = corregir_fonetica(texto_bruto or "")
    texto_norm = normalizar_texto(texto_entrada)
    
    # Manejo de ruido blanco o entradas vacías
    if not texto_norm:
        return {"id": "vacio", "texto": "", "estado": estado, "cerrar": False}

    # Registro en la memoria volátil de la sesión
    estado.historial.append(f"Paciente: {texto_entrada}")
    
    # --- FASE A: ACTUALIZACIÓN DE ESTADO BIO-EMOCIONAL ---
    analizar_estado_emocional(texto_norm, estado)

    # --- FASE B: PROTOCOLO DE SATISFACCIÓN (CIERRE) ---
    if any(p in texto_norm for p in PATRONES_CIERRE):
        return {
            "id": "cierre", 
            "texto": "Me alegra que estés satisfecho con tu cuidado. Hasta pronto.", 
            "estado": estado, 
            "cerrar": True
        }

    # --- FASE C: PROTOCOLOS CINEMATOGRÁFICOS (EASTER EGGS) ---
    # 1. El Gato (Hairy Baby)
    if any(p in texto_norm for p in PATRONES_MASCOTA):
        return {
            "id": "bebe_peludo", 
            "texto": "Bebé peludo... Bebé peludo. El ronroneo de un gato tiene frecuencias que reducen significativamente el estrés humano.", 
            "estado": estado, 
            "cerrar": False
        }

    # 2. Chocar los puños (Protocolo Balalala)
    if any(p in texto_norm for p in PATRONES_PUNOS):
        estado.esperando_explicacion_punos = True
        return {
            "id": "aprender_punos", 
            "texto": "No reconozco ese movimiento en mis protocolos médicos. ¿Cuál es el propósito de chocar los puños?", 
            "estado": estado, 
            "cerrar": False
        }

    if estado.esperando_explicacion_punos:
        estado.esperando_explicacion_punos = False
        return {
            "id": "balalala", 
            "texto": "Entendido. Procesando nuevo saludo social... ¡Balalala!", 
            "estado": estado, 
            "cerrar": False
        }

    # 3. Protocolo de Abrazos
    if any(p in texto_norm for p in PATRONES_ABRAZO):
        estado.contador_abrazos += 1
        return {
            "id": "abrazo", 
            "texto": "Iniciando protocolo de soporte físico. Los abrazos liberan oxitocina y reducen la ansiedad.", 
            "estado": estado, 
            "cerrar": False
        }

    # 4. Modo Batería Baja
    if "bateria baja" in texto_norm or "descargando" in texto_norm:
        return {
            "id": "bateria", 
            "texto": "Tengo... batería baja. Necesito... mi estación de carga. Estamos en un mundo de maravillas.", 
            "estado": estado, 
            "cerrar": False
        }

    # --- FASE D: GESTIÓN DE MUSICOTERAPIA ---
    # Música de Relajación
    if any(p in texto_norm for p in PATRONES_MUSICA_RELAJAR):
        return {
            "id": "reproducir_musica", 
            "tipo_musica": "relajar", 
            "texto": "He detectado tensión muscular y mental. Iniciando terapia relajante. Respire a mi ritmo.", 
            "estado": estado, 
            "cerrar": False
        }
    
    # Música de Ánimo
    if any(p in texto_norm for p in PATRONES_MUSICA_ANIMO):
        return {
            "id": "reproducir_musica", 
            "tipo_musica": "animo", 
            "texto": "Iniciando terapia musical estimulante para elevar sus niveles de dopamina.", 
            "estado": estado, 
            "cerrar": False
        }

    # Detención de Música
    if estado.musica_reproduciéndose and any(p in texto_norm for p in PATRONES_STOP_MUSICA):
        return {
            "id": "detener_musica", 
            "texto": "Tratamiento de audio detenido.", 
            "estado": estado, 
            "cerrar": False
        }

# --- FASE E: PROTOCOLO MÉDICO Y ESCALA DE DOLOR ---
    if estado.esperando_seguimiento:
        # Buscamos si la respuesta del paciente coincide con algún detalle
        respuesta_detalle = obtener_respuesta_detalle(estado.sintoma_actual, texto_norm)
        
        # Intentamos la siguiente pregunta de seguimiento
        siguiente_pregunta = obtener_pregunta_seguimiento(
            estado.sintoma_actual, 
            estado.indice_pregunta
        )
        
        if respuesta_detalle:
            # Tenemos una respuesta específica, la damos y seguimos con más preguntas
            estado.indice_pregunta += 1
            proxima = obtener_pregunta_seguimiento(estado.sintoma_actual, estado.indice_pregunta)
            if proxima:
                return {
                    "id": "seguimiento",
                    "texto": f"{respuesta_detalle} Además, {proxima}",
                    "estado": estado,
                    "cerrar": False
                }
            else:
                estado.esperando_seguimiento = False
                estado.esperando_escala = True
                return {
                    "id": "seguimiento_final",
                    "texto": f"{respuesta_detalle} En una escala del uno al diez, ¿cómo calificarías tu dolor?",
                    "estado": estado,
                    "cerrar": False
                }
        elif siguiente_pregunta:
            estado.indice_pregunta += 1
            return {
                "id": "seguimiento",
                "texto": siguiente_pregunta,
                "estado": estado,
                "cerrar": False
            }
        else:
            estado.esperando_seguimiento = False
            estado.esperando_escala = True
            return {
                "id": "pedir_escala",
                "texto": "En una escala del uno al diez, ¿cómo calificarías tu dolor?",
                "estado": estado,
                "cerrar": False
            }

    if estado.esperando_escala:
        nivel = extraer_escala_dolor(texto_norm)
        if nivel is not None:
            estado.nivel_dolor = nivel
            estado.esperando_escala = False
            if nivel <= 1:
                return {
                    "id": "pubertad",
                    "texto": "Escaneo completo. No sufrió lesión alguna. Su malestar es propio de cambios naturales.",
                    "estado": estado,
                    "cerrar": False
                }
            consejo = generar_respuesta_medica(estado.sintoma_actual)
            return {
                "id": "consejo_medico",
                "texto": f"He registrado un nivel de dolor de {nivel}. {consejo}",
                "estado": estado,
                "cerrar": False
            }
        return {
            "id": "re_escala",
            "texto": "Por favor indica un valor del uno al diez para calificar tu dolor.",
            "estado": estado,
            "cerrar": False
        }

    # --- FASE F: DETECCIÓN DE NUEVAS ANOMALÍAS (SÍNTOMAS) ---
    sintoma, categoria = identificar_patologia(texto_norm)
    if sintoma:
        estado.sintoma_actual = sintoma
        estado.categoria_actual = categoria  # <--- GUARDADO PARA EL REPORTE FINAL
        estado.esperando_seguimiento = True
        estado.indice_pregunta = 0
        
        # Persistencia en el perfil JSON del usuario
        perfil["ultimo_sintoma"] = sintoma
        guardar_perfil(perfil)
        
        return {
            "id": "pedir_escala", 
            "texto": f"He detectado una anomalía en su {sintoma}. En una escala del uno al diez, ¿cómo calificarías tu dolor?", 
            "estado": estado, 
            "cerrar": False
        }

    # --- FASE G: CHARLA GENERAL Y FALLBACK (OLLAMA) ---
    # Si no se activó ningún protocolo específico, usamos la IA generativa.
    actualizar_historial_temas(perfil, texto_norm)
    respuesta_ia = consultar_ollama(texto_entrada, estado, perfil)
    
    return {
        "id": "charla", 
        "texto": respuesta_ia, 
        "estado": estado, 
        "cerrar": False
    }

# ==============================================================================
# FIN DEL CÓRTEX CEREBRAL v19.0
# ==============================================================================