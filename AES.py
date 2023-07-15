# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 08:57:08 2021

@author: Bryant
"""

from Helper import Helper
from keySchedule import KeySchedule
import numpy as np

MIX_COLUMNS_MATRIX = [
        ["02", "03", "01", "01"],
        ["01", "02", "03", "01"],
        ["01", "01", "02", "03"],
        ["03", "01", "01", "02"]
        ]

IRREDUCIBLE_VALUE = '100011011'

class AES():
    
    
    '''
    The following is the main function to encrypt a single 128 bit block. 
    Following the AES mode that utilizes a 128 bit key, there are 10 rounds, 
    starting with a key addition operation. Then 9 rounds of byte substitution,
    shift rows, mix column, and a key addition layer. Finally there is one last 
    round that is similar to the last 9 rounds except there is no mix column layer.
    '''
    def encrypt(inputValue, key):
        #Start by creating the key schedule and load it into a list that can be 
        #retrieved during the corresponding key addition layer.
        keySchedule = KeySchedule(key)
        
        roundInput = AES.keyAdditionLayer(inputValue, keySchedule.getKey(0))
        
        for i in range(1,10):
            substitutionLayerResults = AES.substitutionLayer(roundInput)
            shiftRowLayerResults = AES.shiftRowsLayer(substitutionLayerResults)
            mixColumnsLayerResults = AES.mixColumnsLayer(shiftRowLayerResults)
            roundInput = AES.keyAdditionLayer(mixColumnsLayerResults, keySchedule.getKey(i))
        finalSubstitution = AES.substitutionLayer(roundInput)
        finalShiftRow = AES.shiftRowsLayer(finalSubstitution)
        finalKeyAdd = AES.keyAdditionLayer(AES.convertMatrixToString(finalShiftRow), keySchedule.getKey(10))
        return finalKeyAdd
        
        
    '''
    The following will take a 32 hex bit input and split it into an array
    of length 16 where each value is a 2 hex bit value.
    '''
    def seperateInputToArray(input):
        output = []
        for i in range(0,16):
            firstIndex = 2*i
            lastIndex = (2*(i+1))
            output.append(input[firstIndex:lastIndex])        
        return output
    
    
    '''
    The following will take the array of length 16 and convert it to a matrix of 
    dimensions 4x4 it will remain in this format for the shift rows and mix columns
    layer. 
    '''
    def convertByteArrayToMatrix(input):
        output = []
        for i in range(0, 4):
            row = []
            for j in range(0, 4):
                row.append(input[i+4*j])                
            output.append(row)
        return output
    
    '''
    The following will convert the 4x4 matrix into a single string that is 32 
    characters long.
    '''
    def convertMatrixToString(input):
        output = []
        for i in range(0,4):
            for j in range(0,4):
                output.append(input[j][i])
                
        return ''.join(output)
        
        
    '''
    The following performs the substitution layer operation for AES, by converting 
    string input to an array of 2 bit hexadecimal numbers. then for each 2 bit
    number it will perform an s-box substitution. The return value will be in an
    array format of 2 bit hex values
    '''
    def substitutionLayer(inputBytes):
        outputBytes = []
        if(len(inputBytes) == 32):
            inputArray = AES.seperateInputToArray(inputBytes)
            for byte in inputArray:
                outputBytes.append(Helper.sBox(byte))
                
        return outputBytes
    
    '''
    The following will convert the array into a matrix representation then for 
    each row of the matrix it will perform the correct shift operation.
    '''
    def shiftRowsLayer(inputByteArray):
        byteMatrix = AES.convertByteArrayToMatrix(inputByteArray)
            
        outputMatrix = []
        
        # ROW 0:
        outputMatrix.append(byteMatrix[0])
        
        # ROW 1:
        outputMatrix.append(list(np.roll(byteMatrix[1], 3)))
        
        # ROW 2:
        outputMatrix.append(list(np.roll(byteMatrix[2], 2)))
        
        # ROW 3:
        outputMatrix.append(list(np.roll(byteMatrix[3], 1)))

        return outputMatrix
    
    '''
    The following will multiply the output of the shift rows layer by the 
    mix column matrix that is specified at the top of this file.
    '''
    def mixColumnsLayer(inputMatrix):
        c = []
        for k in range(0, 4):
            for i in range(0, 4):
                valuesToAdd = []
                for j in range(0, 4):
                    value = Helper.convertHexToBinary(inputMatrix[j][k])
                    mixColumnValue = MIX_COLUMNS_MATRIX[i][j]
                    
                    if mixColumnValue == "02":
                        value = AES.multiplyMixBy2(value)
                    elif mixColumnValue == "03":
                        value = AES.multiplyMixBy3(value)
                        
                    valuesToAdd.append(value)
                binary = AES.addAllValues(valuesToAdd)
                c.append(Helper.convertBinaryToHexadecimal(binary))
        output = ''.join(c)
        return output                  
    
    '''
    The next three functions assist in the matrix multiplication found in the 
    mix columns layer.
    '''
    def addAllValues(values):
        a = values[0]
        for i in range(1,4):
            a = Helper.xor(a, values[i])
        
        return a
                
    def multiplyMixBy2(value):
        a = Helper.convertDecimalToBinary(np.left_shift(Helper.convertBinaryToDecimal(value), 1))
        if len(a) == 9:
            a = Helper.xor(a, IRREDUCIBLE_VALUE)
            a = a[1:]
        return a
    
    def multiplyMixBy3(value):
        a = Helper.convertDecimalToBinary(np.left_shift(Helper.convertBinaryToDecimal(value), 1))
        if len(a) == 9:
            b = f'0{value}'
        else:
            b = value
        c = Helper.xor(a, b)
        if len(c) == 9 and c[0] == '1':
            c = Helper.xor(c, IRREDUCIBLE_VALUE)
        
        if len(c) == 9:
            c = c[1:]
            
        return c
    
    '''
    The following performs an xor operation on the two inputs
    '''
    def keyAdditionLayer(inputValue, key):
         a = Helper.convertHexToBinary(inputValue)
         b = Helper.convertHexToBinary(key)
         c = Helper.convertBinaryToHexadecimal(Helper.xor(a,b))
         return c

        
            
        
        
        