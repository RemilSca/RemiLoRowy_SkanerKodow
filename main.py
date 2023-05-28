import cv2
import kivy
kivy.require('2.2.0') # replace with your current kivy version !
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import lora

#Funkcja ktora decyduje czy czytamy kod kreskowy czy qr
#Jesli funkcja szukania kodu kreskowego nic nie znajdzie to wywolywana jest funkcja szukania qr
#jesli i ona nic nie znajdzie to zwracamy None
def detect(frame):
    frame, code = read_barcode(frame)
    if code:
        return frame, code
    else:
        frame, code = read_qrcode(frame)
        if code:
            return frame, code
        else:
            return frame, None


#funkcja czytajaca kod kreskowego
def read_barcode(frame):
    bardet = cv2.barcode.BarcodeDetector()
    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(frame)
    return frame, decoded_info

#funkcja czytajaca kod qr
def read_qrcode(frame):

    qcd = cv2.QRCodeDetector()
    det, a, b = qcd.detectAndDecode(frame)
    val, _ = qcd.decode(frame, a)

    return frame, val


#kawałek kodu ktory formatuje wyglad aplikacji

Builder.load_string('''
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
''')

#klasa odpowiedzialna za działanie guzika capture

class CameraClick(BoxLayout):
    def capture(self):
        camera = self.ids['camera']
        #camera.export_to_png("temp.png")
        frame = cv2.imread('qr.jpg')
        frame, code = detect(frame)
        cv2.imwrite("temp.jpg", frame)
        print(code)
        lora.send(code)

#klasa aplikacji

class MyApp(App):

    def build(self):
        return CameraClick()

#Glowna petla programu

if __name__ == '__main__':
    MyApp().run()