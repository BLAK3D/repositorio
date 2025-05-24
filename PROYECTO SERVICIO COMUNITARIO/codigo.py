from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFrame, QPushButton, QMessageBox, QLineEdit
from PyQt5.QtCore import QTimer, QEvent, Qt
from PyQt5.QtGui import QIntValidator
import sys

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow,  self).__init__()
        loadUi("ventana_espectador.ui", self)
        self.control_window = None  # Referencia a la ventana de control (se asigna externamente)

        self.contador = self.findChild(QLabel, "contador_1")
        self.contador2 = self.findChild(QLabel, "contador_2")
        self.blue_frame = self.findChild(QFrame, "frame_azul")
        self.yellow_blue_frame = self.findChild(QFrame, "tiempo_azul")
        self.yellow_red_frame = self.findChild(QFrame, "tiempo_rojo")
        self.punto_azul = self.findChild(QLabel, "puntos_azul")
        self.punto_rojo = self.findChild(QLabel, "puntos_rojo1")
        self.foto_rojo = self.findChild(QFrame, "foto_rojo")
        self.foto_azul = self.findChild(QFrame, "foto_azul")
        self.info_rojo = self.findChild(QFrame, "info_rojo")
        self.info_azul = self.findChild(QFrame, "info_azul")
        
        
        self.ajuste_tiempo(0)
        self.play_tiempo()
        
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.cuadrar)
        self.timer2.start(1) 
       
        
    def ajuste_ventana(self):
        self.yellow_blue_frame.setGeometry(0, self.blue_frame.height() - 60, round(self.blue_frame.width() * 0.55), 116)
        self.yellow_red_frame.setGeometry(0, -60, round(self.blue_frame.width() * 0.55), 116)
        self.contador.setGeometry(self.yellow_blue_frame.width() - 265, 10, 250, 90)
        self.contador2.setGeometry(self.yellow_blue_frame.width() - 265, 10, 250, 90)
        self.punto_rojo.setGeometry(self.blue_frame.width() -320, round((self.blue_frame.height() - 240)/ 2), 300, 240)
        self.punto_azul.setGeometry(self.blue_frame.width() -320, round((self.blue_frame.height() - 240)/ 2), 300, 240)
        self.foto_azul.setGeometry(30, round((self.blue_frame.height() -210)/2), 130, 150)
        self.foto_rojo.setGeometry(30, round(((self.blue_frame.height() -210)/2) +60), 130, 150)
        
        if self.blue_frame.width() > 1030:
            self.info_azul.setGeometry(170, round((self.blue_frame.height() -250)/2) , 540, 190)
            self.info_rojo.setGeometry(170, round((self.blue_frame.height() -250)/2) + 60 , 540, 190)
        else:
            self.info_azul.setGeometry(170, round((self.blue_frame.height() -250)/2), 410, 190)
            self.info_rojo.setGeometry(170, round((self.blue_frame.height() -250)/2) + 60 , 410, 190)
        
        self.tamano_letra(self.punto_azul, round(self.blue_frame.height() * 0.56))
        self.tamano_letra(self.punto_rojo, round(self.blue_frame.height() * 0.56))
        
    def resizeEvent(self, event):
        # Ajustar posición cuando la ventana cambia de tamaño 
        self.ajuste_ventana()
        super().resizeEvent(event)
        
    def closeEvent(self, event):
        confirm = QMessageBox.question(
            self,
            "Confirmar cierre",
            "¿Estás seguro que deseas cerrar la ventana?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            event.accept()
            if self.control_window:
                self.control_window.close()  # Cierra la ventana de control si existe
        else:
            event.ignore()
       
    def cuadrar(self):
        self.ajuste_ventana()
        self.timer2.stop()
        
    def tamano_letra(self, label, tamaño: int):
        fuente_actual = label.font()  # Obtener la fuente actual
        fuente_actual.setPointSize(tamaño)  # Cambiar el tamaño en puntos
        label.setFont(fuente_actual)  # Aplicar de nuevo al label
        
    def actualizar_contador(self):
        if self.segundos >= 0:
            minutos = self.segundos // 60
            segundos = self.segundos % 60
            self.contador.setText(f"{minutos}:{segundos:02d}")
            self.contador2.setText(f"{minutos}:{segundos:02d}")
            self.segundos -= 1
        else:
            self.timer.stop() 
        
    def play_tiempo(self):
        if not self.timer.isActive():
            self.timer.start(1000)
            print("Temporizador iniciado")
    
    def pause_tiempo(self):
        if self.timer.isActive():
            self.timer.stop()
            print("Temporizador pausado")
            
    def ajuste_tiempo(self, seg: int):
        self.segundos = seg  # Tiempo inicial en segundos
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_contador)

    
class ControlVentana(QMainWindow):
    def __init__(self, ventana_espectador):
        super().__init__()
        loadUi("ventana_control.ui", self)
        self.ventana_espectador = ventana_espectador
        self.boton_control = self.findChild(QPushButton, "play_pause")
        self.editar = self.findChild(QPushButton, "editar")
        self.cancelar = self.findChild(QPushButton, "cancelar")
        self.subir_pts_azul = self.findChild(QPushButton, "subir_pts_azul")
        self.bajar_pts_azul = self.findChild(QPushButton, "bajar_pts_azul")
        self.subir_pts_rojo = self.findChild(QPushButton, "subir_pts_rojo")
        self.bajar_pts_rojo = self.findChild(QPushButton, "bajar_pts_rojo")
        self.tiempo_seg = self.findChild(QLineEdit, "tiempo_seg")
        self.tiempo_min = self.findChild(QLineEdit, "tiempo_min")
        self.dar_pts = self.findChild(QFrame, "dar_pts")
        self.pausado = self.findChild(QLabel, "pausado")
        self.tiempo_min.setText("0")
        self.tiempo_seg.setText("00")
        self.cancelar.hide()
        self.dar_pts.hide()
        
        self.boton_control.clicked.connect(self.cambiar_estado_timer)
        self.editar.clicked.connect(self.permitir_cambios)
        self.cancelar.clicked.connect(self.restaurar_tiempo)
        
        validador_seg = QIntValidator(0, 59)
        self.tiempo_seg.setValidator(validador_seg)
        self.tiempo_seg.setMaxLength(2)
        self.tiempo_seg.textChanged.connect(self.validar_seg)
        
        validador_min = QIntValidator(0, 9)
        self.tiempo_min.setValidator(validador_min)
        self.tiempo_min.setMaxLength(1)
        self.tiempo_min.textChanged.connect(self.capturar_cambio_tiempo)
        
        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.actualizar_contador_control)
        
        
    def closeEvent(self, event):
        confirm = QMessageBox.question(
            self,
            "Confirmar cierre",
            "¿Estás seguro que deseas cerrar la ventana? (Se cerrara todas las ventanas del sistema)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.ventana_espectador.close()  # Cierra la ventana de espectador
            event.accept()
        else:
            event.ignore()
    
    def validar_seg(self, texto):
        self.tiempo_seg.textChanged.disconnect()
        try:
            if texto:
                valor = int(texto)
                if valor > 59:
                    self.tiempo_seg.setText("59")
                elif valor < 0:
                    self.tiempo_seg.setText("00")
        except ValueError:
            self.tiempo_seg.setText("00")
        finally:
            self.tiempo_seg.textChanged.connect(self.validar_seg)
        self.capturar_cambio_tiempo()
    
    def capturar_cambio_tiempo(self):
        if not self.timer3.isActive():
            seg = int(self.tiempo_seg.text()) +  (int(self.tiempo_min.text()) * 60)
            if self.ventana_espectador.segundos + 1 != seg:
                self.cancelar.show()
                        
    def cambiar_estado_timer(self):
        if not self.ventana_espectador.timer.isActive(): # Cuando esta pausado (darle Play)
            self.seg = int(self.tiempo_seg.text()) +  (int(self.tiempo_min.text()) * 60)
            
            self.tiempo_min.setFocusPolicy(Qt.NoFocus)
            self.tiempo_seg.setFocusPolicy(Qt.NoFocus)
            self.tiempo_min.setReadOnly(True)
            self.tiempo_seg.setReadOnly(True)
            self.editar.hide()
            self.cancelar.hide()
            self.pausado.hide()
            
            self.ventana_espectador.ajuste_tiempo(self.seg)
            self.ventana_espectador.play_tiempo()
            self.timer3.start(1000)
            
        else: # Cuando esta activo (darle pause)
            self.editar.show()
            self.pausado.show()
            
            self.ventana_espectador.pause_tiempo()
            self.timer3.stop()
            
    def permitir_cambios(self):
        self.tiempo_min.setFocusPolicy(Qt.ClickFocus)
        self.tiempo_seg.setFocusPolicy(Qt.ClickFocus)
        self.tiempo_min.setReadOnly(False)
        self.tiempo_seg.setReadOnly(False)
        self.tiempo_seg.setFocus()
    
    def restaurar_tiempo(self):
        seg = self.ventana_espectador.segundos + 1
        if seg >= 0 :
            minutos = seg // 60
            segundos = seg % 60
        self.tiempo_min.setText(f"{minutos}")
        if segundos < 10:
            self.tiempo_seg.setText(f"0{segundos}")
        else:
            self.tiempo_seg.setText(f"{segundos}")
        self.cancelar.hide()
            
    def actualizar_contador_control(self):
        if self.seg >= 0:
            minutos = self.seg // 60
            segundos = self.seg % 60
            self.tiempo_min.setText(f"{minutos}")
            if segundos < 10:
                self.tiempo_seg.setText(f"0{segundos}")
            else:
                self.tiempo_seg.setText(f"{segundos}")
            self.seg -= 1
        else:
            self.timer3.stop() 
            self.editar.show()   
            self.pausado.show()     


if __name__ ==  "__main__":
    try:
        app = QApplication(sys.argv)
        espectador = MainWindow()
        control = ControlVentana(espectador)
        
        # Configurar referencias cruzadas
        espectador.control_window = control

        espectador.show()
        control.show()

        sys.exit(app.exec_())
        
    except Exception as e:
        print(e)