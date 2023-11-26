import cv2
from gpiozero import Button
from gpiozero import LED
from signal import pause
from time import sleep
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
    _, decoded_info, decoded_type, corners = bardet.detectAndDecode(frame)
    return frame, decoded_info

#funkcja czytajaca kod qr
def read_qrcode(frame):

    qcd = cv2.QRCodeDetector()
    det, a, b = qcd.detectAndDecode(frame)

    return frame, det


# detect(cv2.imread('kod.jpg'))


button = Button(17)
led = LED(27)
led.on()
sleep(1)
led.off()
def onguzik():
    led.on()

def offguzik():
    led.off()
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    cv2.imwrite('test.png', frame)
    webcam.release()
    print(detect(frame))

button.when_pressed = onguzik
button.when_released = offguzik
pause()



