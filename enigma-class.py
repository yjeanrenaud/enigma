#!/usr/bin/env python3
import string

class Enigma:
    def __init__(self, rotors, ring_settings, plugboard):
        self.rotors = rotors
        self.ring_settings = ring_settings
        self.plugboard = plugboard
        
    def encrypt(self, message):
        ciphertext = ""
        for char in message:
            if char in string.ascii_uppercase:
                # convert character to number (0-25)
                num = ord(char) - ord('A')
                
                # pass through plugboard
                num = self.plugboard[num]
                
                # pass through rotors right-to-left
                for i in range(len(self.rotors)-1, -1, -1):
                    num = (num + self.rotors[i] - self.ring_settings[i]) % 26
                
                # pass through reflector
                num = (num + 13) % 26
                
                # pass through rotors left-to-right
                for i in range(len(self.rotors)):
                    num = (num - self.rotors[i] + self.ring_settings[i]) % 26
                
                # pass through plugboard
                num = self.plugboard[num]
                
                # convert number back to character
                char = chr(num + ord('A'))
            
            # append character to ciphertext
            ciphertext += char
        
        return ciphertext
    
    def decrypt(self, ciphertext):
        plaintext = ""
        for char in ciphertext:
            if char in string.ascii_uppercase:
                # convert character to number (0-25)
                num = ord(char) - ord('A')
                
                # pass through plugboard
                num = self.plugboard[num]
                
                # pass through rotors left-to-right
                for i in range(len(self.rotors)):
                    num = (num - self.rotors[i] + self.ring_settings[i]) % 26
                
                # pass through reflector
                num = (num + 13) % 26
                
                # pass through rotors right-to-left
                for i in range(len(self.rotors)-1, -1, -1):
                    num = (num + self.rotors[i] - self.ring_settings[i]) % 26
                
                # pass through plugboard
                num = self.plugboard[num]
                
                # convert number back to character
                char = chr(num + ord('A'))
            
            # append character to plaintext
            plaintext += char
        
        return plaintext
