# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 10:22:02 2021

@author: Bryant
"""
import numpy as np
from Helper import Helper

ROUND_CONSTANTS = ["01", "02", "04", "08", "10", "20", "40", "80", "1B", "36"]

class KeySchedule():
    
    
    '''
    When initializing the key schedule class it will generate the entire key 
    schedule, based off of the initial key value.
    
    '''
    def __init__(self, inputKey):
        self.keys = []
        
        self.keys.append(inputKey)
        
        for i in range(1,11):    
            nextKey = self.generateNextKey(self.keys[i-1], i)        
            self.keys.append(nextKey)
        
        
    '''
    The following will generate the next key value based off of the previous 
    key schedule value. by utilizing the g-function and xor the various 'word' values
    '''
    def generateNextKey(self, inputKey, roundNum):        
        words = self.splitKeyIntoWords(inputKey)
        
        gResults = self.g(words[3], roundNum)
        results = []
        
        a = Helper.convertHexToBinary(words[0])
        b = Helper.convertHexToBinary(gResults)
        results.append(Helper.convertBinaryToHexadecimal(Helper.xor(a,b)))
        
        for i in range(1,4):
            a = Helper.convertHexToBinary(results[i-1])
            b = Helper.convertHexToBinary(words[i])
            results.append(Helper.convertBinaryToHexadecimal(Helper.xor(a,b)))
        return ''.join(results)
    
    def getKey(self, keyNum):
        return self.keys[keyNum]        
        
        
    '''
    Split the input key value into 3 word values and store them in an array
    '''
    def splitKeyIntoWords(self, key):
        words = []
        words.append(key[0:8])
        words.append(key[8:16])
        words.append(key[16:24])
        words.append(key[24:32])
        return words
        
    '''
    The g function uses one word, split into 4 values of 2 hex bits. Then shift 
    the values before performing an s-box substitution. before finally performing 
    an xor operation with the left-most value and a static RC value
    '''
    def g(self, inputWord, roundNum):
        wordBytes = [inputWord[0:2], inputWord[2:4], inputWord[4:6], inputWord[6:8]]
        wordBytes = list(np.roll(wordBytes, -1))
        
        results = []
        for word in wordBytes:
            results.append(Helper.sBox(word))
        
        a = Helper.convertHexToBinary(results[0])

        b = Helper.convertHexToBinary(ROUND_CONSTANTS[roundNum-1])
        results[0] = Helper.convertBinaryToHexadecimal(Helper.xor(a, b))
        

        return ''.join(results)
