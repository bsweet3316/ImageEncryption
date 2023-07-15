# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 13:38:03 2021

@author: Bryant
"""

from Helper import Helper
import numpy as np
from PIL import Image
from AES import AES
from random import uniform

class ImageEncryption():

    '''
    initialize the class with the image pixel matrix. flatten the matrix to an
    array of pixel values. Then finally convert all pixel decimal values to 
    hexadecimal values.
    '''    
    def __init__(self, image):
        self.inputImagePixelMatrix = np.asarray(image)
        self.height = len(self.inputImagePixelMatrix)
        self.width = len(self.inputImagePixelMatrix[0])
        
        self.flattenedData = Helper.flattenImageMatrix(self.inputImagePixelMatrix)
        self.inputBytes = self.convertPixelToHex(self.flattenedData)
            
    def convertPixelToHex(self, flattenedData):
        output = []
        for value in flattenedData:
            output.append(Helper.convertBinaryToHexadecimal(Helper.convertDecimalToBinary(value)))
            
        return output
    
    
    '''
    The following will cvonvert the output of the encryption mode into an 
    array of pixel values (a tuple of three decimal values for rgb) 
    '''
    def convertToPixelArray(self, encryptionOutput):
        pixelArray = []
        outputString = ''.join(encryptionOutput)
        length = int(len(outputString)/6)
        for i in range(0,length):
            first = i*6
            last = (i+1)*6
            pixelHex = outputString[first:last]
            val1 = Helper.convertBinaryToDecimal(Helper.convertHexToBinary(pixelHex[0:2]))
            val2 = Helper.convertBinaryToDecimal(Helper.convertHexToBinary(pixelHex[2:4]))
            val3 = Helper.convertBinaryToDecimal(Helper.convertHexToBinary(pixelHex[4:6]))
            pixel = (val1, val2, val3)
            pixelArray.append(pixel)
        return pixelArray
    
    
    '''
    The following will encrypt the image in ECB mode, the basic function is as follows:
        
        Yi = AESk(Xi)
        
    This mode mimics a stream cipher since each encryption block is unaffected
    by the previous encryption output.
    '''
    def encryptInECB(self, key):
        print("ENCRYPTING IN ECB MODE")
        output = []
        length = int(len(self.inputBytes)/16)
        extra = False
        #The following prevents a failure if the number entire length of the
        #image file is not divisible by 16 (16 because the inputbytes are an array
        #of 2 bit hex values)
        remainder = len(self.inputBytes)%16
        if remainder > 0:
            extra = True

        for i in range(0, length):
            firstIndex = i*16
            lastIndex = (i+1)*16
            encryptionInput = ''.join(self.inputBytes[firstIndex:lastIndex])
            
            encryptionOutput = AES.encrypt(encryptionInput, key)
            output.append(encryptionOutput) 
            if i % 100 == 0:
                print(output[-1])
        
        #if it was determined that there are extra bits, perform another round 
        #of encryption with the final bits padded to a length of 128.
        if extra:
            lastIndex = length*16
            self.extraBytes = int(len(self.inputBytes) - lastIndex)
            lastBytes = self.inputBytes[length*16:]
            for i in range(self.extraBytes, 16):
                lastBytes.append('11')    
            output.append(AES.encrypt(''.join(lastBytes), key))
        
        #Save the image to an appropriately named file.
        self.saveToImage(output, 'ECB')
            
        
    '''
    Encrypt the image file in a CBC mode of operation. The function for which is:
        
        Yi = AESk(Xi XOR Yi-1)
        where Y1 = AESk(X0 XOR IV)
        
    This mode of operation is affected by the previous output of the encryption 
    function by simply x-or'ing the output with the next input.
    
    The same logic to determine if extra bits are present as in the ECB function 
    is also used here.
    '''
    def encryptInCBC(self, key, IV):
        print("ENCRYPTING IN CBC MODE")
        output = []
        length = int(len(self.inputBytes)/16)
        extra = False
        remainder = len(self.inputBytes)%16
        if remainder > 0:
            extra = True
            
        firstEncryption = Helper.xor(''.join(self.inputBytes[0:16]), IV)
        output.append(AES.encrypt(firstEncryption, key))
        
        for i in range(1, length):
            firstIndex = i*16
            lastIndex = (i+1)*16
            a = Helper.convertHexToBinary(''.join(self.inputBytes[firstIndex:lastIndex]))
            b = Helper.convertHexToBinary(output[i-1])
            encryptionInput = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
            output.append(AES.encrypt(encryptionInput, key))
            
        if extra:
            lastIndex = length*16
            self.extraBytes = int(len(self.inputBytes) - lastIndex)
            lastBytes = self.inputBytes[length*16:]
            for i in range(self.extraBytes, 16):
                lastBytes.append('11')    
            
            a = Helper.convertHexToBinary(''.join(lastBytes))
            b = Helper.convertHexToBinary(output[-1])
            encryptionInput = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
            output.append(AES.encrypt(encryptionInput, key))
        self.saveToImage(output, 'CBC')
    
    '''
    Encrypt the image file in a OFB mode of operation. The function for which is:
        
        Yi = AESk(Si-1) XOR Xi
        where Y1 = AESk(IV) XOR X0
        
    This mode of operation is affected by the previous output of the encryption 
    function by encrypting the IV at first, then using the output of that encryption
    as the input of the next excryption block while also x-or'ing that same output 
    with the plain text block.
    
    The same logic to determine if extra bits are present as in the ECB function 
    is also used here.
    '''
    def encryptInOFB(self, key, IV):
        print("ENCRYPTING IN OFB MODE")
        output = []
        s = []
        length = int(len(self.inputBytes)/16)
        extra = False
        remainder = len(self.inputBytes)%16
        if remainder > 0:
            extra = True
            
        encryptionOutput = AES.encrypt(IV, key)
        s.append(encryptionOutput)
        a = Helper.convertHexToBinary(''.join(self.inputBytes[0:16]))
        b = Helper.convertHexToBinary(encryptionOutput)
        encryptionOutput = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
        output.append(encryptionOutput)
        
        for i in range(1, length):
            firstIndex = i*16
            lastIndex = (i+1)*16
            encryptionOutput = AES.encrypt(s[i-1], key)
            s.append(encryptionOutput)
            a = Helper.convertHexToBinary(''.join(self.inputBytes[firstIndex:lastIndex]))
            b = Helper.convertHexToBinary(encryptionOutput)
            encryptionOutput = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
            output.append(encryptionOutput)

        if extra:
            lastIndex = length*16
            self.extraBytes = int(len(self.inputBytes) - lastIndex)
            lastBytes = self.inputBytes[length*16:]
            for i in range(self.extraBytes, 16):
                lastBytes.append('11') 
            encryptionOutput = AES.encrypt(s[-1], key)
            a = Helper.convertHexToBinary(''.join(lastBytes))
            b = Helper.convertHexToBinary(encryptionOutput)
            encryptionOutput = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
            output.append(encryptionOutput)
            
        self.saveToImage(output, 'OFB')
        
        
    '''
    Encrypt the image file in a CFB mode of operation. The function for which is:
        
        Yi = AESk(Yi-1) XOR Xi
        where Y1 = AESk(IV) XOR X0
        
    This mode of operation is affected by the previous output of the encryption 
    function by encrypting the IV at first, x-or'ing that output with the plain 
    text block. Then taking the output of that xor operation as the input to the 
    next encryption function.
    
    The same logic to determine if extra bits are present as in the ECB function 
    is also used here.
    '''
    def encryptInCFB(self, key, IV):
        print("ENCRYPTING IN CFB MODE")
        output = []
        length = int(len(self.inputBytes)/16)
        extra = False
        remainder = len(self.inputBytes)%16
        if remainder > 0:
            extra = True
        
        encryptionOutput = AES.encrypt(IV, key)
        a = Helper.convertHexToBinary(''.join(self.inputBytes[0:16]))
        b = Helper.convertHexToBinary(encryptionOutput)
        
        output.append(Helper.convertBinaryToHexadecimal(Helper.xor(a,b)))
        
        for i in range(1, length):
            firstIndex = i*16
            lastIndex = (i+1)*16
            encryptionOutput = AES.encrypt(output[-1], key)
            
            a = Helper.convertHexToBinary(''.join(self.inputBytes[firstIndex:lastIndex]))
            b = Helper.convertHexToBinary(encryptionOutput)
            output.append(Helper.convertBinaryToHexadecimal(Helper.xor(a,b)))
            

            
        if extra:
            lastIndex = length*16
            self.extraBytes = int(len(self.inputBytes) - lastIndex)
            lastBytes = self.inputBytes[length*16:]
            for i in range(self.extraBytes, 16):
                lastBytes.append('11') 
                
            encryptionOutput = AES.encrypt(output[-1], key)
            a = Helper.convertHexToBinary(''.join(lastBytes))
            b = Helper.convertHexToBinary(encryptionOutput)
            encryptionOutput = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
            output.append(encryptionOutput)
        self.saveToImage(output, 'CFB')
        
    '''
    Encrypt the image file in a CTR mode of operation. The function for which is:
        
        Yi = AESk(IV||counter) XOR Xi
        
    This mode of operation is not affected by the output of the previous encryption
    block and simply alters the input of the encryption function by concatenating 
    a 24 bit IV with an 8 bit counter value (All in hex).
    
    The same logic to determine if extra bits are present as in the ECB function 
    is also used here.
    '''
    def encryptInCTR(self, key, IV):
        print("ENCRYPTING IN CTR MODE")
        output = []
        length = int(len(self.inputBytes)/16)
        extra = False
        remainder = len(self.inputBytes)%16
        if remainder > 0:
            extra = True
        
        counter = int(uniform(1000, 10000))
        
        for i in range(0, length):
            firstIndex = i*16
            lastIndex = (i+1)*16
            
            counterHex = Helper.convertBinaryToHexadecimal(Helper.convertDecToBinwithLength(counter, 32))

            encryptionInput = ''.join([IV, counterHex])
            encryptionOutput = AES.encrypt(encryptionInput, key)
        
            a = Helper.convertHexToBinary(encryptionOutput)
            b = Helper.convertHexToBinary(''.join(self.inputBytes[firstIndex:lastIndex]))

            output.append(Helper.convertBinaryToHexadecimal(Helper.xor(a,b)))
            counter+= 1

            
        if extra:
            lastIndex = length*16
            self.extraBytes = int(len(self.inputBytes) - lastIndex)
            lastBytes = self.inputBytes[length*16:]
            for i in range(self.extraBytes, 16):
                lastBytes.append('11') 
                
            counterHex = Helper.convertBinaryToHexadecimal(Helper.convertDecToBinwithLength(counter, 32))
        
            encryptionInput = ''.join([IV, counterHex])
            encryptionOutput = AES.encrypt(encryptionInput, key)
        
            a = Helper.convertHexToBinary(encryptionOutput)
            b = Helper.convertHexToBinary(''.join(lastBytes))
            
            output.append(Helper.convertBinaryToHexadecimal(Helper.xor(a,b)))
            
        self.saveToImage(output, 'CTR')
        
            
    '''
    Save the output of the entire image encryption to an appropriately named file
    which will then be called by the output window function.
    '''
    def saveToImage(self, aesOutput, filename):
        pixelArray = self.convertToPixelArray(aesOutput)
        matrix = self.convertToMatrix(pixelArray)
        matrix = np.array(matrix, dtype=np.uint8)
        data = Image.fromarray(matrix)
        data.save(f'{filename}.png')
    
    '''
    convert the pixel array to a pixel matrix.
    '''
    def convertToMatrix(self, array):
        counter = 0
        length = self.height * self.width
        matrix = []
        while counter < length:
            for i in range(0, self.height):
                row = []
                for j in range(0, self.width):
                    row.append(array[counter])
                    counter += 1
                matrix.append(row)
        return matrix
    
                    
            
            
                
    
        