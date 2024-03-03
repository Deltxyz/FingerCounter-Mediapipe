# Modulos empleados en el desarrollo del programa
import cv2
import mediapipe as mp
import numpy as np

def centro_de_la_palma(lista_coordenadas):
     coordenadas = np.array(lista_coordenadas)
     centro = np.mean(coordenadas, axis=0)
     centro = int(centro[0]), int(centro[1])
     return centro


def calcular_angulo_pulgar(coordenadas_pulgar):
     p1 = np.array(coordenadas_pulgar[0])
     p2 = np.array(coordenadas_pulgar[1])
     p3 = np.array(coordenadas_pulgar[2])

     l1 = np.linalg.norm(p2 - p3)
     l2 = np.linalg.norm(p1 - p3)
     l3 = np.linalg.norm(p1 - p2)

     # Calcular el ángulo usando el teorema del coseno
     try:
          angulo = np.arccos((l1**2 + l3**2 - l2**2) / (2 * l1 * l3))
     except Exception as e:
          print(e)
          return 0
     return angulo


def definir_colores():
     colores=dict()
     colores['Pulgar'] = (0, 151, 229)       #Naranja
     colores['Indice'] = (202, 204, 1)       #Celeste
     colores['Medio'] = (0, 204, 255)        #Amarillo
     colores['Anular'] = (48, 255, 48)       #Verde
     colores['Menique'] = (192, 101, 21)     #Azul
     return colores


def definir_puntos():
     puntos = dict()
     puntos['palma']= [0, 1, 2, 5, 9, 13, 17]
     puntos['pulgar'] = [1, 2, 4]
     puntos['extremos'] = [8, 12, 16, 20]         # [Índice, medio, anular y meñique]
     puntos['base'] =[6, 10, 14, 18]              # [Índice, medio, anular y meñique]
     return puntos


def calcular_coordenadas(hand_landmarks, width, height):
     puntos = definir_puntos()
     coordenadas = dict()
     for key in puntos:
          coordenadas[key] =list()
          for index in puntos[key]:
               x = int(hand_landmarks.landmark[index].x * width)
               y = int(hand_landmarks.landmark[index].y * height)
               coordenadas[key].append([x, y])

     coordenadas['centroide'] =  np.array(centro_de_la_palma(coordenadas['palma']))
     return coordenadas


def visualizar_informacion(frame, fingers_counter_left, fingers_counter_right, thickness_left, thickness_right):

     colores = definir_colores()
     ancho = frame.shape[1] 

    # Dibuja el contador de la mano izquierda
     cv2.rectangle(frame, (0, 0), (80, 80), (125, 220, 0), -1)
     cv2.putText(frame, fingers_counter_left, (15, 65), 1, 5, (255, 255, 255), 2)

    # Dibuja el contador de la mano derecha
     cv2.rectangle(frame, (ancho - 80, 0), (ancho, 80), (125, 220, 0), -1)
     cv2.putText(frame, fingers_counter_right, (ancho - 65, 65), 1, 5, (255, 255, 255), 2)

     pos = 90
     i = 0
     for key in colores:

          cv2.rectangle(frame, (ancho-65, pos), (ancho-15 , pos+50), colores[key], thickness_right[i])
          cv2.putText(frame, key, (ancho-65, pos+60), 1, 1, colores[key], 2)
     
          cv2.rectangle(frame, (15, pos), (65, pos+50), colores[key], thickness_left[i])
          cv2.putText(frame, key, (15, pos+60), 1, 1, colores[key], 2)


          pos+=90
          i+=1

     cv2.imshow(".:Conteo:.", frame)


def main():
     mp_drawing = mp.solutions.drawing_utils
     mp_drawing_styles = mp.solutions.drawing_styles
     mp_hands = mp.solutions.hands

     camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)

     with mp_hands.Hands(max_num_hands=2) as hands:  
          try:
               while True:
                    ret, frame = camara.read()

                    if ret == False:
                         break

                    frame = cv2.flip(frame, 1)
                    scale_percent = 120
                    width = int(frame.shape[1] * scale_percent / 100)
                    height = int(frame.shape[0] * scale_percent / 100)
                    frame = cv2.resize(frame, (width, height))


                    height, width, _ = frame.shape
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = hands.process(frame_rgb)
                    results2 = results.multi_handedness
                    fingers_counter_left = "-"
                    fingers_counter_right = "-"
                    thickness_left = [2]*5
                    thickness_right = [2]*5


                    hand_landmarks = results.multi_hand_landmarks
                    if hand_landmarks:

                         for i in range(len(hand_landmarks)):  
                              hand_landmark = hand_landmarks[i]
                              coordenadas = calcular_coordenadas(hand_landmark,width, height)

                              # Pulgar
                              angulo = calcular_angulo_pulgar(coordenadas['pulgar'])
                              thumb_finger = np.array(angulo > 2.62)
                              
                              # Dibujar el punto medio de la palma
                              cv2.circle(frame, tuple(coordenadas['centroide']), 3, (0, 0, 255), 2)

                              # Distancias
                              d_centrid_ft = np.linalg.norm(coordenadas['centroide'] - coordenadas['extremos'], axis=1)
                              d_centrid_fb = np.linalg.norm(coordenadas['centroide'] - coordenadas['base'], axis=1)
                              
                              # Diferencia porcentual de distancias
                              dif = (d_centrid_ft - d_centrid_fb)
                              fingers = dif > 0

                              fingers = np.append(thumb_finger, fingers)

                              fingers_counter = str(np.count_nonzero(fingers==True))
                              #labell = results2[i].classification[0].label

                              #print(type(labell) , labell)
                              if results2[i].classification[0].label == 'Left': 
                                   fingers_counter_left = fingers_counter
                                   for (i, finger) in enumerate(fingers):
                                        if finger == True:
                                             thickness_left[i] = -1
                              else:  # Si es la segunda mano
                                   fingers_counter_right = fingers_counter
                                   for (i, finger) in enumerate(fingers):
                                        if finger == True:
                                             thickness_right[i] = -1

                              mp_drawing.draw_landmarks(frame, 
                                                        hand_landmark, 
                                                        mp_hands.HAND_CONNECTIONS, 
                                                        mp_drawing_styles.get_default_hand_landmarks_style(), 
                                                        mp_drawing_styles.get_default_hand_connections_style())

                    visualizar_informacion(frame, fingers_counter_left, fingers_counter_right, thickness_left, thickness_right)

                    if cv2.waitKey(5) & 0xFF == ord('q'):

                         break

          except Exception as e:
               print(e)
          
     camara.release()
     cv2.destroyAllWindows()


main()