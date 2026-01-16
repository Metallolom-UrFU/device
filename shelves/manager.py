import yaml
import RPi.GPIO as GPIO
import atexit

from .shelf import Shelf


class ShelfManager:
    def __init__(self, config_path: str):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.shelves: dict[str, Shelf] = {}

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        for s in config.get("shelves", []):
            shelf = Shelf(
                shelf_id=s["id"],
                lock_pin=s["lock_pin"],
                door_pin=s["door_pin"]
            )
            self.shelves[shelf.id] = shelf

        atexit.register(self.cleanup)

    def get(self, shelf_id: str) -> Shelf | None:
        return self.shelves.get(shelf_id)

    def all(self):
        return list(self.shelves.values())

    def cleanup(self):
        GPIO.cleanup()
