import cv2


class DetectorMovimiento:

    def __init__(self):
        # Abre el video
        self.cap = cv2.VideoCapture("videos/prueba_manguera.mp4")

        # Sustracción de fondo.
        self.fgbg = cv2.createBackgroundSubtractorKNN()
        # self.fgbg = cv2.createBackgroundSubtractorMOG2()

    def activar(self):

        # Comprueba si el video se abrió correctamente
        if not self.cap.isOpened():
            print("Error al abrir el video")

        while self.cap.isOpened():
            # Lee el video frame por frame
            ret, frame = self.cap.read()

            if ret:
                # Coordenadas del rectángulo
                pt1 = (frame.shape[1] // 3, frame.shape[0] // 3)
                pt2 = (frame.shape[1] - frame.shape[1] // 3, frame.shape[0] - frame.shape[0] // 3)

                # Párametros del texto de aviso cuando está inactivo
                texto = "Apagado"
                color = (0, 255, 0)

                # Aplicación de sustracción de fondo solo en el área del rectángulo
                fgmask = self.fgbg.apply(frame[pt1[1]:pt2[1], pt1[0]:pt2[0]])

                # Busca los contornos en la máscara de la sustracción de fondo
                contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Filtra los contornos basándote en su área
                min_area = 1000  # ajusta esto a tus necesidades
                for contour in contours:
                    if cv2.contourArea(contour) > min_area:
                        # Parámetros del texto de aviso que está activo
                        texto = "Encendido"
                        color = (0, 0, 255)
                        # Dibujo contornos
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(img=frame,
                                      pt1=(pt1[0] + x, pt1[1] + y),
                                      pt2=(pt1[0] + x + w, pt1[1] + y + h),
                                      color=(0, 0, 255),
                                      thickness=2)

                # Creación rectangulo de zona de control
                cv2.rectangle(img=frame,
                              pt1=pt1,
                              pt2=pt2,
                              color=color,
                              thickness=2)

                # Texto de aviso
                cv2.putText(img=frame,
                            text=texto,
                            org=(20, 40),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1,
                            color=color,
                            thickness=1)

                # Muestra la máscara de sustracción de fondo
                # cv2.imshow("Sustracción", fgmask)

                # Muestra el frame
                cv2.imshow('Video', frame)

                # Reproduciendo a la mitad de velocidad
                if cv2.waitKey(int(1000 / (2 * self.cap.get(cv2.CAP_PROP_FPS)))) & 0xFF == ord('q'):
                    break
            else:
                break

        # Cierra el video
        self.cap.release()

        # Cierra todas las ventanas de OpenCV
        cv2.destroyAllWindows()
