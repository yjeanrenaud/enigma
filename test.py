#!/usr/bin/env python3
from enigma_class import Enigma 


# Rotor order: left, middle, right
rotors = ["I", "II", "III"]

# Starting rotor positions
# 0 = A, 1 = B, ..., 25 = Z
positions = [0, 0, 0]


# Ring settings 
# (numbers from 0 to 25), three up to five rotators e.g.
ring_settings = [2, 15, 7]

# plugboard settings (list of pairs of letters) usually 4 to 5 pairs e.g.
plugboard = [
    ("A", "F"),
    ("J", "V"),
    ("G", "L"),
    ("D", "M")
]

# now create a new Enigma machine with the given settings (based on the daily codebook)
enigma = Enigma(rotors, positions, ring_settings, plugboard)

# encrypt a message
message = "HELLO WORLD"
##should most likely be "VCIIR RHHRB" as whitepaces were substituted by X, chars grouped by four etc.

ciphertext = enigma.encrypt(message)
print(ciphertext)  # output: "VCIIR RHHRB"

# Reset the rotors and rings
enigma.reset()

# actually, decrypt = encrypt
# decrypt ciphertext
plaintext = enigma.decrypt(ciphertext)
print(plaintext)  # output: "HELLO WORLD"
