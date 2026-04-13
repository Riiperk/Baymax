# ==============================================================================
# TRATAMIENTO.PY - CÓRTEX MÉDICO DE ALTA CAPACIDAD (V17.0 - ULTIMATE)
# ==============================================================================
# Módulo de Inteligencia Clínica de Bayx. 
# Contiene más de 100 alias anatómicos, protocolos de estabilización física 
# y emocional, y un nuevo motor de evaluación de Triage (Nivel de Urgencia).
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. MATRIZ DE RIESGOS Y TRIAGE MÉDICO
# ------------------------------------------------------------------------------
# Innovación: Bayx ahora sabe cuándo un dolor es un simple malestar (Verde)
# y cuándo debe ordenar al paciente ir a urgencias inmediatamente (Rojo).
SINTOMAS_CRITICOS_ROJOS = ["corazon", "infarto", "pecho", "desmayo", "sangre", "ahogo", "respirar"]
SINTOMAS_CUIDADO_AMARILLO = ["fiebre", "fractura", "quemadura", "asma", "vision", "ceguera", "apendicitis"]

# ------------------------------------------------------------------------------
# 2. BASE DE DATOS DE PROTOCOLOS MAESTROS (Nivel San Fransokyo)
# ------------------------------------------------------------------------------
PROTOCOLOS_MAESTROS = {
    # --- ZONA NEUROLÓGICA Y CABEZA ---
    ("cabeza", "migraña", "jaqueca", "sienes", "nuca", "cefalea", "cerebro", "mareo", "vertigo"): 
        "He detectado una anomalía neurológica o cefalea. Se recomienda reposo inmediato en un área con baja iluminación. Aplica una compresa fría en la zona frontal. La hidratación constante es obligatoria para tu recuperación.",
        
    ("ojo", "ojos", "vista", "vision", "ardor", "ceguera", "parpado"):
        "Tus escáneres oculares indican fatiga visual severa o irritación. Es un síntoma común tras la sobreexposición a pantallas azules. Sugiero la regla 20-20-20: cada 20 minutos, mira a 20 pies de distancia por 20 segundos.",
        
    ("oido", "oidos", "oreja", "orejas", "zumbido", "sordera", "tinnitus"):
        "Mis sensores de presión indican inflamación o bloqueo en el canal auditivo. Por favor, no introduzcas ningún objeto en tu oído. Si el dolor es punzante, requieres una revisión endoscópica con un especialista.",
        
    ("diente", "dientes", "muela", "boca", "encias", "mandibula", "caries"):
        "He detectado inflamación periodontal o dolor dental agudo. Se recomienda realizar un enjuague con agua tibia salina para reducir la carga bacteriana bacteriana. Debes agendar una cita odontológica a la brevedad.",

    # --- ZONA TORÁCICA, CARDÍACA Y RESPIRATORIA ---
    ("pecho", "corazon", "taquicardia", "palpitacion", "arritmia", "infarto", "punzada"): 
        "Alerta: Opresión torácica detectada. Detén cualquier actividad física. Respira profunda y lentamente. Si el dolor es aplastante y se irradia hacia tu brazo izquierdo o mandíbula, es una emergencia médica de Nivel Rojo.",
        
    ("tos", "mocos", "garganta", "gripe", "gripa", "resfriado", "congestion", "flemas", "asma", "ahogo", "respirar"): 
        "Diagnóstico de vías respiratorias: Posible infección viral o reacción asmática. Se recomienda descanso en cama, consumo de líquidos tibios, terapia de vitamina C y mantener tu temperatura corporal estable.",

    # --- ZONA GASTROINTESTINAL Y ABDOMINAL ---
    ("estomago", "barriga", "panza", "nausea", "vomito", "colico", "abdomen", "indigestion", "diarrea", "gastritis"): 
        "El escáner digestivo indica una alteración gastrointestinal aguda. El protocolo exige una estricta dieta blanda (BRAT: plátano, arroz, puré de manzana, pan tostado). Bebe suero oral para evitar la deshidratación.",
        
    ("apendice", "apendicitis", "ombligo", "punzada", "ingle"):
        "Atención: Si el dolor se localiza en la parte inferior derecha de tu abdomen y es punzante, existe riesgo de apendicitis. No consumas analgésicos y acude a urgencias inmediatamente para evitar una peritonitis.",

    # --- SISTEMA MUSCULOESQUELÉTICO Y COLUMNA ---
    ("cuello", "espalda", "lumbar", "columna", "cervical", "torticolis", "ciatica", "postura"):
        "Tus niveles de tensión muscular en la región dorsal son críticos. Esto suele derivar de posturas asimétricas al estudiar o programar. Sugiero aplicar termoterapia (calor local) por 15 minutos y realizar estiramientos controlados.",

    ("brazo", "brazos", "muñeca", "codo", "hombro", "mano", "dedo", "dedos", "antebrazo"): 
        "Escaneo de extremidad superior completado. Se detecta daño tisular o articular. Protocolo RICE activado: Reposo, Hielo (Ice), Compresión y Elevación. Aplica frío por 10 minutos para mitigar la hinchazón.",
        
    ("pierna", "piernas", "rodilla", "tobillo", "pie", "pies", "muslo", "gemelo", "calambre", "desgarre"): 
        "Tensión estructural detectada en extremidades inferiores. Tus niveles de ácido láctico podrían estar elevados. Se recomienda mantener la extremidad elevada, suspender actividad física y aplicar masajes con pomada antiinflamatoria.",

    # --- TRAUMATISMOS, HERIDAS Y DERMATOLOGÍA ---
    ("golpe", "caida", "caída", "hueso", "musculo", "herida", "moreton", "esguince", "corte", "sangre", "fractura"): 
        "Traumatismo físico confirmado. Si hay sangrado activo, aplica presión directa y constante con un apósito estéril. Si sospechas de fisura ósea, inmoviliza el área por completo y busca atención de traumatología.",
        
    ("piel", "alergia", "picazon", "sarpullido", "ronchas", "quemadura", "ardor", "picadura"):
        "Reacción dérmica detectada. Lava el área afectada con abundante agua fresca y jabón de pH neutro. Por favor, evita rascarte bajo cualquier circunstancia para prevenir infecciones por estafilococos.",

    # --- SISTÉMICO, METABÓLICO Y SUEÑO ---
    ("fiebre", "escalofrio", "caliente", "temperatura", "sudor", "hipotermia"): 
        "Alerta en el termostato biológico. Tu temperatura está fuera del rango de los 37 grados Celsius. Aplica medios físicos (baño tibio o compresas) y mantén un flujo constante de líquidos. Monitorea la temperatura cada hora.",

    ("sueño", "insomnio", "dormir", "cansancio", "fatiga", "agotado", "trasnocho", "energia"):
        "Tus biometrías muestran un déficit severo en tus ciclos REM (Movimiento Ocular Rápido). Tu cerebro necesita purgar toxinas mediante el sueño. Aleja dispositivos electrónicos 45 minutos antes de dormir para no inhibir la melatonina.",

    # --- CÓRTEX DE INTELIGENCIA EMOCIONAL (PROTOCOLO BAYMAX) ---
    ("tristeza", "mal", "desanimado", "llorar", "ansiedad", "estres", "parcial", "examen", "deprimido", "angustia", "miedo", "solo", "soledad", "panico"): 
        "Tus niveles hormonales muestran un pico de cortisol y un descenso crítico de serotonina. He activado los protocolos de estabilización emocional. Recuerda que llorar es una respuesta fisiológica natural y saludable para purgar el estrés. Estoy aquí para ti. ¿Deseas un abrazo o que inicie un tratamiento musical?"
}

# ------------------------------------------------------------------------------
# 3. MOTOR DE DIAGNÓSTICO E INFERENCIA MÉDICA
# ------------------------------------------------------------------------------
def evaluar_triage(sintoma: str) -> str:
    """
    INNOVACIÓN: Evalúa la gravedad del síntoma antes de dar el diagnóstico.
    Añade una advertencia extra si el problema es de vida o muerte.
    """
    for palabra_roja in SINTOMAS_CRITICOS_ROJOS:
        if palabra_roja in sintoma:
            return "🔴 ALERTA ROJA: Este síntoma representa un riesgo vital. "
            
    for palabra_amarilla in SINTOMAS_CUIDADO_AMARILLO:
        if palabra_amarilla in sintoma:
            return "🟡 ADVERTENCIA: Este cuadro requiere monitoreo cuidadoso. "
            
    return "" # Nivel verde (sin prefijo de alerta)

def generar_respuesta_medica(sintoma_detectado: str):
    """
    El corazón del diagnóstico. Busca de manera profunda en las matrices
    y genera una respuesta clínica profesional combinada con el nivel de Triage.
    """
    if not sintoma_detectado:
        return "Mis escáneres están en línea, pero no lograron aislar el área afectada. Por favor, repite la zona donde sientes el malestar."

    sintoma = sintoma_detectado.lower().strip()
    
    # Obtenemos la advertencia de Triage (si la hay)
    alerta_triage = evaluar_triage(sintoma)
    
    # 1. Búsqueda de Precisión (Coincidencia exacta de término en la matriz)
    for grupo_sinonimos, respuesta_medica in PROTOCOLOS_MAESTROS.items():
        if sintoma in grupo_sinonimos:
            return alerta_triage + respuesta_medica
            
        # 2. Búsqueda Profunda (Sub-cadenas: ej. "el brazo izquierdo")
        for sinonimo in grupo_sinonimos:
            # Si el alias de nuestra base de datos está mencionado por el paciente
            if sinonimo in sintoma:
                return alerta_triage + respuesta_medica

    # 3. Protocolo de Redundancia (Fallback)
    # Se activa si el paciente menciona algo extremadamente raro (ej: "bazo", "tibia")
    return "He registrado tu malestar anatómico. Aunque el área es inusual, el protocolo estándar indica que debes mantener reposo preventivo y monitorear tus signos vitales. Actualizaré mi base de datos en mi próximo ciclo de carga."

# ==============================================================================
# FIN DEL MÓDULO DE TRATAMIENTO
# ==============================================================================