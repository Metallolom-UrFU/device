import RPi.GPIO as GPIO
import time

class Shelf:
    def __init__(self, shelf_id: str, lock_pin: int, door_pin: int):
        self.id = shelf_id
        self.lock_pin = lock_pin
        self.door_pin = door_pin

        GPIO.setup(self.lock_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def unlock(self):
        """
        Подать импульс 0.2 секунды на замок
        """
        GPIO.output(self.lock_pin, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(self.lock_pin, GPIO.LOW)

    def is_closed(self) -> bool:
        """
        True — дверь закрыта
        False — дверь открыта
        """
        return GPIO.input(self.door_pin) == GPIO.HIGH