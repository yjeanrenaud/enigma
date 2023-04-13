# enigma
work in progress. simulation of the [historic Enigma rotor cypher device
] (https://en.wikipedia.org/wiki/Enigma_machine) that was used during WWII.

## current implementation 
``` 
import enigma-class.py


# rotor settings (numbers from 0 to 25), three up to five rotators e.g.
rotors = [3, 17, 7]

# ring settings (numbers from 0 to 25), three up to five rotators e.g.
ring_settings = [2, 15, 7]

# plugboard settings (list of pairs of letters) usually 4 to 5 pairs e.g.
plugboard = [0, 5, 11, 22] # means: A<==>F, J<==>V

# now create a new Enigma machine with the given settings (based on the daily codebook)
enigma = Enigma(rotors, ring_settings, plugboard)

# encrypt a message
message = "HELLO WORLD"
##should most likely be "XHEL LOXW ORLD" as whitepaces were substituted by X, chars grouped by four etc.

ciphertext = enigma.encrypt(message)
print(ciphertext)  # output: "ZPFVHYQAKG"

# decrypt ciphertext
plaintext = enigma.decrypt(ciphertext)
print(plaintext)  # output: "HELLOWORLD"
