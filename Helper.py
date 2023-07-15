# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 09:53:22 2021

@author: Bryant
"""


SUBSTITUTION_BOX = [
#         1     2     3     4     5     6     7     8     9     10    11    12    13    14    15    16
        ["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"], # row 0
        ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"], # row 1
        ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"], # row 2
        ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"], # row 3
        ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"], # row 4
        ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"], # row 5
        ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"], # row 6
        ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"], # row 7
        ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"], # row 8 
        ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"], # row 9
        ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"], # row 10
        ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"], # row 11
        ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"], # row 12
        ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"], # row 13
        ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"], # row 14
        ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]  # row 15
        ]



class Helper():
    
    '''
    inputByte - a 2 bit hex value 
    returns - the sbox value
    '''
    def sBox(inputByte):
        #By converting the first bit to a decimal row value and the second bit
        #to the decimal column value. A simple look up to the sbox matrix to
        #get the sbox value.
        rowBinary = Helper.convertHexToBinary(inputByte[0])
        row = Helper.convertBinaryToDecimal(rowBinary)
        
        columnBinary = Helper.convertHexToBinary(inputByte[1])
        column = Helper.convertBinaryToDecimal(columnBinary)
        
        output = SUBSTITUTION_BOX[row][column]
        return output
    
    def convertHexToBinary(input):
        fill = len(input) * 4
        return bin(int(input, 16))[2:].zfill(fill)
        
    def convertBinaryToHexadecimal(input):
        fill = len(input) / 4
        return hex(int(input,2)).replace("0x", "").zfill(int(fill)).upper()
        
    def convertBinaryToDecimal(input):
        return int(input, 2)
    
    def convertDecimalToBinary(input):
        return bin(input).replace("0b", "").zfill(8)
    
    def convertDecToBinwithLength(input, length):
        return bin(input).replace("0b", "").zfill(length)
    
    def xor(a,b):
        splitA = [i for i in a]
        splitB = [i for i in b]
        c = ""
        for i in range(0,len(splitA)):
            if splitA[i] != splitB[i]:
                c += '1'
            else:
                c+= '0'
        return c
        
    
    '''
    The following will convert the image matrix of pixel values to a single 
    array of decimal values.
    '''
    def flattenImageMatrix(imgMatrix):
        output = []
        imgHeight = len(imgMatrix)
        imgWidth = len(imgMatrix[0])
        print(f'{imgHeight}  {imgWidth}')
        for i in range(0, imgHeight):
            for j in range(0, imgWidth):
                pixel = list(imgMatrix[i][j])
                for k in range(0,3):
                    output.append(pixel[k])
                    
        return output
                    
        
        