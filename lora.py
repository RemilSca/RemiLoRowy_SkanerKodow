import serial
import time



#Funkcja obslugujaca wysylanie i odbieranie danych portem usb
def write_read(x, lora):

    lora.write(bytes(x, 'utf-8'))
    time.sleep(0.1)
    data = lora.readline()
    data = data.decode()

    return data

#Funkcja wysylajaca dane przez lora, numer portu usb bedzie sie zmieniac wiec trzeba zaimplementowac jakis wykrywacz
def send(d):
    lora = serial.Serial(port='COM5', baudrate=9600, timeout=0.1)
    x = write_read('AT+MODE=TEST\n', lora)
    print(x)
    x = write_read(f'AT+TEST=TXLRSTR,"{d}"\n', lora)
    print(x)

