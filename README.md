# Raton_Artificial

Uploading Vídeo sin título ‐ Hecho con Clipchamp.mp4…

Este es un proyecto de prueba diseñado para controlar el cursor del ratón a través de visión artificial. Utilizando gestos de mano, podrás mover el cursor y realizar clics. 

## Descripción

El proyecto se basa en el modelo **Hand Landmarker** de Google, que forma parte de la suite **MediaPipe**. Este modelo permite detectar y rastrear puntos clave en las manos, lo que facilita la interpretación de gestos para controlar el ratón.

- **Modelo utilizado**: [Hand Landmarker de MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker)
- **Funcionalidades**:
  - Movimiento del cursor basado en la posición de la mano.
  - Detección de gestos para realizar clics (solo izquierdo).
  - Control intuitivo y en tiempo real.

## Requisitos

Para ejecutar este proyecto, necesitarás:

- Python 3.x
- Una cámara web funcional

## Instalación y Ejecucion

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/Raton_Artificial.git
   cd Raton_Artificial
   python app.py


