import sys
import time
import math
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDial
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QThread

from fuzzy_logic_system import get_simulation

class SpeedDial(QDial):
    def __init__(self, parent=None):
        super(SpeedDial, self).__init__(parent)
        self.speed = 0

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{self.speed} km/h")

    def setSpeed(self, speed):
        self.speed = speed
        self.setValue(speed)
        self.repaint()

class CruiseControlUI(QWidget, defaultSpeed):
    def __init__(self):
        super().__init__()
        self.defaultSpeed = self.defaultSpeed
        self.currentSpeed = self.defaultSpeed
        self.slopeValue = 0
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Cruise Control Simulation")

        self.speedDial = SpeedDial()
        self.speedDial.setMaximum(120)  # Max speed
        self.setSpeed(self.currentSpeed)
        self.speedDial.setDisabled(True)

        self.speedDial.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.speedDial.setMinimumSize(400, 400)  # Adjust size as needed

        layout.addWidget(self.speedDial)

        self.webView = QWebEngineView()
        self.loadLottieAnimation("http://localhost:8000/driving_car.json")
        layout.addWidget(self.webView)

        self.slopeLabel = QLabel("Slope: 0%")
        self.slopeLabel.setFont(QFont("Arial", 24))
        layout.addWidget(self.slopeLabel)

        self.increaseSlopeButton = QPushButton("Increase Slope")
        self.decreaseSlopeButton = QPushButton("Decrease Slope")
        layout.addWidget(self.increaseSlopeButton)
        layout.addWidget(self.decreaseSlopeButton)

        self.increaseSlopeButton.clicked.connect(self.increaseSlope)
        self.decreaseSlopeButton.clicked.connect(self.decreaseSlope)

        self.setLayout(layout)

    def setSpeed(self, speed):
        self.speedDial.setSpeed(speed)
    
    def loadLottieAnimation(self, file_path):
        html_content = """
        <!DOCTYPE html>
        <html>
        <body>
            <div id="lottie"></div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.7.3/lottie.min.js"></script>
            <script>
                var animation = bodymovin.loadAnimation({
                    container: document.getElementById('lottie'),
                    renderer: 'svg',
                    loop: true,
                    autoplay: true,
                    path: '""" + file_path + """'
                });
            </script>
        </body>
        </html>
        """
        self.webView.setHtml(html_content)

    def increaseSlope(self):
        self.slopeValue += 1
        self.updateSlopeAndSpeed()

    def decreaseSlope(self):
        self.slopeValue -= 1
        self.updateSlopeAndSpeed()

    def updateSlopeAndSpeed(self):
        self.currentSpeed = self.defaultSpeed - 2 * self.slopeValue
        self.setSpeed(self.currentSpeed)
        self.slopeLabel.setText(f"Slope: {self.slopeValue}%")
        self.adjustAnimationSpeed(self.currentSpeed / self.defaultSpeed)
        rotation_angle = self.calculateRotationAngle(self.slopeValue)
        self.rotateAnimation(rotation_angle)

    def rotateAnimation(self, angle):
        js_code = f"document.getElementById('lottie').style.transform = 'rotate({angle}deg)';"
        self.webView.page().runJavaScript(js_code)
    
    def calculateRotationAngle(self, slope):
        # Example: 1 degree of rotation for each 1% slope change
        return -slope

    def adjustAnimationSpeed(self, speedFactor):
        js_code = f"animation.setSpeed({speedFactor});"
        self.webView.page().runJavaScript(js_code)

def run(cruiseControlUI):
    simulation = get_simulation();

    G = 9.8
    initial_slope = 7
    initial_speed = 100
    target_speed = 90

    for _ in range(20):
        # x = True
        
        initial_speed -= math.sin(initial_slope)*G
        #print("eğimdeki hızz:", initial_speed)
        simulation.input['speed'] = initial_speed-target_speed

        simulation.compute()
        print("control signal:",simulation.output['control_signal'])
        initial_speed += simulation.output['control_signal']
        print("Input Speed:", initial_speed)
        time.sleep(1)

        speed_as_int = int(initial_speed)
        cruiseControlUI.setSpeed(speed_as_int)

        # Print the results
        print("Input Speed:", initial_speed)
        print("Control Signal:", simulation.output['control_signal'])    

def main():
    app = QApplication(sys.argv)
    cruiseControlUI = CruiseControlUI(120)
    cruiseControlUI.show()

    time.sleep(3)

    thread = threading.Thread(target=run, args=[cruiseControlUI])
    thread.start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()