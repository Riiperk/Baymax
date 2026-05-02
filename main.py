# ==============================================================================
# MAIN.PY - DIRECTOR DE ORQUESTA BAYX OS (V19.2)
# ==============================================================================
# Este es el núcleo del sistema. Coordina hilos de ejecución para el rostro,
# el sensor de voz y los actuadores de audio de forma sincronizada.
# ==============================================================================

import time
import sys
import random
import os     # Protocolos de acceso al sistema de archivos y ejecución de reportes
import pygame # Gestión de estados de hardware y hilos de audio secundarios

# ==============================================================================
# 1. INTEGRACIÓN DE LA ARQUITECTURA MODULAR INTEGRAL 
# ==============================================================================
# Intentamos vincular todos los módulos del proyecto.
# Si alguno falta, el sistema detendrá el arranque para evitar daños lógicos.
try:
    from modulo_voz import (
        hablar, 
        reproducir_inicio, 
        reproducir_musica, 
        detener_todo_audio, 
        atenuar_musica
    )
    # sor acústico con filtrado dinámico de eco y sordera selectiva
    from modulo_oidos import escuchar
    # Cargamos el córtex de decisión con todos sus atributos de estado cinematográficos
    from modulo_cerebro import procesar_pensamiento, EstadoSesion
    # Cargamos los sistemas de persistencia y generación de registros clínicos (.json y .txt)
    from modulo_memoria import cargar_perfil, generar_reporte_final
    # Cargamos el motor visual de animación del rostro basado en Tkinter
    from modulo_interfaz import iniciar_interfaz_en_hilo, actualizar_rostro
except ImportError as e:
    print(f"❌ [SISTEMA - ERROR CRÍTICO]: Falla al vincular módulos de hardware: {e}")
    sys.exit(1)

# ==============================================================================
# 2. CONFIGURACIÓN DEL HUD DE DIAGNÓSTICO (CONSOLA DE INGENIERÍA)
# ==============================================================================
def imprimir_hud_operativo():
    """Despliega el panel de control técnico en la terminal de VS Code con colores ANSI."""
    AZUL = '\033[94m'
    BLANCO = '\033[97m'
    VERDE = '\033[92m'
    CYAN = '\033[96m'
    AMARILLO = '\033[93m'
    RESET = '\033[0m'

    print("\n" + AZUL + "╔════════════════════════════════════════════════════════════════════╗")
    print("║" + BLANCO + "    (●—●)  BAYX OS v19.2 - NÚCLEO DE ASISTENCIA MÉDICA          " + AZUL + "║")
    print("╠════════════════════════════════════════════════════════════════════╣")
    print("║ " + VERDE + "[ACTIVO]" + BLANCO + " Hardware Audio: 8 Canales / Inmersión Musical Continua" + AZUL + "║")
    print("║ " + VERDE + "[ACTIVO]" + BLANCO + " Sensor STT: Sordera Selectiva Anti-Retroalimentación  " + AZUL + "║")
    print("║ " + VERDE + "[ACTIVO]" + BLANCO + " Lógica: Córtex Cerebral (Easter Eggs Habilitados)     " + AZUL + "║")
    print("║ " + VERDE + "[ACTIVO]" + BLANCO + " Interfaz: Motor de Animación Sincronizada 60 FPS      " + AZUL + "║")
    print("║ " + AMARILLO + "[MODO]  : COMPAÑERO DE SALUD PERSONAL                          " + AZUL + "║")
    print("╚════════════════════════════════════════════════════════════════════╝" + RESET + "\n")

# ==============================================================================
# 3. COORDINACIÓN MULTIMODAL (SINCRONIZACIÓN HARDWARE-SOFTWARE)
# ==============================================================================
def vocalizar_bayx(texto_respuesta: str, estado_global: EstadoSesion):
    """
    Sincroniza la síntesis de voz con la animación del rostro y el volumen de música.
    Asegura que Bayx sea el centro de atención acústica SOLO mientras él habla.
    """
    if not texto_respuesta: 
        return
    
    # 1. Atenuación Dinámica: Bajamos la música al 5% SOLO cuando Bayx va a hablar
    if estado_global.musica_reproduciéndose:
        atenuar_musica(True)
        
    # 2. Actualización Visual: El rostro activa la vibración de la boca
    actualizar_rostro("hablando")
    
    # 3. Salida de Audio: Se ejecuta la síntesis (Bloquea el hilo principal hasta terminar)
    hablar(texto_respuesta)
    
    # 4. Restauración: Los sistemas regresan a su estado previo tras hablar
    if estado_global.musica_reproduciéndose:
        # Recuperamos el volumen al 100% de ganancia inmediatamente después de hablar
        atenuar_musica(False) 
        actualizar_rostro("musica") # Ojos regresan a modo azul musicoterapia
    else:
        actualizar_rostro("neutral")

# ==============================================================================
# 4. NÚCLEO DE EJECUCIÓN (BUCLE DE CONCIENCIA PRINCIPAL)
# ==============================================================================
def arrancar_bayx():
    """Inicia la secuencia de arranque, saludo y el ciclo infinito de escucha."""
    
    # --- FASE 1: DESPLIEGUE DE INTERFAZ GRÁFICA ---
    print("🖥️ [FRONTEND]: Levantando motor gráfico en hilo paralelo...")
    iniciar_interfaz_en_hilo()
    actualizar_rostro("neutral") 

    imprimir_hud_operativo()
    
    # --- FASE 2: CARGA DE DATOS PERSISTENTES ---
    perfil_paciente = cargar_perfil()
    estado = EstadoSesion()

    print("🔌 [SISTEMA]: Inyectando protocolos de San Fransokyo en el bus...")
    reproducir_inicio() # Efecto de sonido de activación
    time.sleep(1.5) 
    
    # --- FASE 3: SECUENCIA DE SALUDO CINEMATOGRÁFICA ---
    from modulo_memoria import generar_saludo_inteligente
    saludo = generar_saludo_inteligente(perfil_paciente)
    if saludo:
        vocalizar_bayx(saludo, estado)
    else:
        vocalizar_bayx("Hola, yo soy Bayx, tu asistente médico personal.", estado)
        time.sleep(0.5)
        vocalizar_bayx("Escuché un sonido de angustia. ¿Tienes algún problema?", estado)

    # --- FASE 4: CICLO DE INTERACCIÓN ACTIVA ---
    try:
        while True:
            # 1. Ajuste de Sensores para la escucha
            # ¡CORRECCIÓN V19.2!: Se eliminó 'atenuar_musica(True)' aquí. 
            # Ahora la música NO bajará su volumen mientras Bayx espera a que hables.
            
            actualizar_rostro("escuchando") # Los ojos se expanden (feedback visual)
            
            # 2. Captura Acústica (Sensor STT con Sordera Selectiva)
            # Pasamos musica_activa=True para que el MIC ignore el ruido de fondo melódico
            comando_voz = escuchar(duracion_maxima=10, musica_activa=estado.musica_reproduciéndose)
            
            # 3. Restauración tras la escucha
            if estado.musica_reproduciéndose:
                # La música ya estaba al 100%, solo restauramos la cara
                actualizar_rostro("musica")
            else:
                actualizar_rostro("neutral")
            
            # Si el paciente no dijo nada coherente, reiniciamos el ciclo de guardia
            if not comando_voz: 
                continue

            print(f"\n👤 PACIENTE: {comando_voz}")

            # 4. Procesamiento Cerebral (Córtex Lógico v19.0)
            # El cerebro analiza la semántica y retorna una decisión de protocolo
            resultado = procesar_pensamiento(comando_voz, estado, perfil_paciente)
            estado = resultado["estado"] # Sincronización del estado de la sesión

            # 5. Ejecución de Actuadores (Física, Digital y Musical)
            
            # CASO: Protocolo de Cierre (El paciente está satisfecho)
            if resultado["id"] == "cierre":
                vocalizar_bayx(resultado["texto"], estado)
                break # Rompemos el ciclo para ir al apagado seguro y reporte

            # CASO: Detener Terapia de Audio
            elif resultado["id"] == "detener_musica":
                detener_todo_audio()
                estado.musica_reproduciéndose = False
                vocalizar_bayx(resultado["texto"], estado)

            # CASO: Iniciar Musicoterapia (Dinámico: Ánimo / Relax)
            elif resultado["id"] == "reproducir_musica":
                vocalizar_bayx(resultado["texto"], estado)
                # Seleccionamos la pista dinámicamente según la clasificación del cerebro
                tipo_pista = resultado.get("tipo_musica", "animo")
                reproducir_musica(tipo=tipo_pista)
                estado.musica_reproduciéndose = True
                actualizar_rostro("musica")

            # CASO: Protocolos Cinematográficos (Easter Eggs)
            elif resultado["id"] in ["bebe_peludo", "balalala", "aprender_punos", "bateria", "abrazo"]:
                vocalizar_bayx(resultado["texto"], estado)

            # CASO: Respuesta General (Médica o Charlas de Ollama)
            elif resultado["texto"]:
                vocalizar_bayx(resultado["texto"], estado)

            # Pequeña pausa estructural de CPU
            time.sleep(0.3)
            
    # --- FASE 5: DESACTIVACIÓN, REGISTRO Y APAGADO SEGURO ---
    except KeyboardInterrupt:
        print("\n\n⚠️ [SISTEMA]: Interrupción de hardware manual detectada por el ingeniero.")
    except Exception as error_nucleo:
        print(f"\n❌ [SISTEMA - ERROR CRÍTICO]: Falla imprevista en el núcleo: {error_nucleo}")
    finally:
        # Garantizamos el silencio y la neutralidad de la interfaz antes del cierre
        detener_todo_audio()
        actualizar_rostro("neutral")
        
        print("\n📄 [REGISTRO]: Compilando informe médico final en el disco duro...")
        # Esta función escribe el archivo .txt con el historial y biometrías
        archivo_reporte = generar_reporte_final(perfil_paciente, estado)
        
        if archivo_reporte:
            print(f"✅ [SISTEMA]: Reporte generado exitosamente: {archivo_reporte}")
            try:
                # Apertura automática del reporte para validación inmediata
                ruta_completa = os.path.join("Reportes_Clinicos", archivo_reporte)
                print(f"📂 [ABRIENDO]: {ruta_completa}")
                os.startfile(ruta_completa)
            except Exception as e_archivo:
                print(f"⚠️ [AVISO]: El reporte se guardó pero no pudo abrirse automáticamente: {e_archivo}")

        print("\n💤 [SISTEMA]: Bayx ha regresado a su terminal de carga. Protocolo finalizado.")
        time.sleep(1.0)
        sys.exit(0)

# ==============================================================================
# PUNTO DE IGNICIÓN (BOOTLOADER)
# ==============================================================================
if __name__ == "__main__":
    try:
        arrancar_bayx()
    except Exception as e_arranque:
        print(f"❌ [FALLO DE ARRANQUE]: {e_arranque}")  