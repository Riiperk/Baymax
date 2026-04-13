# ==============================================================================
# MODULO_VOZ.PY - SUBSISTEMA DE SALIDA ACÚSTICA BAYX (V19.4)
# ==============================================================================
# Este módulo gestiona la síntesis de voz neuronal (gTTS), la musicoterapia 
# multicanal y la gestión de la memoria acústica persistente.
# ------------------------------------------------------------------------------
# INNOVACIÓN V19.4: Blindaje contra archivos 0-bytes. Si el caché está corrupto,
# el sistema lo detecta, lo elimina y lo vuelve a descargar automáticamente.
# ==============================================================================

import pygame
import os
import hashlib
import time
import sys
import random
import io  # Vital para el parche de archivos corruptos
from gtts import gTTS

# ==============================================================================
# 1. INICIALIZACIÓN DEL MOTOR DE AUDIO (CAPA DE HARDWARE)
# ==============================================================================

def inicializar_subsistema_acustico():
    """
    Realiza una purga de los drivers de audio y levanta el mezclador multicanal.
    Diseñado para garantizar estabilidad en la sustentación del proyecto.
    """
    print("🔌 [SISTEMA]: Iniciando secuencia de ignición del motor acústico...")
    
    # Si el mezclador ya estaba iniciado por un proceso previo, lo reiniciamos.
    if pygame.mixer.get_init():
        pygame.mixer.quit()

    # Configuración de Grado Médico de San Fransokyo:
    # - Frecuencia: 44100Hz (Alta fidelidad)
    # - Canales: 8 canales de hardware para mezcla polifónica (Voz + Música).
    # - Buffer: 4096 para prevenir latencia o 'lag' en la síntesis de voz.
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=4096)
        print("✅ [AUDIO-LOG]: Hardware de audio multicanal operando al 100%.")
    except Exception as e:
        print(f"❌ [AUDIO-ERROR FATAL]: No se pudo acceder a la tarjeta de sonido: {e}")
        print("💡 Sugerencia técnica: Revisa que los altavoces estén conectados y el driver actualizado.")
        sys.exit(1)

# Ejecutamos la inicialización inmediatamente al importar el módulo para blindar el main.py
inicializar_subsistema_acustico()

# ASIGNACIÓN DE CANALES FÍSICOS DEDICADOS (Hard-Coded)
# Canal 1: Reservado para la Musicoterapia (Terapia de fondo continua).
# Canal 2: Reservado para Efectos de Sonido del sistema (SFX de encendido/alertas).
# Canal Maestro (music): Reservado para la síntesis de voz neuronal (gTTS).
CANAL_MUSICA = pygame.mixer.Channel(1)
CANAL_SFX = pygame.mixer.Channel(2)

# Configuración del Repositorio de Memoria Acústica (Caché local)
CARPETA_CACHE = "audio_cache"
if not os.path.exists(CARPETA_CACHE):
    try:
        print(f"📁 [SISTEMA]: Creando infraestructura de persistencia en: {CARPETA_CACHE}")
        os.makedirs(CARPETA_CACHE)
    except Exception as e:
        print(f"⚠️ [AVISO]: Error menor al crear directorio de caché: {e}")

# ==============================================================================
# 2. UTILIDADES DE PROCESAMIENTO DE SEÑAL Y PERSISTENCIA
# ==============================================================================

def limpiar_texto_vocal(texto: str) -> str:
    """
    Sanitiza el string eliminando ruidos sintácticos y saltos de línea.
    Garantiza que el motor gTTS genere una voz fluida y sin pausas raras.
    """
    if not texto: 
        return ""
    # Eliminamos saltos de línea y normalizamos espacios dobles
    texto_procesado = " ".join(texto.replace('\n', ' ').split()).strip()
    return texto_procesado

def generar_firma_acustica(texto: str) -> str:
    """
    Genera un identificador MD5 único basado en el contenido del texto.
    Permite a Bayx saber si ya ha dicho esta frase para evitar descargas innecesarias.
    """
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

# ==============================================================================
# 3. CONTROLADORES DE ACTUADORES ACÚSTICOS (MÚSICA Y SFX)
# ==============================================================================

def reproducir_inicio() -> None:
    """Ejecuta la secuencia de audio de arranque icónica de Bayx."""
    ruta_inicio = os.path.join("sonidos", "inicio.wav")
    if os.path.exists(ruta_inicio):
        try:
            # Los efectos de sistema tienen prioridad en el Canal 2
            sfx_boot = pygame.mixer.Sound(ruta_inicio)
            CANAL_SFX.play(sfx_boot)
            CANAL_SFX.set_volume(0.9) 
            print("🔊 [SISTEMA]: SFX de inicio ejecutado con éxito.")
        except Exception as e:
            print(f"⚠️ [AVISO]: El actuador SFX ha fallado: {e}")
    else:
        print("⚠️ [AVISO]: No se localizó 'inicio.wav'. Revisa la carpeta /sonidos.")

def reproducir_musica(tipo: str = "animo") -> None:
    """
    Activa la musicoterapia multicanal inyectando audio al Canal 1.
    INNOVACIÓN: Fuerza el volumen al 100% en cada inicio para blindar el Ducking.
    """
    # Selección de pistas según la clasificación del córtex cerebral
    if tipo == "animo":
        opciones_pistas = ["animo.wav", "animo 2.wav"]
        print("\n🎵 [TERAPIA]: Iniciando protocolo de ESTIMULACIÓN DOFAMÍNICA.")
    elif tipo == "relajar":
        opciones_pistas = ["relajar.wav", "relajar2.wav"]
        print("\n🎵 [TERAPIA]: Iniciando protocolo de RELAJACIÓN (Baja de cortisol).")
    else:
        opciones_pistas = ["animo.wav"]
        
    pista_final = random.choice(opciones_pistas)
    ruta_pista = os.path.join("sonidos", pista_final)
    
    if os.path.exists(ruta_pista):
        try:
            # 1. Cargamos el archivo en el buffer de sonido
            musica_objeto = pygame.mixer.Sound(ruta_pista)
            
            # 2. RESET DE GANANCIA ABSOLUTA
            # Obligamos al hardware a subir al 100% ignorando estados previos.
            CANAL_MUSICA.set_volume(1.0) 
            musica_objeto.set_volume(1.0)
            
            # 3. Play en bucle infinito (-1) para acompañamiento médico constante
            CANAL_MUSICA.play(musica_objeto, loops=-1)
            
            print(f"   [ 💿 INFO ]: Inyectando {pista_final} al Canal 1 (Vol: 100%).")
        except Exception as e:
            print(f"❌ [ACTUADOR]: Error de inyección de audio en Canal 1: {e}")
    else:
        print(f"❌ [ERROR]: El archivo {pista_final} está ausente en el directorio.")

def detener_todo_audio() -> None:
    """
    Aplica un protocolo de silencio absoluto con desvanecimiento (fade-out).
    Evita cortes bruscos que rompan la inmersión del paciente.
    """
    try:
        print("\n🔇 [SISTEMA]: Ejecutando protocolo de silencio total...")
        # Desvanecimiento de 1.2 segundos para una transición suave
        CANAL_MUSICA.fadeout(1200) 
        pygame.mixer.music.stop()
        pygame.mixer.music.unload() 
    except Exception as e:
        print(f"❌ [SISTEMA]: El bus de detención de audio presenta errores: {e}")

def atenuar_musica(atenuar: bool) -> None:
    """
    Control de Ducking Dinámico (Atenuación Automática).
    True: Reduce la música al 5% para priorizar la voz o escucha.
    False: Restaura la música al 100% de ganancia.
    """
    if atenuar:
        CANAL_MUSICA.set_volume(0.05)
    else:
        CANAL_MUSICA.set_volume(1.0)

# ==============================================================================
# 4. MOTOR DE SÍNTESIS DE VOZ NEURONAL (BAYX VOICE CORE)
# ==============================================================================

def animacion_hablando() -> None:
    """
    Genera un visualizador HUD en la terminal sincronizado con el bus de voz.
    Mantiene la consola activa mientras el hardware emite sonido.
    """
    frames_anim = ["  ▂ ▃ ▄ ▅ ▆ ▇ █", "█ ▇ ▆ ▅ ▄ ▃ ▂  ", "  ▃ ▅ ▇ █ ▇ ▅ ▃", "█ ▆ ▄ ▂   ▂ ▄ ▆"]
    idx = 0
    # Verificamos si el bus maestro está transmitiendo datos
    while pygame.mixer.music.get_busy():
        sys.stdout.write(f"\r   [ 🔊 TRANSMITIENDO... {frames_anim[idx % len(frames_anim)]} ]")
        sys.stdout.flush()
        time.sleep(0.12)
        idx += 1
    # Limpieza estética de la línea de comandos
    sys.stdout.write("\r" + " " * 75 + "\r")
    sys.stdout.flush()

def hablar(texto: str, emocion: str = "neutral") -> None:
    """
    Punto de entrada principal para la vocalización de Bayx.
    INNOVACIÓN V19.4: Detecta archivos de 0 bytes y los purga para evitar crashes.
    """
    texto_limpio = limpiar_texto_vocal(texto)
    if not texto_limpio: 
        return

    print(f"🤖 Bayx: {texto_limpio}")
    
    # Generamos identificador para la memoria local
    hash_id = generar_firma_acustica(texto_limpio)
    ruta_audio = os.path.join(CARPETA_CACHE, f"{hash_id}.mp3")

    try:
        # --- LÓGICA DE PERSISTENCIA ACÚSTICA CON BLINDAJE ---
        # Verificamos si el archivo NO existe, o si existe pero pesa 0 bytes (corrupto)
        if not os.path.exists(ruta_audio) or os.path.getsize(ruta_audio) == 0:
            print("   [ ☁️  CLOUD ]: Sintetizando nueva respuesta neuronal...")
            # Si el archivo existía pero estaba corrupto, gTTS lo sobreescribirá
            tts = gTTS(text=texto_limpio, lang='es', tld='com.mx')
            tts.save(ruta_audio)
        else:
            # Reutilización instantánea: Carga desde el disco duro
            print("   [ 💽 CACHÉ ]: Paquete de voz recuperado de memoria local.")
        
        # Freno de seguridad: Detenemos cualquier audio maestro anterior antes de cargar uno nuevo
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        # --- PARCHE PARA 'BAD TAGS' (BytesIO) ---
        with open(ruta_audio, "rb") as f:
            datos_audio = io.BytesIO(f.read())
            
        # Inyectamos el buffer de memoria en el canal maestro
        pygame.mixer.music.load(datos_audio)
        pygame.mixer.music.set_volume(1.0) # Forzamos volumen máximo para Bayx
        pygame.mixer.music.play()
        
        # Sincronizamos con el visualizador HUD
        animacion_hablando()
            
    except Exception as e_vocal:
        print(f"\n❌ [SÍNTESIS-ERROR]: Protocolo fallido. Detalle técnico: {e_vocal}")

# ==============================================================================
# FIN DEL MÓDULO DE VOZ - VERSIÓN 19.4
# ==============================================================================