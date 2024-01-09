import cv2
from gpiozero import Button
from gpiozero import LED
from signal import pause
from time import sleep
import lora


with open('db.txt', 'r') as f:
    baza = eval(f.read())


#Funkcja ktora decyduje czy czytamy kod kreskowy czy qr
#Jesli funkcja szukania kodu kreskowego nic nie znajdzie to wywolywana jest funkcja szukania qr
#jesli i ona nic nie znajdzie to zwracamy None
def detect(frame):
    code = read_barcode(frame)
    if code:
        return code
    else:
        code = read_qrcode(frame)
        if code:
            return code
        else:
            return None


#funkcja czytajaca kod kreskowego
def read_barcode(frame):
    bardet = cv2.barcode.BarcodeDetector()
    decoded_info, decoded_type, corners = bardet.detectAndDecode(frame)
    return decoded_info

#funkcja czytajaca kod qr
def read_qrcode(frame):

    qcd = cv2.QRCodeDetector()
    det, a, b = qcd.detectAndDecode(frame)
    return det


# detect(cv2.imread('kod.jpg'))


button = Button(17)
ledy = LED(27)
ledz = LED(23)
ledc = LED(24)
ledy.on()
ledz.on()
ledc.on()




def onguzik():
    ledy.on()

def offguzik():
    ledy.off()
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    cv2.imwrite('test.png', frame)
    webcam.release()
    result = detect(frame)
    if result is not None:
        if result in baza.values():
            found = list(baza.keys())[list(baza.values()).index(result)]
            lora.send(found)
            ledz.on()
            sleep(0.25)
            ledz.off()
        else:
            for i in range(2):
                ledc.on()
                sleep(0.25)
                ledc.off()
                sleep(0.1)
    else:
        ledc.on()
        sleep(0.25)
        ledc.off()

button.when_pressed = onguzik
button.when_released = offguzik
lora.start()
ledy.off()
ledz.off()
ledc.off()
pause()



