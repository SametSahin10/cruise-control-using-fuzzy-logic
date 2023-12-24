import sys
from PyQt5.QtWidgets import QApplication
from simulation import Simulation
from simulation_ui import SimulationUI

def main():
    app = QApplication(sys.argv)

    initialSpeed = 80
    target_speed = 100
    initialSlope = 3

    simulationUI = SimulationUI(initialSpeed=60, initialSlope=initialSlope)
    simulation = Simulation(
        initial_speed=initialSpeed,
        target_speed=target_speed,
        initial_slope=initialSlope
    )

    simulation.set_speed_in_ui.connect(simulationUI.set_speed)
    simulationUI.set_slope_in_simulation.connect(simulation.set_slope)

    simulationUI.show()
    simulation.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

