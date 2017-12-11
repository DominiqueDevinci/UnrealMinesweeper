import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController
from Util import choose
from MinesweeperGUI import MinesweeperGUI
from QPushButtonCustom import QPushButtonCustom

import Solver



       
   

def main():
   app = QApplication(sys.argv)   
   view = MinesweeperGUI()
   view.newGame(9, 9, 10)
   view.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()