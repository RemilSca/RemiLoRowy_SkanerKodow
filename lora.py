import serial
import time

port = '/dev/ttyUSB0'
appkey = '592D888ADE8D3EB039F1CFC0673639D5'

#Funkcja obslugujaca wysylanie i odbieranie danych portem usb
def write_read(x, lora):

    lora.write(bytes(x, 'utf-8'))
    time.sleep(0.5)
    data = lora.readline()
    data = data.decode()

    return data

def start():
    lora = serial.Serial(port=port, baudrate=9600, timeout=None)
    x = write_read(f'AT+KEY=APPKEY,"{appkey}"', lora)
    time.sleep(1)
    print(x)
    x = write_read(f'AT+MODE=LWOTAA', lora)
    time.sleep(1)
    print(x)
    x = write_read(f'AT+JOIN', lora)
    time.sleep(15)
    print(x)
    send('11')
#Funkcja wysylajaca dane przez lora, numer portu usb bedzie sie zmieniac wiec trzeba zaimplementowac jakis wykrywacz
def send(d):
    lora = serial.Serial(port=port, baudrate=9600, timeout=0.1)
    x = write_read(f'AT+MSGHEX={d}\n', lora)

start()