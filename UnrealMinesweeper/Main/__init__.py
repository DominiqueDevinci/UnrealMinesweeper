import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ImageLoader import ImageLoader
from BoardController import BoardController
from Util import choose
from MinesweeperGUI import MinesweeperGUI

import Solver



       
   

def main():
   app = QApplication(sys.argv)
   
   view = MinesweeperGUI()
   boardController=BoardController(view, 10, 10, 20)
   view.initBoard(10, 10, boardController)

   view.show()
   sys.exit(app.exec_())
    
if __name__ == '__main__':
   main()