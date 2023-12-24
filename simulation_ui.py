import math
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QDial
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import pyqtSignal

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

class SimulationUI(QWidget):
    set_slope_in_simulation = pyqtSignal(int)

    def __init__(self, initialSpeed, initialSlope):
        super().__init__()
        self.initialSpeed = initialSpeed
        self.currentSpeed = initialSpeed
        self.slope = initialSlope
        self.initUI()
        self.slopeLabel.setText(f"Slope: {self.slope}%")
        
    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle("Cruise Control Simulation")

        self.speedDial = SpeedDial()
        self.speedDial.setMaximum(120)  # Max speed
        self.set_speed(self.currentSpeed)
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

    def set_speed(self, speed):
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
        self.slope += 1
        self.set_slope_in_simulation.emit(self.slope)
        self.updateSlopeAndSpeed()

    def decreaseSlope(self):
        self.slope -= 1
        self.set_slope_in_simulation.emit(self.slope)
        self.updateSlopeAndSpeed()

    def updateSlopeAndSpeed(self):
        G = 9.8

        print("Updating slope and speed...")
        # print(f"Egimin etkisi: ${math.sin(self.slope) * G}");
        # self.currentSpeed -= math.sin(self.slope) * G
        print(f"New speed: ${self.currentSpeed}")

        # self.set_speed(self.currentSpeed)
        self.slopeLabel.setText(f"Slope: {self.slope}%")

        print(f"Setting animation speed to: ${self.currentSpeed / self.initialSpeed}")

        self.adjustAnimationSpeed(self.currentSpeed / self.initialSpeed)
        rotation_angle = self.calculateRotationAngle(self.slope)
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