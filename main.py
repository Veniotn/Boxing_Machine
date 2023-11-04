import RPi.GPIO as GPIO
from hx711 import HX711
from Classes.boxing_machine import BoxingMachine


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    boxing_machine = BoxingMachine(HX711(dout_pin=6, pd_sck_pin=5))
    boxing_machine.run()
