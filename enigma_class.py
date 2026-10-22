#!/usr/bin/env python3
import string

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

#
#

class Rotor:
    def __init__(self, name, position=0, ring_setting=0):
        self.name = name
        self.wiring = ROTOR_WIRINGS[name]
        self.notch = ROTOR_NOTCHES[name]

        self.position = position
        self.ring_setting = ring_setting

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
        shifted = (
            num
            + self.position
            - self.ring_setting
        ) % 26

        wired_letter = self.wiring[shifted]
        wired_num = ALPHABET.index(wired_letter)

        return (
            wired_num
            - self.position
            + self.ring_setting
        ) % 26

    def backward(self, num):
        shifted = (
            num
            + self.position
            - self.ring_setting
        ) % 26

        wired_letter = self.inverse_wiring[shifted]
        wired_num = ALPHABET.index(wired_letter)

        return (
            wired_num
            - self.position
            + self.ring_setting
        ) % 26


class Enigma:
    def __init__(
        self,
        rotor_names,
        positions,
        ring_settings,
        plugboard_pairs=None
    ):
        if len(rotor_names) != 3:
            raise ValueError("This implementation expects exactly 3 rotors.")

        if len(positions) != 3:
            raise ValueError("Need exactly 3 rotor positions.")

        if len(ring_settings) != 3:
            raise ValueError("Need exactly 3 ring settings.")

        self.initial_positions = positions.copy()

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
        left, middle, right = self.rotors

        middle_at_notch = middle.at_notch()
        right_at_notch = right.at_notch()

        if middle_at_notch:
            left.step()

        if right_at_notch or middle_at_notch:
            middle.step()

        right.step()

    def plugboard_swap(self, num):
        return self.plugboard[num]

    def reflect(self, num):
        letter = self.reflector[num]
        return ALPHABET.index(letter)

    def encrypt_char(self, char):
        if char not in ALPHABET:
            return char

        self.step_rotors()

        num = ALPHABET.index(char)

        num = self.plugboard_swap(num)

        # Forward: right -> middle -> left
        for rotor in reversed(self.rotors):
            num = rotor.forward(num)

        num = self.reflect(num)

        # Backward: left -> middle -> right
        for rotor in self.rotors:
            num = rotor.backward(num)

        num = self.plugboard_swap(num)

        return ALPHABET[num]

    def encrypt(self, message):
        result = ""

        for char in message.upper():
            result += self.encrypt_char(char)

        return result

    # because decryption is actually the same function
    decrypt = encrypt

    def reset(self):
        for rotor, position in zip(
            self.rotors,
            self.initial_positions
        ):
            rotor.position = position
