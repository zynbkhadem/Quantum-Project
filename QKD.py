import random

def generate_random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    return [random.randint(0, 1) for _ in range(length)]

def encode_bits(bits, bases):
    encoded_bits = []
    for i in range(len(bits)):
        if bases[i] == 0: 
            encoded_bits.append(bits[i])
        else: 
            encoded_bits.append(bits[i] + 2)
    return encoded_bits

def measure_bits(encoded_bits, bases):
    measured_bits = []
    for i in range(len(encoded_bits)):
        if bases[i] == 0:  
            measured_bits.append(encoded_bits[i] % 2)
        else:  
            measured_bits.append((encoded_bits[i] // 2) % 2)
    return measured_bits

def sift_keys(alice_bits, bob_bits, alice_bases, bob_bases):
    sifted_key = []
    for i in range(len(alice_bases)):
        if alice_bases[i] == bob_bases[i]:
            sifted_key.append(alice_bits[i])
    return sifted_key


length = 20
alice_bits = generate_random_bits(length)
alice_bases = generate_random_bases(length)
encoded_bits = encode_bits(alice_bits, alice_bases)

bob_bases = generate_random_bases(length)
bob_bits = measure_bits(encoded_bits, bob_bases)

sifted_key = sift_keys(alice_bits, bob_bits, alice_bases, bob_bases)
print("Sifted Key:", sifted_key)

