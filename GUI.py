# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 07:14:57 2021

@author: Bryant
"""

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, \
                            QMainWindow, QVBoxLayout, QHBoxLayout, \
                            QWidget, QFileDialog, QLineEdit
from datetime import datetime
                            
from PyQt5.QtGui import QPixmap
from PIL import Image
from ImageEncryption import ImageEncryption


'''
The following class is used for the output of each mode of operation,
and will be a simple window with the mode of operation in the title and the 
encrypted image.

5 instances of this class will be used in total
'''
class outputWindow(QMainWindow):
    
    def __init__(self, encryptionMode, parent=None):
        super(outputWindow, self).__init__(parent)
        
        self.setWindowTitle(f'{encryptionMode} Encryption Output')
        
        self.imageLabel = QLabel(self)
        #The output image file will be named as the mode of operation to
        #make it easier to find
        self.image = QPixmap(f'{encryptionMode}.png')
        
        if self.image.width() > 600:
            self.image.scaledToWidth(600)
        self.imageLabel.setPixmap(self.image)
        
        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        self.show()


'''
The main QUI window will consist of two portions, the left portion will be
a button that opens a file explorer and allows the user to select an image file
to encrypt. On the Right side there will 6 buttons along with key and initial 
value text fields (except for the ECB button) which will encrypt the image in 
either ECB, CBC, OFB, CFB, CTR mode; or all 5.
'''
class GUI(QMainWindow):
    
    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        
        #In order for the output windows to be persistent they must be 
        #initialized along with the main window but left empty until 
        #the encryption has finished
        self.ECBWindow = None
        self.CBCWindow = None
        self.OFBWindow = None
        self.CFBWindow = None
        self.CTRWindow = None
        
        self.setWindowTitle("AES Image Encryption")
        
        uploadFileBtn = QPushButton("Open Image File")
        self.inputImageLabel = QLabel('Original Image')
        
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(uploadFileBtn)
        leftLayout.addWidget(self.inputImageLabel)
        
        self.createEncryptionOptionButtons()
        
        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.addLayout(self.rightLayout)
        
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        
        
        uploadFileBtn.clicked.connect(self.openFilePicker)
        self.AllButton.clicked.connect(self.encryptAll)
        self.ECBButton.clicked.connect(self.encryptECB)
        self.CBCButton.clicked.connect(self.encryptCBC)
        self.OFBButton.clicked.connect(self.encryptOFB)
        self.CFBButton.clicked.connect(self.encryptCFB)
        self.CTRButton.clicked.connect(self.encryptCTR)
        
        self.resize(800,600)
        self.show()
    
    '''
    The following function will create the buttons and text fields for each mode
    of operation along with a button to encrypt in all five using the same key 
    and initial value. This will be the right side of the GUI window.
    
    The key and IV values entered by the user are expected to be a hexadecimal 
    value that is 32 hexadecimal bits in length. The text fields will limit
    the users input to 32 characters.
    
    This function does not link the buttons to seperate functions that will 
    perform the encryption.
    '''
    def createEncryptionOptionButtons(self):
        textBoxWidth = 200
        buttonWidth = 100
        
        self.AllButton = QPushButton("Encrypt All")
        self.AllKey = QLineEdit("Key")
        self.AllIV = QLineEdit("Initial Value")
        self.AllButton.setFixedWidth(buttonWidth)
        self.AllKey.setFixedWidth(textBoxWidth)
        self.AllIV.setFixedWidth(textBoxWidth)
        self.AllKey.setMaxLength(32)
        self.AllIV.setMaxLength(32)
        
        self.AllVerticalBox = QVBoxLayout()
        self.AllHorizantalBox = QHBoxLayout()
        self.AllVerticalBox.addWidget(self.AllKey)
        self.AllVerticalBox.addWidget(self.AllIV)
        
        self.AllHorizantalBox.addLayout(self.AllVerticalBox)
        self.AllHorizantalBox.addWidget(self.AllButton)
        
        
        self.ECBButton = QPushButton("Encrypt In ECB")
        self.ECBKey = QLineEdit("Key")
        self.ECBButton.setFixedWidth(buttonWidth)
        self.ECBKey.setFixedWidth(textBoxWidth)
        self.ECBKey.setMaxLength(32)
        
        
        self.ECBLayoutBox = QHBoxLayout()
        self.ECBLayoutBox.addWidget(self.ECBKey)
        self.ECBLayoutBox.addWidget(self.ECBButton)
        
        
        self.CBCButton = QPushButton("Encrypt In CBC")
        self.CBCKey = QLineEdit("Key")
        self.CBCIV = QLineEdit("Initial Value")
        self.CBCButton.setFixedWidth(buttonWidth)
        self.CBCKey.setFixedWidth(textBoxWidth)
        self.CBCIV.setFixedWidth(textBoxWidth)
        self.CBCKey.setMaxLength(32)
        self.CBCIV.setMaxLength(32)
        
        self.CBCVerticalBox = QVBoxLayout()
        self.CBCHorizantalBox = QHBoxLayout()
        self.CBCVerticalBox.addWidget(self.CBCKey)
        self.CBCVerticalBox.addWidget(self.CBCIV)
        
        self.CBCHorizantalBox.addLayout(self.CBCVerticalBox)
        self.CBCHorizantalBox.addWidget(self.CBCButton)
        
        
        self.OFBButton = QPushButton("Encrypt In OFB")
        self.OFBKey = QLineEdit("Key")
        self.OFBIV = QLineEdit("Initial Value")
        self.OFBButton.setFixedWidth(buttonWidth)
        self.OFBKey.setFixedWidth(textBoxWidth)
        self.OFBIV.setFixedWidth(textBoxWidth)
        self.OFBKey.setMaxLength(32)
        self.OFBIV.setMaxLength(32)
        
        self.OFBVerticalBox = QVBoxLayout()
        self.OFBHorizantalBox = QHBoxLayout()
        self.OFBVerticalBox.addWidget(self.OFBKey)
        self.OFBVerticalBox.addWidget(self.OFBIV)
        
        self.OFBHorizantalBox.addLayout(self.OFBVerticalBox)
        self.OFBHorizantalBox.addWidget(self.OFBButton)
        
        
        self.CFBButton = QPushButton("Encrypt In CFB")
        self.CFBKey = QLineEdit("Key")
        self.CFBIV = QLineEdit("Initial Value")
        self.CFBButton.setFixedWidth(buttonWidth)
        self.CFBKey.setFixedWidth(textBoxWidth)
        self.CFBIV.setFixedWidth(textBoxWidth)
        self.CFBKey.setMaxLength(32)
        self.CFBIV.setMaxLength(32)
        
        self.CFBVerticalBox = QVBoxLayout()
        self.CFBHorizantalBox = QHBoxLayout()
        self.CFBVerticalBox.addWidget(self.CFBKey)
        self.CFBVerticalBox.addWidget(self.CFBIV)
        
        self.CFBHorizantalBox.addLayout(self.CFBVerticalBox)
        self.CFBHorizantalBox.addWidget(self.CFBButton)
        
        
        self.CTRButton = QPushButton("Encrypt In CTR")
        self.CTRKey = QLineEdit("Key")
        self.CTRIV = QLineEdit("Initial Value")
        self.CTRButton.setFixedWidth(buttonWidth)
        self.CTRKey.setFixedWidth(textBoxWidth)
        self.CTRIV.setFixedWidth(textBoxWidth)
        self.CTRKey.setMaxLength(32)
        self.CTRIV.setMaxLength(32)
        
        self.CTRVerticalBox = QVBoxLayout()
        self.CTRHorizantalBox = QHBoxLayout()
        self.CTRVerticalBox.addWidget(self.CTRKey)
        self.CTRVerticalBox.addWidget(self.CTRIV)
        
        self.CTRHorizantalBox.addLayout(self.CTRVerticalBox)
        self.CTRHorizantalBox.addWidget(self.CTRButton)
        
        
        self.rightLayout = QVBoxLayout()
        self.rightLayout.addLayout(self.AllHorizantalBox)
        self.rightLayout.addLayout(self.ECBLayoutBox)
        self.rightLayout.addLayout(self.CBCHorizantalBox)
        self.rightLayout.addLayout(self.OFBHorizantalBox)
        self.rightLayout.addLayout(self.CFBHorizantalBox)
        self.rightLayout.addLayout(self.CTRHorizantalBox)
        
    
    '''
    When the 'encrypt in ECB' button is clicked, the following funtion is called,
    it will retrieve the key value entered by the user and verifies that it is 
    32 characters long.
    If it is valid, the encryption function is called using the key while also
    determining how long it takes to run the encryption.
    '''
    def encryptECB(self):
        imageEncrypt = ImageEncryption(self.img)
        key = self.ECBKey.text()
        if len(key) == 32:
            start = datetime.now()
            imageEncrypt.encryptInECB(key)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in ECB {elapsedTime}')
            self.openECBWindow()
        else:
            print("Invalid key provided")
        
    '''
    When the 'encrypt in CBC' button is clicked, the following funtion is called,
    it will retrieve the key and IV value entered by the user and verifies that it is 
    32 characters long.
    If it is valid, the encryption function is called using the key while also
    determining how long it takes to run the encryption.
    '''
    def encryptCBC(self):
        imageEncrypt = ImageEncryption(self.img)
        key = self.CBCKey.text()
        IV = self.CBCIV.text()
        if (len(key) == 32) & (len(IV) == 32):
            start = datetime.now()
            imageEncrypt.encryptInCBC(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in CBC {elapsedTime}')
            self.openCBCWindow()
        else:
            print("Invalid key of IV provided")
            
    
    '''
    When the 'encrypt in OFB' button is clicked, the following funtion is called,
    it will retrieve the key and IV value entered by the user and verifies that it is 
    32 characters long.
    If it is valid, the encryption function is called using the key while also
    determining how long it takes to run the encryption.
    '''
    def encryptOFB(self):
        imageEncrypt = ImageEncryption(self.img)
        key = self.OFBKey.text()
        IV = self.OFBIV.text()
        if (len(key) == 32) & (len(IV) == 32):
            start = datetime.now()
            imageEncrypt.encryptInOFB(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in OFB {elapsedTime}')
            self.openOFBWindow()
        else:
            print("Invalid key or IV provided")
        
        
    '''
    When the 'encrypt in CFB' button is clicked, the following funtion is called,
    it will retrieve the key and IV value entered by the user and verifies that it is 
    32 characters long.
    If it is valid, the encryption function is called using the key while also
    determining how long it takes to run the encryption.
    '''
    def encryptCFB(self):
        imageEncrypt = ImageEncryption(self.img)
        key = self.CFBKey.text()
        IV = self.CFBIV.text()
        if (len(key) == 32) & (len(IV) == 32):
            start = datetime.now()
            imageEncrypt.encryptInCFB(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in CFB {elapsedTime}')
            self.openCFBWindow()
        else:
            print("Invalid key or IV provided")
        
        
    '''
    When the 'encrypt in CTR' button is clicked, the following funtion is called,
    it will retrieve the key and IV value entered by the user and verifies that it is 
    32 characters long.
    If it is valid, the encryption function is called using the key while also
    determining how long it takes to run the encryption.
    '''    
    def encryptCTR(self):
        imageEncrypt = ImageEncryption(self.img)
        key = self.CTRKey.text()
        IV = self.CTRIV.text()
        if (len(key) == 32) & (len(IV) == 32):
            if len(IV) > 24:
                IV = IV[:24]
            start = datetime.now()
            imageEncrypt.encryptInCTR(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in CTR {elapsedTime}')
            self.openCTRWindow()
        else:
            print("Invalid key or IV provided")
            
    
    '''
    When the 'Encrypt All' button is clicked,  the following function is called
    it will retrieve the key and IV values entered by the user and verifies that
    they are 32 characters long.
    If it is valid it will call all 5 encryption functions using the key and IV 
    values given by the user.
    '''
    def encryptAll(self):
        imageEncrypt = ImageEncryption(self.img)
        key = self.AllKey.text()
        IV = self.AllIV.text()
        if (len(key) == 32) & (len(IV) == 32):
            CTRIV = IV[:24]
        
            start = datetime.now()
            imageEncrypt.encryptInECB(key)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in ECB {elapsedTime}')
            
            start = datetime.now()
            imageEncrypt.encryptInCBC(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in CBC {elapsedTime}')
            
            start = datetime.now()
            imageEncrypt.encryptInOFB(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in OFB {elapsedTime}')
            
            start = datetime.now()
            imageEncrypt.encryptInCFB(key, IV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in CFB {elapsedTime}')
            
            start = datetime.now()
            imageEncrypt.encryptInCTR(key, CTRIV)
            end = datetime.now()
            elapsedTime = end-start
            print(f'Time to encrypt in CTR {elapsedTime}')
            
            
            self.openECBWindow()
            self.openCBCWindow()
            self.openOFBWindow()
            self.openCFBWindow()
            self.openCTRWindow()
        else:
            print("Invalid key or IV provided")
        
    
    '''
    The following functions will initialize the output window for the specified
    mode of operation and then open the window by loading the png file of the same
    name (e.g. ECB.png for the ECB output window)
    '''
    def openECBWindow(self):
        if self.ECBWindow is None:
            self.ECBWindow = outputWindow("ECB")
        self.ECBWindow.show()
        
    def openCBCWindow(self):
        if self.CBCWindow is None:
            self.CBCWindow = outputWindow("CBC")
        self.CBCWindow.show()
        
    def openOFBWindow(self):
        if self.OFBWindow is None:
            self.OFBWindow = outputWindow("OFB")
        self.OFBWindow.show()
        
    def openCFBWindow(self):
        if self.CFBWindow is None:
            self.CFBWindow = outputWindow("CFB")
        self.CFBWindow.show()

    def openCTRWindow(self):
        if self.CTRWindow is None:
            self.CTRWindow = outputWindow("CTR")
        self.CTRWindow.show()
        
        
    '''
    The following will open a file picker dialog in the current working directory,
    load the chosen image, and adjust the scaling if need be.
    '''
    def openFilePicker(self):
        path = QFileDialog.getOpenFileName(self, 'Choose an image file', '', 
                                           'All Files(*.*)')
    
        if path != ('', ''):
            print(path[0])
            self.img = Image.open(path[0])
            self.inputImage = QPixmap(path[0]).scaledToHeight(600)
            self.inputImageLabel.setPixmap(self.inputImage)
            self.inputImageLabel.show()
            
            
            



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())
    