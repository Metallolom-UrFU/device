import yaml
import RPi.GPIO as GPIO
import atexit

from .shelf import Shelf


class ShelfManager:
    def __init__(self, config_path: str):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.shelves: list[Shelf] = []

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        for s in config.get("shelves", []):
            shelf = Shelf(
                shelf_id=s["id"],
                lock_pin=s["lock_pin"],
                door_pin=s["door_pin"]
            )
            self.shelves.append(shelf)

        atexit.register(self.cleanup)

    def get_free_shelf(self) -> Shelf | None:
        for shelf in self.shelves:
            if shelf.is_closed() and not shelf.busy:
                shelf.busy = True
                return shelf
        return None

    def release_shelf(self, shelf: Shelf):
        shelf.busy = False

    def cleanup(self):
        GPIO.cleanup()
