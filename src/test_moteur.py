#! /usr/bin/env python3

import controller
import time

def move_forward(duration=5.0, speed=-50):
    """
    Avance le robot en faisant tourner les deux moteurs à la même vitesse.

    Parameters:
    - duration (float): Temps pendant lequel le robot avance (en secondes).
    - speed (int): Vitesse des moteurs (valeur positive pour avancer).
    """
    # Initialiser le contrôleur
    c = controller.Controller()
    c.set_motor_shutdown_timeout(duration)
    c.standby()
    
    # Définir la vitesse pour avancer (les deux moteurs en avant)
    c.set_motor_speed(speed, int(speed/2))
    
    # Attendre pendant la durée spécifiée
    time.sleep(duration)
    
    # Arrêter les moteurs
    c.standby()
    print(f"Le robot a avancé pendant {duration} secondes avec une vitesse de {speed}.")

if __name__ == "__main__":
    try:
        move_forward()  # Appel par défaut pour avancer 5 seconde à une vitesse de 50
    except Exception as e:
        print(f"Erreur : {e}")
