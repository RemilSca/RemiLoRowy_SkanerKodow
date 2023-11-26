import cv2
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

try:
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    print(detect(frame))
except: print('kamerka nie dziala')

