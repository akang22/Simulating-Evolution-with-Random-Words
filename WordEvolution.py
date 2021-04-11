# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:07:34 2021

@author: olive
"""

import enchant
import random as r

d = enchant.Dict("en_US")

#generates a random sequence of words with certain rules
def random_sequence (sequence_length):
    sequence = ""
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',\
                  's', 't', 'v', 'x', 'z']
    length = 0 #tracks length of sequence
    space = 0 #used to prevent two spaces in a row
    word_type = 0 #increases chances of vowels after consonants and vice versa
    consonant_frequency = 77
    space_frequency = 15
    
    while length < sequence_length:
        n = r.randint(0,100)
        word_type_gen = r.randint (0,10)
        if n > space_frequency or space == 1: #n is the rng to decide space frequency
            m = r.randint(0,100) #m is rng to decide consonant vs vowel
            if m < consonant_frequency and word_type == 1 or word_type_gen > 8:
                sequence = sequence + r.choice(consonants)
                word_type = 0 #if consonant is added, word_type = 0
            else:
                sequence = sequence + r.choice(vowels)
                word_type = 1 #if vowel is added, word_type = 1
                
            length += 1
            space = 0
            
        elif space != 1:
            sequence = sequence + " "
            length += 1
            space = 1
            
    return sequence

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

