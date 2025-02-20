from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from plyer import camera
from PIL import Image
from pyzbar.pyzbar import decode
import pandas as pd
import os
from datetime import datetime
from kivy.utils import platform

# Solicitar permisos de cámara en Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])

# Nombre del archivo Excel en Android
EXCEL_FILE = "/storage/emulated/0/registro_cajas.xlsx"

# Crear el archivo Excel si no existe
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Fecha", "Código de Barras"])
    df.to_excel(EXCEL_FILE, index=False)

def guardar_en_excel(codigo_barras):
    """ Guarda el código escaneado en un archivo Excel """
    df = pd.read_excel(EXCEL_FILE)
    nueva_fila = pd.DataFrame([[datetime.now(), codigo_barras]], columns=["Fecha", "Código de Barras"])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)
    print(f"Guardado: {codigo_barras}")

class ScanScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.result_label = Label(text="Presiona el botón para tomar una foto...", size_hint_y=0.2)
        self.add_widget(self.result_label)

        self.capture_button = Button(text="Capturar Imagen", size_hint_y=0.2, on_press=self.capturar_imagen)
        self.add_widget(self.capture_button)

        self.save_button = Button(text="Guardar Código", size_hint_y=0.2, on_press=self.guardar_codigo)
        self.add_widget(self.save_button)

    def capturar_imagen(self, instance):
        self.ruta_imagen = '/storage/emulated/0/DCIM/codigo_barras.jpg'
        camera.take_picture(self.ruta_imagen, self.procesar_imagen)

    def procesar_imagen(self, ruta_imagen):
        self.result_label.text = "Procesando imagen..."
        image = Image.open(ruta_imagen)
        codes = decode(image)
        
        if codes:
            self.codigo_barras = codes[0].data.decode("utf-8")
            self.result_label.text = f"Código: {self.codigo_barras}"
        else:
            self.result_label.text = "No se detectó ningún código de barras."

    def guardar_codigo(self, instance):
        if hasattr(self, 'codigo_barras'):
            guardar_en_excel(self.codigo_barras)
            self.result_label.text = "Código guardado en Excel."

class BarcodeScannerApp(App):
    def build(self):
        return ScanScreen()

if __name__ == "__main__":
    BarcodeScannerApp().run()