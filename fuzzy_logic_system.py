from re import T
#MERT
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def get_simulation():
    # Create fuzzy variables
    speed = ctrl.Antecedent(np.arange(-25, 25, 1), 'speed')
    control_signal = ctrl.Consequent(np.arange(-15, 16, 1), 'control_signal')

    # Define membership functions
    speed['TooSlow'] = fuzz.trapmf(speed.universe, [-25,-20,-15,-10])
    speed['Slow'] = fuzz.trapmf(speed.universe, [-15,-10,-5,-5])
    speed['Normal'] = fuzz.trimf(speed.universe, [-5,0,5])
    speed['Fast'] = fuzz.trapmf(speed.universe, [5,5,10,15])
    speed['VeryFast'] = fuzz.trapmf(speed.universe, [10,15,20,25])

    control_signal['Decrease'] = fuzz.trimf(control_signal.universe, [-15, -10, -5])
    control_signal['DecreaseSlightly'] = fuzz.trimf(control_signal.universe, [-10, -5, -0])
    control_signal['Maintain'] = fuzz.trimf(control_signal.universe, [-5, 0, 5])
    control_signal['IncreaseSlightly'] = fuzz.trimf(control_signal.universe, [0, 5, 10])
    control_signal['Increase'] = fuzz.trimf(control_signal.universe, [5, 10, 15])

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