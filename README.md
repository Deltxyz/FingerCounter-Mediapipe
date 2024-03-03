# Resultados de la práctica de una librería de IA

## Introducción
En este informe se presentan los resultados de la práctica de una librería de Inteligencia Artificial (IA) implementada en Python. La librería utilizada es Mediapipe, la cual se emplea para el reconocimiento y análisis de gestos y movimientos de manos en imágenes y videos.

## Desarrollo del Programa
El programa desarrollado hace uso de Mediapipe y otras librerías como OpenCV para la manipulación de imágenes y numpy para operaciones matemáticas. A continuación, se describen las principales funciones y procesos del programa:

### Funciones Implementadas
1. `centro_de_la_palma(lista_coordenadas)`: Esta función calcula el centro de la palma utilizando la media de las coordenadas de los puntos detectados.

2. `calcular_angulo_pulgar(coordenadas_pulgar)`: Calcula el ángulo formado por los puntos del pulgar utilizando el teorema del coseno.

3. `definir_colores()`: Define una serie de colores asociados a las etiquetas de cada elemento.

4. `definir_puntos()`: Define los grupos de puntos que se utilizarán para el análisis. Segun los hand landmarks proporcionados por mediapipe
![Hand Landmarks](https://developers.google.com/static/mediapipe/images/solutions/hand-landmarks.png)

5. `calcular_coordenadas(hand_landmarks, width, height)`: Calcula las coordenadas de los puntos de interés en la mano detectada.

6. `visualizar_informacion(frame, fingers_counter_left, fingers_counter_right, thickness_left, thickness_right)`: Muestra en pantalla la información del conteo de dedos y colores asociados.

### Proceso Principal
El programa inicia capturando el video de la cámara, luego utiliza Mediapipe para detectar y analizar las manos en tiempo real. A medida que se detectan manos, se calculan diversas métricas como el ángulo del pulgar y las distancias entre puntos clave.

Posteriormente, se visualizan en la pantalla los resultados, incluyendo el conteo de dedos y colores asociados a cada dedo. Además, se muestran los puntos clave y las conexiones entre ellos.

## Conclusiones
La aplicación de IA utilizando la librería Mediapipe en Python ha demostrado ser una herramienta efectiva para el análisis de gestos y movimientos de manos en tiempo real. El programa desarrollado permite realizar un seguimiento preciso de la posición y orientación de los dedos, así como el cálculo de ángulos relevantes.

## Recomendaciones
Se sugiere explorar la posibilidad de integrar esta funcionalidad en aplicaciones interactivas o sistemas de control que requieran la detección y seguimiento de gestos manuales.