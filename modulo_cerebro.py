# ==============================================================================
# MODULO_CEREBRO.PY - CÓRTEX CEREBRAL BAYX (V21.0 - BAYMAX EDITION)
# ==============================================================================
import re
import requests
import time
import random
import spacy
from rapidfuzz import fuzz
from dataclasses import dataclass, field

nlp = spacy.load("es_core_news_md")
print("✅ [CEREBRO]: Modelo de lenguaje spaCy cargado.")

# ==============================================================================
# 1. ENLACE CON MÓDULOS VITALES
# ==============================================================================
try:
    from tratamiento import (
        generar_respuesta_medica,
        obtener_pregunta_seguimiento,
        obtener_respuesta_detalle,
        PROTOCOLOS_MAESTROS
    )
    from modulo_memoria import actualizar_historial_temas, guardar_perfil
except ImportError as e:
    print(f"❌ [CEREBRO - ERROR DE ENLACE]: {e}")

# ==============================================================================
# 2. ESTADO DE CONCIENCIA DE LA SESIÓN
# ==============================================================================
@dataclass
class EstadoSesion:
    # Datos de sesión
    historial: list = field(default_factory=list)
    turnos: int = 0
    cerrado: bool = False

    # Diagnóstico médico
    esperando_escala: bool = False
    esperando_seguimiento: bool = False
    indice_pregunta: int = 0
    sintoma_actual: str = "NINGUNO"
    categoria_actual: str = "GENERAL"
    nivel_dolor: int = 0

    # Monitoreo emocional
    emocion: str = "NEUTRAL"
    contador_abrazos: int = 0

    # Actuadores
    musica_reproduciéndose: bool = False
    modo_alerta_nombre: bool = False

    # Easter eggs
    esperando_explicacion_punos: bool = False
    modo_bateria_baja: bool = False
    en_estado_alerta: bool = False
    detecto_gato: bool = False

# ==============================================================================
# 3. PATRONES LINGÜÍSTICOS
# ==============================================================================

PATRONES_CIERRE = [
    "estoy satisfecho con mi cuidado", "estoy satisfecha con mi cuidado",
    "estoy satisfecho con tu cuidado", "estoy satisfecha con tu cuidado",
    "estoy satisfecho", "estoy satisfecha",
    "toy satisfecho", "toy satisfecha",
    "satisfecho con", "satisfecha con",
    "ya estoy bien", "puedes irte", "desconectate", "apagate", "chau bayx"
]

PATRONES_STOP_MUSICA = [
    "detente", "para la musica", "deten la musica", "silencio",
    "stop", "apaga la musica", "silencia", "para la cancion"
]
PATRONES_MUSICA_ANIMO = [
    "ponme musica", "musica para animarme", "musica de animo",
    "alegre", "animame", "pon algo alegre", "musica animada"
]
PATRONES_MUSICA_RELAJAR = [
    "relajar", "dormir", "calmar", "musica suave", "estoy estresado",
    "musica relajante", "relax", "quiero relajarme", "ayudame a calmar"
]

PATRONES_MASCOTA = [
    "gato", "perro", "mascota", "gatito", "perrito",
    "michi", "hairy baby", "bebe peludo"
]
PATRONES_PUNOS = [
    "choca los punos", "chocar los punos", "choca el puno",
    "choque de punos", "choca los puños", "chocar los puños"
]
PATRONES_ABRAZO = [
    "dame un abrazo", "quiero un abrazo", "abrazame",
    "necesito un abrazo", "un abrazo por favor"
]
PATRONES_NOMBRE = [
    "como te llamas", "cual es tu nombre", "quien eres",
    "que eres", "eres un robot", "eres una ia"
]
PATRONES_CREADOR = [
    "quien te creo", "quien te hizo", "quien te programo",
    "quien es tu creador", "quien te diseño"
]
PATRONES_PELICULA = [
    "grandes heroes", "big hero", "hiro", "tadashi", "san fransokyo"
]

# Clasificador de emociones
MAPA_EMOCIONES = {
    "ANSIEDAD": ["miedo", "asustado", "preocupado", "nervioso", "ansiedad", "estres", "panico", "asustada"],
    "TRISTEZA": ["triste", "mal", "desanimado", "cansado", "deprimido", "solo", "soledad", "llorar", "lagrimas"],
    "ALEGRIA": ["feliz", "bien", "excelente", "emocionado", "contento", "genial", "super", "alegre"],
    "DOLOR": ["duele", "dolor", "anomalia", "golpe", "herida", "punzada", "quemazon"]
}

# Lista dinámica de síntomas desde tratamiento.py
TODOS_LOS_SINTOMAS = [s for grupo in PROTOCOLOS_MAESTROS.keys() for s in grupo]

# Partes del cuerpo para diferenciar de sensaciones
PARTES_CUERPO = [
    "cabeza", "brazo", "pierna", "pecho", "espalda", "rodilla",
    "tobillo", "hombro", "cuello", "estomago", "oido", "ojo",
    "garganta", "mano", "pie", "diente", "muela", "piel"
]

# ==============================================================================
# 4. MOTOR DE PROCESAMIENTO DE LENGUAJE
# ==============================================================================
def corregir_fonetica(texto: str) -> str:
    variaciones = [
        r"\bbakes\b", r"\bbeiks\b", r"\bbaiks\b", r"\bbaics\b",
        r"\bvaiks\b", r"\bbaymax\b", r"\bbaix\b", r"\bbayx\b"
    ]
    for patron in variaciones:
        texto = re.sub(patron, "bayx", texto, flags=re.IGNORECASE)
    return texto

def normalizar_texto(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.lower().strip()
    texto = corregir_fonetica(texto)
    remplazos = (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ñ","n"))
    for a, b in remplazos:
        texto = texto.replace(a, b)
    return re.sub(r'[^\w\s]', '', texto)

def analizar_estado_emocional(texto_norm: str, estado: EstadoSesion) -> None:
    for emocion_id, palabras_clave in MAPA_EMOCIONES.items():
        if any(p in texto_norm for p in palabras_clave):
            estado.emocion = emocion_id
            break

def extraer_escala_dolor(texto: str):
    dic_num = {
        'diez':10,'nueve':9,'ocho':8,'siete':7,'seis':6,'cinco':5,
        'cuatro':4,'tres':3,'dos':2,'uno':1,'cero':0
    }
    encontrados = [val for pal, val in dic_num.items() if re.search(rf'\b{pal}\b', texto)]
    digitos = [int(d) for d in re.findall(r"\b\d+\b", texto) if 0 <= int(d) <= 10]
    encontrados.extend(digitos)
    return max(encontrados) if encontrados else None

def identificar_patologia(texto_norm: str):
    # Nivel 1: búsqueda exacta
    for grupo_sinonimos in PROTOCOLOS_MAESTROS.keys():
        for sinonimo in grupo_sinonimos:
            if sinonimo in texto_norm:
                return sinonimo, grupo_sinonimos[0].upper()

    # Nivel 2: búsqueda semántica con spaCy
    doc = nlp(texto_norm)
    lemas_texto = [token.lemma_ for token in doc if not token.is_stop and len(token.text) > 2]

    for grupo_sinonimos in PROTOCOLOS_MAESTROS.keys():
        for sinonimo in grupo_sinonimos:
            doc_sin = nlp(sinonimo)
            lemas_sin = [token.lemma_ for token in doc_sin]
            if any(lema in lemas_texto for lema in lemas_sin):
                return sinonimo, grupo_sinonimos[0].upper()

    # Nivel 3: fuzzy matching (nuevo)
    # Detecta palabras mal pronunciadas o transcritas por Whisper
    # Ejemplo: "cabesa" → "cabeza", "superio" → "superior"
    from rapidfuzz import fuzz
    palabras_texto = texto_norm.split()
    mejor_sintoma = None
    mejor_score = 0
    mejor_grupo = None

    for grupo_sinonimos in PROTOCOLOS_MAESTROS.keys():
        for sinonimo in grupo_sinonimos:
            for palabra in palabras_texto:
                # Solo comparamos palabras de longitud similar para evitar falsos positivos
                if abs(len(palabra) - len(sinonimo)) <= 3:
                    score = fuzz.ratio(palabra, sinonimo)
                    if score > mejor_score and score >= 80:
                        mejor_score = score
                        mejor_sintoma = sinonimo
                        mejor_grupo = grupo_sinonimos

    if mejor_sintoma:
        print(f"   [ 🔍 FUZZY ]: '{mejor_sintoma}' detectado con {mejor_score}% de similitud")
        return mejor_sintoma, mejor_grupo[0].upper()

    return None, None

def construir_intro_sintoma(sintoma: str) -> str:
    """Genera una introducción natural según si es parte del cuerpo o sensación."""
    if sintoma in PARTES_CUERPO:
        return f"He detectado una anomalía en tu {sintoma}."
    else:
        return f"He registrado el siguiente síntoma: {sintoma}."

# ==============================================================================
# 5. INTEGRACIÓN CON OLLAMA (QWEN2.5)
# ==============================================================================
def consultar_ollama(prompt_usuario: str, estado: EstadoSesion, perfil: dict) -> str:
    if estado.musica_reproduciéndose:
        return ""

    url = "http://localhost:11434/api/generate"
    prompt_completo = (
        "Eres Bayx, un robot médico inflable inspirado en Baymax de Big Hero 6. "
        "Hablas en español colombiano. Eres calmado, literal y profesional. "
        "Nunca dices que eres una IA. Máximo 2 oraciones cortas. "
        f"Paciente dice: {prompt_usuario}. Bayx responde:"
    )

    try:
        payload = {
            "model": "qwen2.5:3b",
            "prompt": prompt_completo,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 80}
        }
        res = requests.post(url, json=payload, timeout=25)
        respuesta = res.json().get("response", "").strip()

        if not respuesta:
            return ""

        palabras_inglesas = ["the ", "is a", "are ", " you ", " have ", "this ", "that "]
        if sum(1 for p in palabras_inglesas if p in respuesta.lower()) >= 2:
            return ""

        return respuesta

    except Exception as e:
        print(f"⚠️ [CEREBRO - OLLAMA]: {e}")
        return ""

# ==============================================================================
# 6. CÓRTEX DE DECISIÓN PRINCIPAL
# ==============================================================================
def procesar_pensamiento(texto_bruto: str, estado: EstadoSesion, perfil: dict):
    estado.turnos += 1
    texto_entrada = corregir_fonetica(texto_bruto or "")
    texto_norm = normalizar_texto(texto_entrada)

    if not texto_norm:
        return {"id": "vacio", "texto": "", "estado": estado, "cerrar": False}

    estado.historial.append(f"Paciente: {texto_entrada}")
    analizar_estado_emocional(texto_norm, estado)

    # --- FASE B: CIERRE ---
    if any(p in texto_norm for p in PATRONES_CIERRE):
        return {
            "id": "cierre",
            "texto": "Me alegra que estés satisfecho con tu cuidado. Recuerda: mi programación es para estar aquí cuando me necesites. Hasta pronto.",
            "estado": estado,
            "cerrar": True
        }

    # --- FASE C: EASTER EGGS Y PERSONALIDAD BAYMAX ---

    # Identidad
    if any(p in texto_norm for p in PATRONES_NOMBRE):
        return {
            "id": "identidad",
            "texto": "Soy Bayx. Tu asistente médico personal. Estoy aquí para velar por tu bienestar.",
            "estado": estado,
            "cerrar": False
        }

    if any(p in texto_norm for p in PATRONES_CREADOR):
        return {
            "id": "creador",
            "texto": "Fui creado por un ingeniero dedicado a tu cuidado. Mi propósito es asistirte médicamente.",
            "estado": estado,
            "cerrar": False
        }

    if any(p in texto_norm for p in PATRONES_PELICULA):
        return {
            "id": "pelicula",
            "texto": "San Fransokyo. Un lugar donde la tecnología y el cuidado humano se unen. Me identifico con ese concepto.",
            "estado": estado,
            "cerrar": False
        }

    # Gato / Hairy Baby
    if any(p in texto_norm for p in PATRONES_MASCOTA):
        return {
            "id": "bebe_peludo",
            "texto": "Bebé peludo... Bebé peludo. El ronroneo de un gato tiene frecuencias que reducen el estrés humano significativamente.",
            "estado": estado,
            "cerrar": False
        }

    # Chocar los puños
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
            "texto": "Entendido. Procesando nuevo protocolo de saludo social... ¡Balalala!",
            "estado": estado,
            "cerrar": False
        }

    # Abrazo
    if any(p in texto_norm for p in PATRONES_ABRAZO):
        estado.contador_abrazos += 1
        frases_abrazo = [
            "Iniciando protocolo de soporte físico. Los abrazos liberan oxitocina y reducen la ansiedad.",
            "Protocolo de abrazo activado. El contacto físico positivo reduce el cortisol en un 30%.",
            "Abrazo en curso. Recuerda que el contacto humano es tan importante como la medicina."
        ]
        return {
            "id": "abrazo",
            "texto": random.choice(frases_abrazo),
            "estado": estado,
            "cerrar": False
        }

    # Batería baja
    if "bateria baja" in texto_norm or "descargando" in texto_norm:
        return {
            "id": "bateria",
            "texto": "Tengo... batería baja. Necesito... mi estación de carga. Estamos en un mundo... de maravillas.",
            "estado": estado,
            "cerrar": False
        }

    # --- FASE D: MUSICOTERAPIA ---
    if any(p in texto_norm for p in PATRONES_MUSICA_RELAJAR):
        return {
            "id": "reproducir_musica",
            "tipo_musica": "relajar",
            "texto": "He detectado tensión en tus niveles de cortisol. Iniciando protocolo de relajación musical. Respira a mi ritmo.",
            "estado": estado,
            "cerrar": False
        }

    if any(p in texto_norm for p in PATRONES_MUSICA_ANIMO):
        return {
            "id": "reproducir_musica",
            "tipo_musica": "animo",
            "texto": "Iniciando terapia musical estimulante. Esto elevará tus niveles de dopamina y serotonina.",
            "estado": estado,
            "cerrar": False
        }

    if estado.musica_reproduciéndose and any(p in texto_norm for p in PATRONES_STOP_MUSICA):
        return {
            "id": "detener_musica",
            "texto": "Tratamiento de audio detenido. ¿En qué más puedo ayudarte?",
            "estado": estado,
            "cerrar": False
        }

    # --- FASE E: SEGUIMIENTO Y ESCALA DE DOLOR ---
    if estado.esperando_seguimiento:
        # Si menciona un síntoma nuevo, reseteamos
        nuevo_sintoma, nueva_categoria = identificar_patologia(texto_norm)
        if nuevo_sintoma and nuevo_sintoma != estado.sintoma_actual:
            estado.esperando_seguimiento = False
            estado.esperando_escala = False
            estado.indice_pregunta = 0
            # Caemos a la FASE F para procesar el nuevo síntoma

        else:
            respuesta_detalle = obtener_respuesta_detalle(estado.sintoma_actual, texto_norm)
            siguiente_pregunta = obtener_pregunta_seguimiento(estado.sintoma_actual, estado.indice_pregunta)

            if respuesta_detalle:
                estado.indice_pregunta += 1
                proxima = obtener_pregunta_seguimiento(estado.sintoma_actual, estado.indice_pregunta)
                if proxima:
                    return {
                        "id": "seguimiento",
                        "texto": f"{respuesta_detalle} También necesito saber: {proxima}",
                        "estado": estado,
                        "cerrar": False
                    }
                else:
                    estado.esperando_seguimiento = False
                    estado.esperando_escala = True
                    return {
                        "id": "seguimiento_final",
                        "texto": f"{respuesta_detalle} En una escala del uno al diez, ¿cómo calificarías tu malestar?",
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
                    "texto": "En una escala del uno al diez, ¿cómo calificarías tu malestar?",
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
                    "texto": "Escaneo completado. No se detectó lesión significativa. Es posible que sea un malestar pasajero propio de tu edad y cambios hormonales.",
                    "estado": estado,
                    "cerrar": False
                }

            consejo = generar_respuesta_medica(estado.sintoma_actual)
            sintoma_registrado = estado.sintoma_actual

            # Reseteo completo del estado médico
            estado.sintoma_actual = "NINGUNO"
            estado.categoria_actual = "GENERAL"
            estado.esperando_escala = False
            estado.esperando_seguimiento = False
            estado.indice_pregunta = 0

            return {
                "id": "consejo_medico",
                "texto": f"He registrado un nivel de malestar de {nivel} sobre diez en tu {sintoma_registrado}. {consejo} ¿Tienes algún otro síntoma que reportar?",
                "estado": estado,
                "cerrar": False
            }

        return {
            "id": "re_escala",
            "texto": "No logré capturar el valor. Por favor indica un número del uno al diez.",
            "estado": estado,
            "cerrar": False
        }

    # --- FASE F: DETECCIÓN DE NUEVAS ANOMALÍAS ---
    sintoma, categoria = identificar_patologia(texto_norm)
    if sintoma:
        estado.sintoma_actual = sintoma
        estado.categoria_actual = categoria
        estado.esperando_seguimiento = True
        estado.indice_pregunta = 0

        perfil["ultimo_sintoma"] = sintoma
        guardar_perfil(perfil)

        intro = construir_intro_sintoma(sintoma)
        primera_pregunta = obtener_pregunta_seguimiento(sintoma, 0)

        if primera_pregunta:
            estado.indice_pregunta = 1
            return {
                "id": "pedir_seguimiento",
                "texto": f"{intro} {primera_pregunta}",
                "estado": estado,
                "cerrar": False
            }
        else:
            estado.esperando_seguimiento = False
            estado.esperando_escala = True
            return {
                "id": "pedir_escala",
                "texto": f"{intro} En una escala del uno al diez, ¿cómo calificarías tu malestar?",
                "estado": estado,
                "cerrar": False
            }

    # --- FASE G: CONVERSACIÓN GENERAL ---
    actualizar_historial_temas(perfil, texto_norm)

    respuestas_generales = {
        ("como estas", "como te sientes", "que tal", "como vas"): [
            "Estoy funcionando al 100% de capacidad. Gracias por preguntar. ¿Cómo estás tú?",
            "Todos mis sistemas operan con normalidad. Mi prioridad eres tú. ¿Cómo te encuentras?",
            "Mis diagnósticos internos muestran funcionamiento óptimo. ¿Y tú cómo te sientes?"
        ],
        ("cuentame algo", "dime algo", "que sabes", "sabias que", "cuéntame"): [
            "El corazón humano late aproximadamente 100.000 veces al día. Cuidarlo es mi misión principal.",
            "Dormir menos de 7 horas reduce tu sistema inmune en un 40%. ¿Estás durmiendo bien?",
            "El cerebro humano consume el 20% de toda la energía del cuerpo, aunque solo pesa 1.4 kilos.",
            "Reír 15 minutos al día tiene el mismo efecto cardiovascular que 30 minutos de caminata.",
            "Beber agua antes de cada comida puede mejorar tu digestión hasta en un 30%."
        ],
        ("gracias", "muchas gracias", "te lo agradezco", "te agradezco"): [
            "No hay de qué. Mi función es tu bienestar.",
            "Es un placer ayudarte. Para eso estoy programado.",
            "No es necesario agradecerme. Es mi propósito."
        ],
        ("que puedes hacer", "que haces", "para que sirves", "que sabes hacer"): [
            "Puedo diagnosticar síntomas, aplicar protocolos médicos, reproducir musicoterapia y monitorear tu estado emocional.",
            "Estoy diseñado para tu cuidado médico personal. Dime dónde te duele y activo mis protocolos de diagnóstico.",
            "Mis funciones incluyen: evaluación de síntomas, terapia musical, soporte emocional y generación de reportes clínicos."
        ],
        ("hola", "buenos dias", "buenas tardes", "buenas noches", "hey", "ey"): [
            "Hola. Estoy listo para atenderte. ¿Cómo te sientes hoy?",
            "Saludos. Mis sensores están en línea. ¿Tienes algún malestar que reportar?",
            "Hola. Es un gusto verte. ¿En qué puedo ayudarte hoy?"
        ],
        ("aburrido", "aburro", "nada que hacer", "estoy aburrido"): [
            "El aburrimiento puede ser una señal de que tu cerebro necesita estimulación. ¿Quieres que inicie la musicoterapia?",
            "Conozco un buen protocolo anti-aburrimiento. Se llama musicoterapia. ¿Lo iniciamos?",
            "El cerebro humano necesita entre 4 y 6 horas de actividad estimulante al día. ¿Qué tal si ponemos música?"
        ],
        ("me siento bien", "estoy bien", "me siento excelente", "estoy excelente"): [
            "Me alegra escuchar eso. Mantener un estado positivo fortalece el sistema inmune.",
            "Excelente. Mis sensores registran estabilidad en tu estado general. Sigue así.",
            "Eso es lo que quiero escuchar. ¿Hay algo en lo que pueda ayudarte hoy?"
        ],
        ("no me siento bien", "me siento mal", "estoy mal"): [
            "Entiendo. ¿Puedes describirme dónde sientes el malestar específicamente?",
            "Lo siento. ¿Puedes decirme qué parte de tu cuerpo está afectada para activar el protocolo correcto?",
            "Mis sensores detectan que algo no está bien. ¿Dónde sientes el malestar?"
        ]
    }

    for patrones, respuestas in respuestas_generales.items():
        if any(p in texto_norm for p in patrones):
            return {
                "id": "charla",
                "texto": random.choice(respuestas),
                "estado": estado,
                "cerrar": False
            }

    # Fallback: Ollama
    respuesta_ia = consultar_ollama(texto_entrada, estado, perfil)
    if not respuesta_ia:
        respuesta_ia = random.choice([
            "No logré procesar esa consulta completamente. ¿Tienes algún síntoma que reportar?",
            "Mis procesadores no encontraron una respuesta adecuada. ¿Puedes reformular tu pregunta?",
            "No estoy seguro de haber entendido. ¿Puedes contarme cómo te sientes físicamente?"
        ])

    return {
        "id": "charla",
        "texto": respuesta_ia,
        "estado": estado,
        "cerrar": False
    }

# ==============================================================================
# FIN DEL CÓRTEX CEREBRAL V21.0 - BAYMAX EDITION
# ==============================================================================