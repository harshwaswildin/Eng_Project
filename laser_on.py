
import pyfirmata as pf
import datetime

board = pf.Arduino("COM5")
it = pf.util.Iterator(board)  
it.start()

laser = board.get_pin('d:8:o')
ldr = board.get_pin('a:0:i')
buzzer = board.get_pin('d:11:o')  
light_threshold = 0.1


while True:
    laser.write(1)
    ldr_output = ldr.read()
    if (ldr_output or 0)>=light_threshold:
        buzzer.write(1)
    else:
        buzzer.write(0)
    #print(ldr.read())

def off():
    buzzer.write(0)
    laser.write(0)