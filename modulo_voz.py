# ==============================================================================
# MODULO_VOZ.PY - SUBSISTEMA DE SALIDA ACÚSTICA BAYX (V22.1 - EDGE-TTS)
# ==============================================================================
import pygame
import edge_tts
import asyncio
import os
import time
import sys
import random

# Voz + ajustes para sonar como Baymax:
# - Voz masculina Jorge (México) - más grave y calmada
# - Rate -15%: más lento y pausado como Baymax
# - Pitch -10Hz: más grave y robótico
VOZ_BAYX = "es-MX-JorgeNeural"
RATE = "-10%"
PITCH = "+0Hz"

# ==============================================================================
# 1. INICIALIZACIÓN DEL MOTOR DE AUDIO
# ==============================================================================
def inicializar_subsistema_acustico():
    print("🔌 [SISTEMA]: Iniciando motor acústico...")
    if pygame.mixer.get_init():
        pygame.mixer.quit()
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=8, buffer=4096)
        print("✅ [AUDIO-LOG]: Hardware de audio multicanal operando al 100%.")
    except Exception as e:
        print(f"❌ [AUDIO-ERROR FATAL]: {e}")
        sys.exit(1)

inicializar_subsistema_acustico()

CANAL_MUSICA = pygame.mixer.Channel(1)
CANAL_SFX = pygame.mixer.Channel(2)

CARPETA_CACHE = "audio_cache"
if not os.path.exists(CARPETA_CACHE):
    os.makedirs(CARPETA_CACHE)

# ==============================================================================
# 2. MOTOR DE SÍNTESIS NEURAL (edge-tts)
# ==============================================================================
async def generar_audio_async(texto: str) -> bytes:
    comunicar = edge_tts.Communicate(texto, VOZ_BAYX, rate=RATE, pitch=PITCH)
    audio_bytes = b""
    async for chunk in comunicar.stream():
        if chunk["type"] == "audio":
            audio_bytes += chunk["data"]
    return audio_bytes

def generar_audio(texto: str) -> bytes:
    return asyncio.run(generar_audio_async(texto))

# ==============================================================================
# 3. CONTROLADORES DE MÚSICA Y SFX
# ==============================================================================
def reproducir_inicio() -> None:
    ruta_inicio = os.path.join("sonidos", "inicio.wav")
    if os.path.exists(ruta_inicio):
        try:
            sfx_boot = pygame.mixer.Sound(ruta_inicio)
            CANAL_SFX.play(sfx_boot)
            CANAL_SFX.set_volume(0.9)
            print("🔊 [SISTEMA]: SFX de inicio ejecutado con éxito.")
        except Exception as e:
            print(f"⚠️ [AVISO]: El actuador SFX ha fallado: {e}")

def reproducir_musica(tipo: str = "animo") -> None:
    if tipo == "animo":
        opciones_pistas = ["animo.wav", "animo 2.wav"]
        print("\n🎵 [TERAPIA]: Iniciando protocolo de ESTIMULACIÓN DOPAMÍNICA.")
    elif tipo == "relajar":
        opciones_pistas = ["relajar.wav", "relajar2.wav"]
        print("\n🎵 [TERAPIA]: Iniciando protocolo de RELAJACIÓN.")
    else:
        opciones_pistas = ["animo.wav"]

    pista_final = random.choice(opciones_pistas)
    ruta_pista = os.path.join("sonidos", pista_final)

    if os.path.exists(ruta_pista):
        try:
            musica_objeto = pygame.mixer.Sound(ruta_pista)
            CANAL_MUSICA.set_volume(1.0)
            musica_objeto.set_volume(1.0)
            CANAL_MUSICA.play(musica_objeto, loops=-1)
            print(f"   [ 💿 INFO ]: Reproduciendo {pista_final} (Vol: 100%).")
        except Exception as e:
            print(f"❌ [ACTUADOR]: Error en Canal 1: {e}")

def detener_todo_audio() -> None:
    try:
        print("\n🔇 [SISTEMA]: Ejecutando protocolo de silencio total...")
        CANAL_MUSICA.fadeout(1200)
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"❌ [SISTEMA]: Error al detener audio: {e}")

def atenuar_musica(atenuar: bool) -> None:
    if atenuar:
        CANAL_MUSICA.set_volume(0.05)
    else:
        CANAL_MUSICA.set_volume(1.0)

# ==============================================================================
# 4. FUNCIÓN PRINCIPAL DE VOZ
# ==============================================================================
def hablar(texto: str, emocion: str = "neutral") -> None:
    texto_limpio = " ".join(texto.replace('\n', ' ').split()).strip()
    if not texto_limpio:
        return

    print(f"🤖 Bayx: {texto_limpio}")

    try:
        print("   [ 🎙️ Sintetizando voz neural... ]")
        audio_bytes = generar_audio(texto_limpio)

        if not audio_bytes:
            print("❌ [VOZ]: No se generó audio.")
            return

        ruta_temp = os.path.join(CARPETA_CACHE, f"temp_{int(time.time()*1000)}.mp3")
        with open(ruta_temp, "wb") as f:
            f.write(audio_bytes)

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        pygame.mixer.music.load(ruta_temp)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Limpiamos temporales viejos
        for archivo in os.listdir(CARPETA_CACHE):
            if archivo.startswith("temp_") and archivo != os.path.basename(ruta_temp):
                try:
                    os.remove(os.path.join(CARPETA_CACHE, archivo))
                except:
                    pass

    except Exception as e:
        print(f"\n❌ [SÍNTESIS-ERROR]: {e}")