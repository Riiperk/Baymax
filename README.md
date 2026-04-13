# Bayx OS - Asistente Médico Inteligente

## Descripción

Bayx OS es un sistema de asistencia médica inteligente basado en IA, inspirado en Baymax de la película *Big Hero 6*. Este sistema proporciona soporte médico personalizado a través de una interfaz multimodal que incluye voz, visión y procesamiento cognitivo avanzado.

## Características Principales

- **Interfaz Multimodal**: Combina síntesis de voz, reconocimiento de voz, interfaz gráfica animada y procesamiento de lenguaje natural.
- **Diagnóstico Médico**: Motor de evaluación de síntomas con protocolos médicos basados en evidencia.
- **Musicoterapia**: Integración de música terapéutica para mejorar la experiencia del paciente.
- **Persistencia de Datos**: Almacenamiento de perfiles de pacientes y generación de reportes clínicos.
- **Interfaz Gráfica**: Rostro animado que refleja el estado emocional y de procesamiento del sistema.

## Arquitectura del Sistema

El sistema está compuesto por los siguientes módulos:

- `main.py`: Núcleo de coordinación y bucle principal de ejecución.
- `modulo_cerebro.py`: Procesamiento cognitivo y toma de decisiones.
- `modulo_interfaz.py`: Interfaz gráfica animada del rostro.
- `modulo_memoria.py`: Gestión de perfiles de pacientes y reportes.
- `modulo_oidos.py`: Reconocimiento de voz y procesamiento auditivo.
- `modulo_voz.py`: Síntesis de voz y gestión de audio.
- `tratamiento.py`: Base de datos de protocolos médicos y evaluación de síntomas.

## Requisitos del Sistema

- Python 3.12.10
- Bibliotecas: pygame, tkinter (incluido en Python estándar), speech_recognition, pyttsx3
- Sistema operativo: Windows/Linux/MacOS

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/proyecto_bayx.git
   cd proyecto_bayx
   ```
2. Crear entorno Virtual ENV
   ```bash
   pip install virtualenv #Instala virtual ENV
   virtualenv env # Crea el entorno Virtual
   ./env/Scripts/activate #Lo activa
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser # ESTE COMANDO POR SI LE MOLESTA LAS EXCEPCIONES Y LE TIRA ERROR DE SCRIPTS / ESTE COMANDO SOLO FUNCIONA POR SESIÓN
   
   ```


3. Instala las dependencias:
   ```bash
   pip install pygame gTTS SpeechRecognition requests PyAudio
   ```
4. **Instalación del Motor de IA Generativa (Requisito para charla natural):**
   Bayx utiliza un modelo de lenguaje local para garantizar la privacidad y mantener su personalidad cuando no está dando diagnósticos médicos.
   - Descarga e instala [Ollama](https://ollama.com/).
   - Abre una nueva terminal y ejecuta el siguiente comando para descargar el modelo neuronal:
     ```bash
     ollama run phi3
     ```
   - Asegúrate de que Ollama esté ejecutándose en segundo plano (puerto `localhost:11434`) antes de iniciar `main.py`.


5. Ejecuta el sistema:
   ```bash
   python main.py
   ```

## Uso

1. Al iniciar, el sistema mostrará el HUD operativo en la consola.
2. La interfaz gráfica se abrirá automáticamente.
3. Bayx te saludará y comenzará a escuchar comandos de voz.
4. Describe tus síntomas y Bayx proporcionará consejos médicos apropiados.

## Funcionalidades Médicas

### Monitoreo Químico-Emocional
- **Escaneo Semántico:** Detección en tiempo real del estado de ánimo del paciente a través del procesamiento de lenguaje natural.
- **Categorización:** Identificación automática de estados de Ansiedad, Tristeza, Alegría o Neutralidad.
- **Registro Clínico:** Inclusión del estado emocional en el reporte final `.txt` generado por el módulo de memoria.

### Evaluación de Síntomas
- Clasificación por niveles de urgencia (Rojo, Amarillo, Verde)
- Protocolos específicos para diferentes sistemas corporales
- Recomendaciones de tratamiento basadas en evidencia

### Sistemas Corporales Soportados
- Neurológico y cefálico
- Cardiovascular y respiratorio
- Gastrointestinal
- Musculoesquelético
- Sensorial (vista, oído)

## Protocolos Cinematográficos (Easter Eggs)

Para mantener la esencia del personaje de San Fransokyo, el sistema cuenta con comandos ocultos que activan respuestas y comportamientos icónicos:
- **"Bebé Peludo" / "Gato":** Activa el protocolo de reducción de estrés mediante frecuencias de ronroneo.
- **"Chocar los puños":** Secuencia de interacción social de dos pasos que culmina con el icónico sonido "¡Balalala!".
- **"Dame un abrazo":** Activa el protocolo de soporte físico para la liberación de oxitocina.
- **"Batería baja":** Reacción a niveles bajos de energía del sistema.
- **Escena de la Pubertad:** Respuesta automática inofensiva si el paciente reporta un nivel de dolor de 0 o 1 tras un diagnóstico.

## Optimizaciones de Hardware

- **Memoria Acústica Hash MD5:** Sistema de caché local (`audio_cache/`) que guarda las frases sintetizadas por Google (gTTS). Evita latencia y ahorra consumo de red al reutilizar audios instantáneamente.
- **Blindaje BytesIO:** Corrección de grado industrial para motores Pygame, evitando crasheos por etiquetas MP3 corruptas (bad tags) provenientes de la nube.
- **Ducking Dinámico:** Gestión inteligente de los 8 canales físicos de audio. La musicoterapia fluye al 100% de volumen y solo se atenúa (5%) de manera elegante cuando Bayx emite un diagnóstico vocal.

## Configuración

El sistema incluye configuraciones avanzadas para:
- Filtrado de eco en reconocimiento de voz
- Atenuación dinámica de música durante interacciones
- Generación automática de reportes clínicos
- Persistencia de estados de sesión

## Seguridad y Privacidad

- Todos los datos de pacientes se almacenan localmente
- No se transmite información médica a servidores externos
- Cumple con estándares de privacidad médica básicos

## Desarrollo

### Estructura del Código
```
proyecto_bayx/
├── main.py                 # Punto de entrada principal
├── modulo_*.py            # Módulos especializados
├── tratamiento.py         # Base de datos médica
├── memoria_paciente.json  # Almacenamiento de perfiles
├── audio_cache/           # Cache de archivos de audio
├── sonidos/               # Archivos de audio del sistema
└── Reportes_Clinicos/     # Reportes generados
```

### Contribuir
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, contacta al equipo de desarrollo.

## Versiones

- v19.2: Eliminación de ducking durante escucha, mejora en musicoterapia
- v17.0: Motor de evaluación de triage médico avanzado

---

*Bayx OS - Tu compañero médico personal*    
