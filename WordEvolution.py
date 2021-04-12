# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 17:07:34 2021

@author: olive
"""

import enchant
import random as r
import math 

d = enchant.Dict("en_US")

#generates a random sequence of words with certain rules
def random_sequence (sequence_length):
    sequence = ""
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r',\
                  's', 't', 'v', 'w', 'x', 'z']
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
    span = 1
    seq = random_sequence(s_length)
    check = seq.split()
    check = [" ".join(check[i:i+span]) for i in range(0, len(check), span)]
    output = ""
    
    for i in check:
        piece = i.split()
        print(piece)
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
        DNA = selection(1000, 1)
        species_tag = "/1/" + str(letter_code[a])
        Species1.update({species_tag: DNA})
        a += 1
        t += 1
    return Species1

#function that simulates a polymerase class enzyme. Makes new copies of "DNA"
#10% chance of causing a mutation, which is 50% addition and 50% subsitution.
#Replication increases population
def replication(dictionary):
    survival = 30
    capacity = 1000
    a = 0
    b = 0
    temp_dictionary = {}
    for k, v in dictionary.items():
        replication = ""
        mutated = 0
        if r.randint(0,100) < 10: #10% of replications result in some type of mutation
            mutated = 1
            new_species_tag = str(letter_code[a])
            replication = replication + v + " " #second replication may not be needed
            if r.randint(0,100) < 80: #mutation that adds random sequence
                replication = replication + selection(10000, 3)
            else: #mutation that adds random length sequence to random place
                split = replication.split()
                split[r.randint(0, (len(split) - 1))] += random_sequence(r.randint(0,20))
                for i in split:
                    replication = replication + i + " "
            b += 1
            if b > 8:
                b = 0
                a += 1
                
        decode = k.split("/")
        population = int(decode[1])
            
        check = v.split()
        x = 0 #counts correct words
        y = 0
        for i in check:
            if d.check(i) == True:
                x += 1
                if len(i) > 3:
                    y += 1
            replication = replication + i + " "
            
        fitness = (x/len(check)) + y
        modify = k.split("/")
        if mutated == 0:
            temp_dictionary.update({"/" +\
            str(math.ceil(population + (population*((fitness**2)\
            +(1-(survival/100)))*((capacity - population)/capacity))))\
            + "/" + modify[-1]: replication}) 
            #grows at full rate since both strands are non-mutation fixed
            
        else:
            temp_dictionary.update({"/" +\
            str(math.ceil(population + (0.5*population*((fitness**2)\
            +(1-(survival/100)))*((capacity - population)/capacity))))\
            + "/" + modify[-1] + "-" + new_species_tag + str(b):\
            replication})  #replicated (fixed mutation) strand (grows at half rate)
                
            temp_dictionary.update({"/" +\
            str(math.ceil(population + (population*((fitness**2)\
            +(1-(survival/100)))*((capacity - population)/capacity))))\
            + "/" + modify[-1]: v}) #parent strand (grows at half rate)
    
    return temp_dictionary
                    
Species = create_primordial()
#Always prune after Species = Species1 and not before
Prune = endonuclease("i a", Species)
replicated = replication(Prune)
replicated = replication(replicated)
Prune = endonuclease("i a", replicated)
[print(key, ":", value) for key, value in replicated.items()]

