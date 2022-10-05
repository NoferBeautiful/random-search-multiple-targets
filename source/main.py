from PyQt6.QtWidgets import QApplication, QWidget, QGraphicsScene, QGraphicsItem
from PyQt6 import uic
from PyQt6.QtGui import QBrush, QColor, QPen
from PyQt6.QtCore import Qt, QTimer
import sys


from grid import Grid
from point import Point


def search(point, grid, canvas=None):
    point.move()
    found_x = False
    found_y = False
    """
    while True:
        check = grid.check(*point.get_point())
        if check == 3:
            break
        elif check == 2 and not found_y:
            point.change_y_distribution("end")
            found_y = True
        elif check == 3 and not found_x:
            point.change_x_distribution("end")
            found_x = True
        point.move()
        print(1)
    """


app = QApplication(sys.argv)
window = uic.loadUi("../wdw.ui")


view = window.scene

startButton = window.startButton

scene = QGraphicsScene()

point = Point()
point.appear(scene)
grid = Grid(500, 500, 10, 10)

grid.draw(scene)
point.draw(scene)

view.setSceneRect(0, 0, 500, 500)
view.setScene(scene)

timer = QTimer()
timer.timeout.connect(point.move)
timer.start(10)

window.show()

app.exec()

#search(point, grid)
