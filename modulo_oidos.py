# ==============================================================================
# MODULO_OIDOS.PY - SUBSISTEMA DE CAPTURA ACÚSTICA BAYX (V20.1 - WHISPER)
# ==============================================================================
import speech_recognition as sr
import whisper
import numpy as np
import sys

print("🧠 [OIDOS]: Cargando modelo Whisper...")
try:
    modelo_whisper = whisper.load_model("small")
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

                wav_data = audio.get_wav_data()
                audio_np = np.frombuffer(wav_data, dtype=np.int16).astype(np.float32) / 32768.0

                resultado = modelo_whisper.transcribe(
                    audio_np,
                    language="es",
                    fp16=False,
                    initial_prompt="Síntomas médicos: me duele el brazo, tengo fiebre, me duele la cabeza, Bayx"
                )

                texto = resultado["text"].strip()
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