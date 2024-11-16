import os
from src.tools.controller import Controller

is_pros = lambda: os.getenv('ENV') == 'PROD'

MAX_SPEED = 100

class Robot:
    controller: Controller

    def __init__(self):
        if is_pros():
            self.controller = Controller()
            self.controller.standby()
    

    def move(self, righ: int, left: int):
        if is_pros():
            self.controller.set_motor_speed(left, righ)
        print(f"[robot] {left} {righ}")
    
    def stop(self):
        if is_pros():
            self.controller.standby()
        print("[robot] stop")


robot = Robot()
