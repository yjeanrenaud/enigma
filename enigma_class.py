#!/usr/bin/env python3
import string

<<<<<<< HEAD
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
=======

ALPHABET = string.ascii_uppercase


# Historical Enigma I rotor wirings
ROTOR_WIRINGS = {
    "I":   "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II":  "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV":  "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V":   "VZBRGITYUPSDNHLXAWMJQOFECK",
}

# Turnover notches
ROTOR_NOTCHES = {
    "I": "Q",
    "II": "E",
    "III": "V",
    "IV": "J",
    "V": "Z",
}

REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"


class Rotor:
    def __init__(self, name, position=0, ring_setting=0):
        self.name = name
        self.wiring = ROTOR_WIRINGS[name]
        self.notch = ROTOR_NOTCHES[name]

        # 0 = A, 1 = B, ..., 25 = Z
        self.position = position
        self.ring_setting = ring_setting

        # Inverse wiring for the return path
        self.inverse_wiring = [""] * 26

        for i, letter in enumerate(self.wiring):
            output_index = ALPHABET.index(letter)
            self.inverse_wiring[output_index] = ALPHABET[i]

        self.inverse_wiring = "".join(self.inverse_wiring)

    def at_notch(self):
        return ALPHABET[self.position] == self.notch

    def step(self):
        self.position = (self.position + 1) % 26

    def forward(self, num):
        """
        Signal travelling from keyboard toward reflector.
        """

        # Account for rotor position and ring setting
        shifted = (
            num
            + self.position
            - self.ring_setting
        ) % 26

        # Pass through rotor wiring
        wired_letter = self.wiring[shifted]
        wired_num = ALPHABET.index(wired_letter)

        # Undo position/ring offset
        result = (
            wired_num
            - self.position
            + self.ring_setting
        ) % 26

        return result

    def backward(self, num):
        """
        Signal travelling from reflector back toward keyboard.
        """

        shifted = (
            num
            + self.position
            - self.ring_setting
        ) % 26

        # Use inverse rotor wiring
        wired_letter = self.inverse_wiring[shifted]
        wired_num = ALPHABET.index(wired_letter)

        result = (
            wired_num
            - self.position
            + self.ring_setting
        ) % 26

        return result


class Enigma:
    def __init__(
        self,
        rotor_names,
        positions,
        ring_settings,
        plugboard_pairs=None
    ):
        self.initial_positions = positions.copy()

        self.rotors = [
            Rotor(
                rotor_names[i],
                positions[i],
                ring_settings[i]
            )
            for i in range(3)
        ]

        if len(rotor_names) != 3:
            raise ValueError("This implementation expects exactly 3 rotors.")

        if len(positions) != 3:
            raise ValueError("Need exactly 3 rotor positions.")

        if len(ring_settings) != 3:
            raise ValueError("Need exactly 3 ring settings.")

        # Rotors stored left -> middle -> right
        self.rotors = [
            Rotor(
                rotor_names[i],
                positions[i],
                ring_settings[i]
            )
            for i in range(3)
        ]

        self.reflector = REFLECTOR_B

        self.plugboard = list(range(26))

        if plugboard_pairs:
            for a, b in plugboard_pairs:
                a_num = ALPHABET.index(a)
                b_num = ALPHABET.index(b)

                self.plugboard[a_num] = b_num
                self.plugboard[b_num] = a_num

    def step_rotors(self):
        """
        Implements Enigma stepping including double-stepping.
        """

        left, middle, right = self.rotors

        # Important: evaluate notch state BEFORE stepping
        middle_at_notch = middle.at_notch()
        right_at_notch = right.at_notch()

        # Middle rotor causes left rotor to step
        if middle_at_notch:
            left.step()

        # Middle rotor steps either:
        # - when right rotor is at its notch
        # - when it itself is at its notch
        if right_at_notch or middle_at_notch:
            middle.step()

        # Right rotor always steps
        right.step()

    def plugboard_swap(self, num):
        return self.plugboard[num]

    def reflect(self, num):
        letter = self.reflector[num]
        return ALPHABET.index(letter)

    def encrypt_char(self, char):
        if char not in ALPHABET:
            return char

        # Enigma steps BEFORE encryption
        self.step_rotors()

        num = ALPHABET.index(char)

        # Plugboard
        num = self.plugboard_swap(num)

        # Forward: right -> middle -> left
        for rotor in reversed(self.rotors):
            num = rotor.forward(num)

        # Reflector
        num = self.reflect(num)

        # Backward: left -> middle -> right
        for rotor in self.rotors:
            num = rotor.backward(num)

        # Plugboard again
        num = self.plugboard_swap(num)

        return ALPHABET[num]

    def encrypt(self, message):
        result = ""

        for char in message.upper():
            result += self.encrypt_char(char)

        return result

    decrypt = encrypt
    def reset(self):
        for rotor, position in zip (self.rotors, self.initial_positions):
            rotor.position = position
>>>>>>> 412f4dc (updated code)
