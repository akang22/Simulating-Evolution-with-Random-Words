# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:07:34 2021

@author: olive
"""

import enchant
import random as r

d = enchant.Dict("en_US")

# generates a random sequence of words with rules to model real words
def random_sequence (sequence_length):
    sequence = [None] * sequence_length
    previous_char_type = 0 # 0: space, 1: vowel, 2: consonant

    CONSONANTS = { 'b': 0.02, 'c': 0.04, 'd': 0.038, 'f': 0.014, 'g': 0.03, 'h': 0.023, 'j': 0.0021, 'k': 0.0097, 'l': 0.053, 'm': 0.027, 
    'n': 0.072, 'p': 0.028, 'q': 0.0019, 'r': 0.073, 's': 0.087, 't': 0.067, 'v': 0.01, 'w': 0.0091, 'x': 0.0027, 'z': 0.0044 }
    ALPHABET = dict(CONSONANTS, **{ 'a': 0.078, 'e': 0.11, 'i': 0.086, 'o': 0.061, 'u': 0.033, 'y': 0.016 })

    SPACE_PC = 0.15
    CONSONANT_FOLLOWS_VOWEL_PC = 0.77

    for i in range(sequence_length):
        if previous_char_type == 0 or r.random() > SPACE_PC:
            if r.random() < CONSONANT_FOLLOWS_VOWEL_PC and previous_char_type == 1:
                sequence[i] = choose(CONSONANTS, 0.6262)
                previous_char_type = 2
            else:
                sequence[i] = choose(ALPHABET, 1.0102)
                previous_char_type = 1
        else:
            sequence[i] = " "
            previous_char_type = 0
            
    return ''.join(sequence)

def choose (dictionary, sum):
    running_val = r.random() * sum
    for k, v in dictionary.items():
        running_val -= v
        if 0 > running_val:
            return k
    return " "

#Uses random_sequence to generate random "words" and splits them into 2 word chunks. 
#Chunks are kept if at least one word in the chunk is "correct".
#s_length specifies how long the total input sequence is
#o_length specifies criteria for how long a word must be to be correct excluding I and a.
def selection (s_length, o_length):
    span = 2
    seq = random_sequence(s_length)
    check = seq.split()
    check = [" ".join(check[i:i+span]) for i in range(0, len(check), span)]
    output = ""
    
    for i in check:
        piece = i.split()
        group_length = len(piece)
        if group_length == 2: 
            if d.check(piece[0]) == True or d.check(piece[1]) == True:
                if len(piece[0]) > o_length and len(piece[1]) > o_length and i != " " \
                or i == "i" or i == "a":
                    output = output + " " + piece[0] + " " + piece[1]
        elif group_length == 1:
            if d.check(piece[0]) == True:
                if len(piece[0]) > o_length\
                and piece[0] != " " or i == "i" or i == "a":
                    output = output + " " + piece[0] 
    return output

#Part of a class of "endonucleases" that cuts out certain (extraneous) sequences from Species
def endonuclease(prune_sequence, dictionary):
    for component in prune_sequence.split():
        for k, v in dictionary.items():
            output = ""
            for i in v.split():
                if i != component:
                    output = output + " " + i
            dictionary[k] = output
    return dictionary
        

Species = {}

letter_code = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',\
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
#Creates primordial species A-Z, 
def create_primordial():
    Species1 = {}
    a = 0
    t = 0
    while t < (26):
        DNA = selection(10000, 1)
        species_tag = str(letter_code[a])
        Species1.update({"\n " + str(species_tag): DNA})
        a += 1
        t += 1
    return Species1

        # if b > 98:
        #     b = 0
        #     a += 1
    
        
Species = create_primordial()
#Always prune after Species = Species1 and not before
Prune = endonuclease("i a", Species)

[print(key, ":", value) for key, value in Prune.items()]

