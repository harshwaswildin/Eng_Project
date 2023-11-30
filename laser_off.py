
import pyfirmata as pf
import time 
import subprocess as s

board = pf.Arduino("COM5")
board.reset()
board.transport.close()
it = pf.util.Iterator(board)  
it.start()

laser = board.get_pin('d:8:o')
ldr = board.get_pin('a:0:i')
buzzer = board.get_pin('d:11:o')  

buzzer.write(0)
laser.write(0)