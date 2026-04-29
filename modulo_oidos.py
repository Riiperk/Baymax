# Whisper nos sirve para usar a Baymax en modo offline, sin necesidad de conexión a internet. Tambien funciona mejor que GTTS
import speech_recognition as sr
import numpy as np
import sys
from faster_whisper import WhisperModel

print("🧠 [OIDOS]: Cargando modelo Whisper...")
try:
    modelo_whisper = WhisperModel("small", device="cpu", compute_type="int8")
    print("✅ [OIDOS]: Whisper listo. Modo offline activado.")
except Exception as e:
    print(f"❌ [OIDOS - ERROR FATAL]: {e}")
    sys.exit(1)

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5
recognizer.dynamic_energy_threshold = False

def inicializar_sensores():
    print("🔌 [Escaneando hardware de entrada de audio...]")
    try:
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            print("❌ [ERROR CRÍTICO] No se detectó micrófono.")
            sys.exit(1)
        print(f"✅ [Sensor detectado: {mics[0][:50]}...]")
    except Exception as e:
        print(f"❌ [Falla de hardware]: {e}")
        sys.exit(1)

inicializar_sensores()

def escuchar(duracion_maxima=10, musica_activa=False):
    print("\n   [ 👂 Bayx escuchando con Whisper... ]")
    
    if musica_activa:
        recognizer.energy_threshold = 1500
    else:
        recognizer.energy_threshold = 300

    try:
        with sr.Microphone(sample_rate=16000) as source:
            try:
                audio = recognizer.listen(
                    source,
                    timeout=5.0,
                    phrase_time_limit=duracion_maxima
                )
                
                print("   [ 🧠 Procesando con Whisper offline... ]")
                
                # Convertimos el audio a números que Whisper entiende
                # Sin ffmpeg, directo en RAM
                wav_data = audio.get_wav_data()
                audio_np = np.frombuffer(wav_data, dtype=np.int16).astype(np.float32) / 32768.0
                
                segmentos, _ = modelo_whisper.transcribe(
                    audio_np,
                    language="es",
                    initial_prompt="Síntomas médicos: me duele el brazo, tengo fiebre, Bayx"
                )
                
                texto = " ".join([s.text for s in segmentos]).strip()
                if texto:
                    return texto.lower()
                return ""
                
            except sr.WaitTimeoutError:
                return ""
            except Exception as e:
                print(f"   [ ❌ Error de transcripción: {e} ]")
                return ""
                
    except Exception as e:
        print(f"❌ [Falla en el micrófono: {e}]")
        return ""