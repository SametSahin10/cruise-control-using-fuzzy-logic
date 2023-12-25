import math
import time
from re import T
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class Simulation(QThread):
    set_speed_in_ui = pyqtSignal(int)

    def __init__(self, initial_speed, target_speed, initial_slope):
        super().__init__()
        self.current_speed = initial_speed
        self.target_speed = target_speed
        self.slope = initial_slope


    def set_slope(self, slope):
        self.slope = slope

    def get_simulation(self):
        # Create fuzzy variables
        speed = ctrl.Antecedent(np.arange(-25, 25, 1), 'speed')
        control_signal = ctrl.Consequent(np.arange(-15, 16, 1), 'control_signal')

        # Define membership functions
        speed['TooSlow'] = fuzz.trapmf(speed.universe, [-25,-20,-15,-10])
        speed['Slow'] = fuzz.trapmf(speed.universe, [-15,-10,-5,-0])
        speed['Normal'] = fuzz.trimf(speed.universe, [-5,0,5])
        speed['Fast'] = fuzz.trapmf(speed.universe, [0,5,10,15])
        speed['VeryFast'] = fuzz.trapmf(speed.universe, [10,15,20,25])

        control_signal['Decrease'] = fuzz.trimf(control_signal.universe, [-9, -6, -3])
        control_signal['DecreaseSlightly'] = fuzz.trimf(control_signal.universe, [-6, -3, 0])
        control_signal['Maintain'] = fuzz.trimf(control_signal.universe, [-3, 0, 3])
        control_signal['IncreaseSlightly'] = fuzz.trimf(control_signal.universe, [0, 3, 6])
        control_signal['Increase'] = fuzz.trimf(control_signal.universe, [3, 6, 9])

        # Define rules
        rule1 = ctrl.Rule(speed['TooSlow'], control_signal['Increase'])
        rule2 = ctrl.Rule(speed['Slow'], control_signal['IncreaseSlightly'])
        rule3 = ctrl.Rule(speed['Normal'], control_signal['Maintain'])
        rule4 = ctrl.Rule(speed['Fast'], control_signal['DecreaseSlightly'])
        rule5 = ctrl.Rule(speed['VeryFast'], control_signal['Decrease'])

        # Create the control system
        speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        speed_stabilization = ctrl.ControlSystemSimulation(speed_ctrl)

        return speed_stabilization
    
    def run(self):
        self.runSimulation()
        
    def runSimulation(self):
        simulation = self.get_simulation();

        G = 9.8

        while True:

            slope_in_radians = math.radians(self.slope)

            self.current_speed -= math.sin(slope_in_radians) * G
            print(f"Egimden kaybedilen hiz: ${math.sin(slope_in_radians) * G}")
            simulation.input['speed'] = self.current_speed - self.target_speed

            print(f"Initial speed: ${self.current_speed}")

            simulation.compute()
            self.current_speed += simulation.output['control_signal']
            print("Output speed:", self.current_speed)
            time.sleep(1)

            speed_as_int = int(self.current_speed)
            self.set_speed_in_ui.emit(speed_as_int)