import speech_recognition as sr
import sys
import time

# =================================================================
# 1. DIAGNÓSTICO Y CALIBRACIÓN DE SENSORES
# =================================================================
def inicializar_sensores():
    """
    Realiza un escaneo profundo del hardware de audio para asegurar 
    su operatividad antes de arrancar el núcleo del sistema.
    """
    print("🔌 [Escaneando hardware de entrada de audio...]")
    try:
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            print("❌ [ERROR CRÍTICO] No se detectó hardware de captura.")
            print("💡 Sugerencia: Revisa la conexión del micrófono y permisos de Windows.")
            sys.exit(1)
        
        print(f"✅ [Sensor detectado: {mics[0][:40]}...]")
    except Exception as e:
        print(f"❌ [Falla de hardware]: {e}")
        sys.exit(1)

# Ejecutamos la inicialización al cargar el módulo
inicializar_sensores()

# =================================================================
# 2. NÚCLEO DE PROCESAMIENTO ACÚSTICO (Configuración Estática)
# =================================================================
recognizer = sr.Recognizer()

# --- AJUSTES DE PRECISIÓN CLÍNICA ---
# Tiempo de silencio para considerar fin de frase (1.0s permite pausas naturales)
recognizer.pause_threshold = 1.0 

# Margen de seguridad para capturar el inicio y final de las palabras completas
recognizer.non_speaking_duration = 0.5

# 🚀 INNOVACIÓN ANTI-ECO: Apagamos el ajuste dinámico (False). 
# Si lo dejamos encendido, el micrófono se vuelve loco tratando de 
# ajustarse a los bajos y agudos de la música. Lo forzamos a estático.
recognizer.dynamic_energy_threshold = False 

# =================================================================
# 3. FUNCIÓN MAESTRA DE ESCUCHA (Con Sordera Selectiva)
# =================================================================
def escuchar(duracion_maxima=10, musica_activa=False): 
    """
    Captura la voz del usuario. 
    Si 'musica_activa' es True, baja drásticamente la sensibilidad del
    micrófono para que Bayx ignore la música y solo escuche tu voz.
    """
    print("\n   [ 👂 Bayx ajustando sensores y escuchando... ]")
    
    try:
        with sr.Microphone() as source:
            
            # --- FILTRO DE AISLAMIENTO ACÚSTICO ---
            # Dependiendo de si hay música o no, cambiamos la "dureza" del oído.
            if musica_activa:
                # El oído se vuelve 'sordo' a los ruidos menores a 1500 de energía.
                # La música de fondo (que atenuaremos en el main) no pasará de 500.
                # Solo tu voz directa, hablando hacia el micrófono, pasará este filtro.
                recognizer.energy_threshold = 1500 
            else:
                # Sensibilidad normal para una habitación en silencio (escucha hasta susurros)
                recognizer.energy_threshold = 300  
            
            try:
                # Captura de la señal de audio
                audio = recognizer.listen(
                    source, 
                    timeout=5.0, # Tiempo máximo de espera a que empieces a hablar
                    phrase_time_limit=duracion_maxima # Límite de la frase completa
                )
                
                print("   [ 🌐 Procesando paquete acústico en la nube... ]")
                
                # Traducción a texto (Usamos es-CO para mayor precisión del acento local)
                texto = recognizer.recognize_google(audio, language="es-CO")
                return texto.lower().strip()
                
            except sr.WaitTimeoutError:
                # El usuario no habló en los 5 segundos de timeout
                return "" 
                
            except sr.UnknownValueError:
                # Se detectó un ruido que superó el umbral de energía, 
                # pero no era lenguaje coherente (Ej. un pico fuerte de la canción)
                return ""
                
            except sr.RequestError as e:
                # Fallo en la conexión con los servidores de Google
                print(f"   [ ❌ Error de enlace de datos: {e} ]")
                return ""
                
    except Exception as e_acustico:
        # Fallo general del bus de audio (Micrófono desconectado en pleno uso)
        print(f"❌ [Falla en el bus de datos acústicos: {e_acustico}]")
        return ""