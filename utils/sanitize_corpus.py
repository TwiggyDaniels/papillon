# Utilize this entry point to sanitize a file of all punctuation, stop words 
#(by a flag), set characters to lowercase, and remove numbers.


import csv
import re
import string
import sys

import pandas as pd

csv.field_size_limit(sys.maxsize)

# Description: Non-helper method to call for sanitizing an input text entry.
#
# Return: data: Array of sanitized sentences
def sanitize_data(data, min_frequency = 10, save_stopwords = False,
save_sanitize = False, sanitized_name = 'default_sanitized.csv'):

    word_freq = {}
    letter_freq = {}
    final_word_freq = {}
    final_letter_freq = {}
        
    for e, row in data.iterrows():
        # attempt to remove non-english characters by encoding to 
        # ascii back to unicode again and ignoring failures
        data.iat[e, 0] = remove_nonenglish(data.iat[e, 0])

        # remove all punctuation (TODO: decide whether to remove periods)
        # remove all numerals
        data.iat[e, 0] = remove_numbers(data.iat[e, 0])
        
        # strip all extraneous whitespace
        data.iat[e, 0] = reduce_whitespace(data.iat[e, 0])
    
        # remove whatever punctuation that string can match
        data.iat[e, 0] = remove_punctuation(data.iat[e, 0])
    
        # all to lowercase
        data.iat[e, 0] = remove_uppercase(data.iat[e, 0])
        
        # remove all stopwords if the flag is set
        if (not remove_stopwords):
            data.iat[e, 0] = remove_stopwords(data.iat[e, 0])

        # remove single character words (also non-english?)
        data.iat[e, 0] = remove_single(data.iat[e, 0])
        
        # get the frequencies of each letter and word
        word_freq, letter_freq = find_frequency(data.iat[e, 0], 
                word_freq, letter_freq)

        data.iat[e, 0] = remove_frequency(data.iat[e, 0], 
                word_freq, min_frequency)

        # get the frequencies of each letter and word
        final_word_freq, final_letter_freq = find_frequency(data.iat[e, 0], 
                final_word_freq, final_letter_freq)

    with open('word.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in final_word_freq.items():
            writer.writerow([key, value])

    with open('letter.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in final_letter_freq.items():
            writer.writerow([key, value])

    return data

def remove_nonenglish(entry):
    return entry.encode('ascii', 'ignore').decode('utf-8', 'ignore')

# TODO: Implement
def remove_stopwords(entry):
    return entry

def remove_uppercase(entry):
    return entry.lower()

# Code from: 'https://stackoverflow.com/questions/265960/
# best-way-to-strip-punctuation-from-a-string'
def remove_punctuation(entry):
    return entry.translate(str.maketrans('', '', string.punctuation))

def remove_numbers(entry):
    return re.sub(r'\d+', '', entry)

def reduce_whitespace(entry):
    entry = re.sub('\s+', ' ', entry)
    return re.sub(' +', ' ', entry)

def remove_single(entry):
    return re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', entry)

def find_frequency(entry, word_freq, letter_freq):
    words = entry.split(' ')

    for word in words:
        if (word in word_freq.keys()):
            word_freq[word] += 1
        else:
            word_freq[word] = 1

        for letter in word:
            if (letter in letter_freq):
                letter_freq[letter] += 1
            else:
                letter_freq[letter] = 1

    return word_freq, letter_freq

def remove_frequency(entry, word_freq, min_freq):
    words = entry.split(' ')

    clean_entry = ''

    for i, word in enumerate(words):
        if (word_freq[word] >= min_freq):
            clean_entry += word
            if (not i == len(words) - 1):
                clean_entry += ' '
        
    return clean_entry
