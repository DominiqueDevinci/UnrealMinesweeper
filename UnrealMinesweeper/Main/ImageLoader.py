from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ImageLoader:
    iconFlag=None 
    iconMine=None
    
    
    @staticmethod
    def init():
        ImageLoader.iconFlag=QIcon(QPixmap("flag.png"))
        ImageLoader.iconMine=QIcon(QPixmap("mine.png"))
        