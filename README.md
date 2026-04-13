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

2. Instala las dependencias:
   ```bash
   pip install pygame gTTS SpeechRecognition requests PyAudio
   ```

3. Ejecuta el sistema:
   ```bash
   python main.py
   ```

## Uso

1. Al iniciar, el sistema mostrará el HUD operativo en la consola.
2. La interfaz gráfica se abrirá automáticamente.
3. Bayx te saludará y comenzará a escuchar comandos de voz.
4. Describe tus síntomas y Bayx proporcionará consejos médicos apropiados.

## Funcionalidades Médicas

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
