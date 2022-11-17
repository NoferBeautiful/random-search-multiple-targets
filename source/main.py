from PyQt6.QtWidgets import QApplication, QGraphicsScene, QSlider
from PyQt6 import uic
from PyQt6.QtCore import QTimer
import sys
import numpy as np

from grid import Grid
from point import Point
from ui import UI
import env

if __name__ == "__main__":
    UI = UI()
    UI.start_exe()
