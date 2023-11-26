import cv2
from gpiozero import Button
from gpiozero import LED
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
    val, _ = qcd.decode(frame, a)

    return frame, val


# detect(cv2.imread('kod.jpg'))


button = Button(17)
led = LED(27)

while True:
    button.wait_for_press()
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('test.png', gray)
    webcam.release()
    print(detect(gray))


