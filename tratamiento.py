# ==============================================================================
# TRATAMIENTO.PY - CÓRTEX MÉDICO (V20.0 - CON PREGUNTAS DE SEGUIMIENTO)
# ==============================================================================

SINTOMAS_CRITICOS_ROJOS = [
    "corazon", "infarto", "pecho", "desmayo", "sangre", "ahogo",
    "respirar", "convulsion", "paralisis", "derrame"
]
SINTOMAS_CUIDADO_AMARILLO = [
    "fiebre", "fractura", "quemadura", "asma", "vision",
    "ceguera", "apendicitis", "vomito", "diarrea"
]

PROTOCOLOS_MAESTROS = {
    ("cabeza", "migraña", "jaqueca", "sienes", "nuca", "cefalea", "cerebro", "mareo", "vertigo"): {
        "preguntas": [
            "¿El dolor es pulsante como latidos, o es una presión constante?",
            "¿Tienes sensibilidad a la luz o al ruido?"
        ],
        "respuesta_base": "He detectado una anomalía neurológica. Reposo inmediato en área oscura, compresa fría en la frente e hidratación constante.",
        "respuestas_detalle": {
            "pulsante": "Los síntomas indican una migraña vascular. Evita pantallas y busca un ambiente oscuro y silencioso.",
            "presion": "Parece una cefalea tensional. Aplica calor en el cuello y realiza respiraciones profundas.",
            "luz": "La fotosensibilidad confirma migraña. Necesitas oscuridad total y reposo absoluto.",
            "ruido": "La sensibilidad al ruido confirma migraña. Busca un ambiente silencioso y oscuro."
        }
    },
    ("ojo", "ojos", "vista", "vision", "ardor ocular", "ceguera", "parpado"): {
        "preguntas": [
            "¿El malestar es en ambos ojos o solo en uno?",
            "¿Tienes visión borrosa o solo irritación?"
        ],
        "respuesta_base": "Tus sensores oculares indican fatiga o irritación. Aplica la regla 20-20-20 y evita pantallas.",
        "respuestas_detalle": {
            "borrosa": "La visión borrosa puede indicar fatiga severa o tensión ocular. Si persiste más de 24 horas consulta un especialista.",
            "irritacion": "Irritación ocular detectada. Lava con agua limpia y evita frotarte los ojos.",
            "uno": "El malestar en un solo ojo puede indicar un cuerpo extraño o conjuntivitis. No lo frotes.",
            "ambos": "Malestar en ambos ojos indica fatiga visual severa. Descansa de pantallas por al menos 2 horas."
        }
    },
    ("oido", "oidos", "oreja", "orejas", "zumbido", "sordera", "tinnitus"): {
        "preguntas": [
            "¿Escuchas un zumbido constante o sientes el oído tapado?",
            "¿Tienes dolor punzante dentro del oído?"
        ],
        "respuesta_base": "Mis sensores detectan inflamación o bloqueo auditivo. No introduzcas objetos en el oído.",
        "respuestas_detalle": {
            "zumbido": "El tinnitus puede ser por exposición a ruidos fuertes. Reposo auditivo absoluto por 24 horas.",
            "tapado": "Bloqueo del canal auditivo detectado. Puede ser cerumen acumulado. Un médico debe revisarlo.",
            "dolor": "Dolor punzante indica posible otitis media. Requiere atención médica y posiblemente antibióticos."
        }
    },
    ("diente", "dientes", "muela", "boca", "encias", "mandibula", "caries"): {
        "preguntas": [
            "¿El dolor es constante o solo al morder o tomar algo frío?",
            "¿Tienes la encía inflamada o con sangrado?"
        ],
        "respuesta_base": "He detectado inflamación periodontal. Enjuague con agua tibia salina y agenda cita odontológica.",
        "respuestas_detalle": {
            "frio": "Sensibilidad al frío indica dentina expuesta o caries profunda. Evita alimentos fríos y ve al dentista.",
            "constante": "Dolor constante puede ser una infección dental o absceso. Requiere atención odontológica urgente.",
            "sangrado": "Sangrado de encías indica gingivitis. Mejora el cepillado y usa hilo dental diariamente."
        }
    },
    ("pecho", "corazon", "taquicardia", "palpitacion", "arritmia", "infarto"): {
        "preguntas": [
            "¿El malestar se irradia hacia el brazo izquierdo o la mandíbula?",
            "¿Tienes dificultad para respirar junto con el malestar?"
        ],
        "respuesta_base": "Alerta torácica. Detén toda actividad física y respira lento y profundo.",
        "respuestas_detalle": {
            "brazo": "ALERTA ROJA. Esto puede ser un infarto. Llama a emergencias inmediatamente y no te muevas.",
            "mandibula": "ALERTA ROJA. Dolor irradiado a mandíbula es señal de emergencia cardíaca. Llama ya.",
            "respirar": "Dificultad respiratoria con malestar pectoral es una emergencia. Busca atención médica ahora.",
            "no": "Sin irradiación. Puede ser ansiedad o tensión muscular. Respira profundo y descansa."
        }
    },
    ("tos", "mocos", "garganta", "gripe", "gripa", "resfriado", "congestion", "flemas", "asma", "ahogo", "cuerpo cortado", "cuerpo partido", "destemplado", "escalofrios", "tiritera"): {
        "preguntas": [
            "¿Tienes fiebre junto con el malestar?",
            "¿Tienes flemas de color amarillo o verde?"
        ],
        "respuesta_base": "Diagnóstico respiratorio: posible infección viral. Reposo, líquidos tibios y vitamina C.",
        "respuestas_detalle": {
            "fiebre": "Malestar con fiebre puede indicar influenza o bronquitis. Reposo absoluto y monitorea la temperatura.",
            "amarillo": "Flemas amarillas o verdes indican infección bacteriana. Podrías necesitar antibióticos, consulta a un médico.",
            "verde": "Flemas verdes indican infección bacteriana activa. Consulta a un médico pronto.",
            "no": "Sin fiebre ni flemas, puede ser un resfriado común. Reposo e hidratación son suficientes."
        }
    },
    ("estomago", "barriga", "panza", "nausea", "nauseas", "vomito", "colico", "abdomen", "indigestion", "diarrea", "gastritis", "revuelve", "revoltijo", "empacho"): {
        "preguntas": [
            "¿Sientes el malestar más en la parte superior o inferior del abdomen?",
            "¿El malestar aparece después de comer o es constante?"
        ],
        "respuesta_base": "Alteración gastrointestinal detectada. Dieta blanda y suero oral para evitar deshidratación.",
        "respuestas_detalle": {
            "superior": "Malestar en abdomen superior puede ser gastritis o reflujo. Evita comidas grasosas y ácidas.",
            "superio": "Malestar en abdomen superior puede ser gastritis o reflujo. Evita comidas grasosas y ácidas.",
            "arriba": "Malestar en abdomen superior puede ser gastritis o reflujo. Evita comidas grasosas y ácidas.",
            "inferior": "Malestar en abdomen inferior puede ser colon irritable o apendicitis. Si es muy intenso ve a urgencias.",
            "abajo": "Malestar en abdomen inferior puede ser colon irritable o apendicitis. Si es muy intenso ve a urgencias.",
            "despues de comer": "Malestar post-comida indica posible gastritis o intolerancia alimentaria. Evita comidas pesadas.",
            "constante": "Malestar constante en el abdomen requiere evaluación médica para descartar causas graves.",
            "vomito": "Vómitos activos detectados. Hidratación con sorbos pequeños frecuentes es prioritaria.",
            "nausea": "Náuseas detectadas. Evita alimentos sólidos por 2 horas y toma sorbos pequeños de agua fría."
        }
    },
    ("apendice", "apendicitis", "ombligo", "ingle"): {
        "preguntas": [
            "¿El malestar es constante en la parte inferior derecha del abdomen?",
            "¿Tienes fiebre junto con el malestar?"
        ],
        "respuesta_base": "Posible apendicitis. No tomes analgésicos y acude a urgencias.",
        "respuestas_detalle": {
            "derecha": "ALERTA AMARILLA. Malestar inferior derecho constante es señal clásica de apendicitis. Ve a urgencias ya.",
            "fiebre": "Fiebre con malestar abdominal inferior es una combinación de alto riesgo. Atención médica inmediata.",
            "si": "ALERTA AMARILLA. Estos síntomas requieren evaluación médica urgente. Ve a urgencias ahora."
        }
    },
    ("cuello", "espalda", "lumbar", "columna", "cervical", "torticolis", "ciatica", "postura"): {
        "preguntas": [
            "¿El malestar baja hacia las piernas o se queda en la espalda?",
            "¿Empeoró después de levantar algo pesado o de estar sentado mucho tiempo?"
        ],
        "respuesta_base": "Tensión muscular dorsal crítica. Termoterapia 15 minutos y estiramientos controlados.",
        "respuestas_detalle": {
            "piernas": "Malestar que baja a piernas indica compresión del nervio ciático. Reposo y antiinflamatorio.",
            "sentado": "Malestar por postura prolongada. Cada 30 minutos levántate y estira la espalda.",
            "pesado": "Posible distensión muscular por esfuerzo. Hielo las primeras 24 horas, luego calor.",
            "espalda": "Malestar localizado en espalda. Aplica calor local y evita cargar peso por 48 horas."
        }
    },
    ("brazo", "brazos", "muñeca", "codo", "hombro", "mano", "dedo", "dedos", "antebrazo"): {
        "preguntas": [
            "¿Puedes mover el brazo con normalidad o el movimiento duele?",
            "¿Hay inflamación visible o moretón en la zona?"
        ],
        "respuesta_base": "Daño tisular o articular detectado. Protocolo RICE: Reposo, Hielo, Compresión y Elevación.",
        "respuestas_detalle": {
            "no puedo": "Limitación de movimiento severa. Posible fractura o luxación. Inmoviliza y ve a urgencias.",
            "duele": "Movimiento doloroso indica posible esguince o desgarre. Reposo e hielo por 20 minutos.",
            "inflamacion": "Inflamación visible confirma traumatismo. Hielo 10 minutos cada hora las primeras 24 horas.",
            "moreton": "Hematoma detectado. Eleva el brazo por encima del corazón para reducir la hinchazón.",
            "no": "Sin inflamación aparente. Reposo preventivo y monitorea si aparece hinchazón."
        }
    },
    ("pierna", "piernas", "rodilla", "tobillo", "pie", "pies", "muslo", "gemelo", "calambre", "desgarre"): {
        "preguntas": [
            "¿Puedes apoyar el peso del cuerpo en la pierna afectada?",
            "¿El malestar fue súbito como un chasquido o apareció gradualmente?"
        ],
        "respuesta_base": "Tensión en extremidades inferiores. Eleva la pierna y suspende actividad física.",
        "respuestas_detalle": {
            "no puedo": "Imposibilidad de apoyar peso puede indicar fractura. Inmoviliza y acude a urgencias.",
            "chasquido": "Sonido al lesionarse indica posible rotura de ligamento. Requiere evaluación médica urgente.",
            "gradual": "Malestar gradual indica sobrecarga muscular. Reposo 48 horas y antiinflamatorio tópico.",
            "si": "Puedes apoyar peso, lo cual es buena señal. Reposo relativo e hielo en la zona afectada."
        }
    },
    ("golpe", "caida", "caída", "hueso", "herida", "moreton", "esguince", "corte", "fractura"): {
        "preguntas": [
            "¿Hay herida abierta con sangrado activo?",
            "¿Sientes entumecimiento u hormigueo en la zona?"
        ],
        "respuesta_base": "Traumatismo físico confirmado. Si hay sangrado aplica presión constante con apósito limpio.",
        "respuestas_detalle": {
            "sangrado": "Sangrado activo: presión directa constante por al menos 10 minutos sin levantar el apósito.",
            "hormigueo": "Hormigueo post-traumático puede indicar daño nervioso. Requiere evaluación médica.",
            "entumecimiento": "Entumecimiento indica posible compresión nerviosa. No muevas la zona y busca atención médica.",
            "no": "Sin complicaciones aparentes. Protocolo RICE y monitoreo de la zona durante 24 horas."
        }
    },
    ("piel", "alergia", "picazon", "sarpullido", "ronchas", "quemadura", "ardor", "picadura"): {
        "preguntas": [
            "¿La reacción apareció después de comer algo o contacto con alguna sustancia?",
            "¿Las ronchas se están expandiendo rápidamente?"
        ],
        "respuesta_base": "Reacción dérmica detectada. Lava con agua y jabón de pH neutro. No te rasques.",
        "respuestas_detalle": {
            "comida": "Posible alergia alimentaria. Evita ese alimento y consulta a un alergólogo.",
            "expandiendo": "ALERTA: Reacción que se expande puede ser anafilaxia. Busca atención médica inmediata.",
            "picadura": "Picadura de insecto: lava la zona, aplica hielo y antihistamínico si tienes.",
            "sustancia": "Dermatitis de contacto detectada. Lava la zona y evita el contacto con esa sustancia.",
            "no": "Sin causa aparente identificada. Aplica crema calmante y evita rascarte."
        }
    },
    ("fiebre", "escalofrio", "caliente", "temperatura", "sudor", "hipotermia"): {
        "preguntas": [
            "¿Cuántos grados tienes de temperatura?",
            "¿La fiebre lleva más de 24 horas?"
        ],
        "respuesta_base": "Temperatura fuera del rango normal. Baño tibio, compresas y líquidos constantes.",
        "respuestas_detalle": {
            "38": "Fiebre moderada. Reposo, líquidos y monitoreo cada 2 horas.",
            "39": "Fiebre alta detectada. Si supera 39.5 grados requiere atención médica urgente.",
            "40": "ALERTA ROJA. Temperatura crítica. Ve a urgencias inmediatamente.",
            "24 horas": "Fiebre persistente más de 24 horas requiere evaluación médica para descartar infección grave.",
            "si": "Fiebre prolongada requiere atención médica. No te automediques sin consultar a un doctor.",
            "no": "Fiebre reciente. Monitorea la temperatura cada 2 horas y mantente hidratado."
        }
    },
    ("sueño", "insomnio", "dormir", "cansancio", "fatiga", "agotado", "trasnocho", "energia"): {
        "preguntas": [
            "¿Llevas más de 2 días sin dormir bien?",
            "¿El cansancio es físico, mental o los dos?"
        ],
        "respuesta_base": "Déficit severo en ciclos REM detectado. Aleja dispositivos 45 minutos antes de dormir.",
        "respuestas_detalle": {
            "dos dias": "Insomnio crónico detectado. Establece un horario fijo de sueño y evita cafeína después del mediodía.",
            "mental": "Fatiga mental indica sobrecarga cognitiva. Técnicas de meditación y pausas de 10 minutos cada hora.",
            "fisico": "Fatiga física indica recuperación insuficiente. 8 horas de sueño y nutrición adecuada son prioritarias.",
            "los dos": "Fatiga total detectada. Tu cuerpo y mente necesitan descanso urgente. Prioriza el sueño esta noche.",
            "si": "Insomnio prolongado detectado. Considera hablar con un médico sobre técnicas de higiene del sueño.",
            "no": "Cansancio puntual. Una buena noche de sueño debería restaurar tus niveles de energía."
        }
    },
    ("tristeza", "mal", "desanimado", "llorar", "ansiedad", "estres", "deprimido", "angustia", "miedo", "solo", "soledad", "panico"): {
        "preguntas": [
            "¿Este sentimiento lleva más de una semana?",
            "¿Hay algo específico que lo esté causando?"
        ],
        "respuesta_base": "Pico de cortisol y descenso de serotonina detectados. Estoy aquí para ti. Llorar es completamente normal.",
        "respuestas_detalle": {
            "semana": "Tristeza prolongada más de una semana puede indicar depresión. Hablar con un profesional puede ayudarte mucho.",
            "si": "Identificar la causa es el primer paso. ¿Quieres contarme más sobre lo que está pasando?",
            "no": "A veces el cuerpo acumula estrés sin razón aparente. Ejercicio suave y contacto social son tu mejor medicina.",
            "trabajo": "El estrés laboral es una causa común de ansiedad. Establecer límites y tomarte descansos es fundamental.",
            "examen": "La ansiedad ante exámenes es normal. Respira profundo, estás más preparado de lo que crees."
        }
    }
}


def evaluar_triage(sintoma: str) -> str:
    for palabra_roja in SINTOMAS_CRITICOS_ROJOS:
        if palabra_roja in sintoma:
            return "🔴 ALERTA ROJA: Este síntoma representa un riesgo vital. "
    for palabra_amarilla in SINTOMAS_CUIDADO_AMARILLO:
        if palabra_amarilla in sintoma:
            return "🟡 ADVERTENCIA: Este cuadro requiere monitoreo cuidadoso. "
    return ""


def generar_respuesta_medica(sintoma_detectado: str):
    if not sintoma_detectado:
        return "No logré aislar el área afectada. ¿Puedes repetir dónde sientes el malestar?"
    sintoma = sintoma_detectado.lower().strip()
    alerta_triage = evaluar_triage(sintoma)
    for grupo_sinonimos, protocolo in PROTOCOLOS_MAESTROS.items():
        if sintoma in grupo_sinonimos:
            return alerta_triage + protocolo["respuesta_base"]
        for sinonimo in grupo_sinonimos:
            if sinonimo in sintoma:
                return alerta_triage + protocolo["respuesta_base"]
    return "He registrado tu malestar. El protocolo estándar indica reposo preventivo y monitoreo de signos vitales."


def obtener_pregunta_seguimiento(sintoma_detectado: str, indice: int) -> str:
    """Retorna la pregunta de seguimiento según el síntoma e índice."""
    sintoma = sintoma_detectado.lower().strip()
    for grupo_sinonimos, protocolo in PROTOCOLOS_MAESTROS.items():
        encontrado = sintoma in grupo_sinonimos or any(s in sintoma for s in grupo_sinonimos)
        if encontrado:
            preguntas = protocolo.get("preguntas", [])
            if indice < len(preguntas):
                return preguntas[indice]
    return None


def obtener_respuesta_detalle(sintoma_detectado: str, respuesta_paciente: str) -> str:
    """Busca una respuesta específica según lo que dijo el paciente."""
    sintoma = sintoma_detectado.lower().strip()
    for grupo_sinonimos, protocolo in PROTOCOLOS_MAESTROS.items():
        encontrado = sintoma in grupo_sinonimos or any(s in sintoma for s in grupo_sinonimos)
        if encontrado:
            detalles = protocolo.get("respuestas_detalle", {})
            for clave, respuesta in detalles.items():
                if clave in respuesta_paciente:
                    return respuesta
    return None