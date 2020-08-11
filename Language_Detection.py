"""
Author: Steven Yang
This file process data to be feed into the network
"""
import unicodedata
import string
import numpy as np

# We are dealing with around 570,000 words for each of the three languages we are studying
# Data are lists downloaded from GitHub
with open("es_full.txt", encoding="utf-8") as s:
    spanish = [line.rstrip("\n") for line in s]

with open("fr_full.txt", encoding='utf-8') as f:
    french = [line.rstrip('\n') for line in f]

with open("nl_full.txt", encoding="utf-8") as d:
    dutch = [line.rstrip('\n') for line in d]


# Functions to help clean the lists


def remove_spaces(word):
    return word.strip()


def lower_case(word):
    return str.lower(word)


def remove_numbers(word):
    return ''.join([i for i in word if not i.isdigit()])


def break_lines(b):  # this function is tailored for spanish
    fix = []
    for i in b:
        fix += i.split()
    return fix


def replace_periods(b):  # this function is tailored for french
    fix = []
    for i in b:
        fix.append(i.replace(".", ""))
    return fix


def remove_non_words(b):
    return list(filter(None, b))


def lower_case(word):
    return str.lower(word)


# clean lists
spanish1 = remove_non_words(spanish)
spanish2 = [remove_spaces(lower_case(i)) for i in spanish1]
del spanish1
spanish3 = [remove_numbers(i) for i in spanish2]
del spanish2
french1 = remove_non_words(french)
french2 = [remove_spaces(lower_case(i)) for i in french1]
del french1
french3 = [remove_numbers(i) for i in french2]
del french2
dutch1 = remove_non_words(dutch)
dutch2 = [remove_spaces(lower_case(i)) for i in dutch1]
del dutch1
dutch3 = [remove_numbers(i) for i in dutch2]
del dutch2
# Make sure distribution of number of words is even
Spanish = spanish3
del spanish3
Dutch = dutch3
del dutch3
French = french3
del french3

print("shut up")
print(len(Spanish), len(French), len(Dutch))
# Part 2: Produce list of all letters in our 'universe'


def find_accents(b):  # This function will find the accents we must include for the project
    accents = set()
    for i in b:
        for j in i:
            if j not in string.ascii_lowercase:
                accents.add(j)
    return accents


def need(b):
    total = set()
    for i in b:
        temp = find_accents(i)
        for j in temp:
            total.add(j)
    return total


def string_need(b):
    empty = ""
    for i in b:
        empty += i
    return empty


extra_accents = string_need(need([Spanish, French, Dutch]))
english_alphabet = string.ascii_lowercase
letters = list(english_alphabet + extra_accents)


cleaned = set()
for i in letters:
    cleaned.add(unicodedata.category(i))
cleaner = list(letters)


def fix_please(b):
    for i in b:
        if unicodedata.category(i) == 'Lo':
            # print(i)
            b.remove(i)
    return b


def ignore_character(b):
    bad = []
    for i in b:
        if unicodedata.category(i) == 'Lo':
            bad.append(i)
            # print(bad)
    return bad

# print(len(cleaner))


first = ignore_character(cleaner)
fix_please(cleaner)
second = ignore_character(cleaner)
fix_please(cleaner)
third = ignore_character(cleaner)
fix_please(cleaner)
fourth = ignore_character(cleaner)
fix_please(cleaner)
fifth = ignore_character(cleaner)
fix_please(cleaner)
sixth = ignore_character(cleaner)
fix_please(cleaner)
# maybe = ['º']
chinese = list(set(first + second + third + fourth + fifth + sixth))


freq = []
for i in cleaner:
    freq.append(unicodedata.category(i))


last = ['̇ ', '々', 'ˆ', 'ー', '〵', 'ˇ']
unneeded = last + chinese
for i in last:
    if i in cleaner:
        cleaner.remove(i)
# print('̇ ̇' in cleaner)

cryllic = list("бвгджзийклмнопрстуфхцчшщъыьэюя")


for i in cryllic:
    if i in cleaner:
       # print(i)
        cleaner.remove(i)

greek = [chr(code) for code in range(945,970)]
# print(len(greek))

not_need = list("бвгджзийклмнопрстуфцчшщъыьэюя")+list('αβγδεηθικλμνοπρςστυφ')+['ђ','ώ','ά', 'њ', 'έ'] + chinese

for i in greek:
    if i in cleaner:
        cleaner.remove(i)


# print(len(cleaner))
for i in ['ђ','ώ','ά', 'њ', 'έ']:
    cleaner.remove(i)
# print(len(cleaner))


for i in not_need:
    for j in Spanish:
        if i in j:
            Spanish.remove(j)
    for j in French:
        if i in j:
            French.remove(j)
    for j in Dutch:
        if i in j:
            Dutch.remove(j)


# THIS IS LETTERS IN ALL THE WORDS
all_words = cleaner
print("hi")
print(len(all_words))

length = min(len(Spanish), len(French), len(Dutch))
Spanish1 = Spanish[:length]
Dutch1 = Dutch[:length]
del Spanish
del Dutch
# print(len(Spanish1),len(French),len(Dutch1))

# Get count of each letter in a word, represented in a list


def get_count(word, letter_list):
    counts = []
    for i in letter_list:
        counts.append(word.count(i))
    return counts


# Represent all words as these lists of letter frequencies
total_lang = Spanish1 + French + Dutch1


def data_network(b):
    aggregate = []
    for i in b:
        aggregate.append(get_count(i, letters))
    return aggregate


samples = data_network(total_lang)
print("Samples")

# Make labels for each word
labels = {"es": 0, "fr": 1, "nl": 2}
language = []
for word in Spanish1:
    language.append(labels["es"])
for word in French:
    language.append(labels["fr"])
for word in Dutch1:
    language.append(labels["nl"])


# Make master list containing [word, label, count]
def create_master(b):
    master = []
    for i in range(len(b)):
        entry = []
        # entry.extend([total_lang[i]] + [language[i]] + samples[i])
        entry.extend(samples[i] + [language[i]])
        master.append(entry)
    return master


aggregate_list = create_master(total_lang)
del Spanish1
del French
del Dutch1
# free up data

test_data = np.array(aggregate_list)  # Convert to numpy
np.save("test_data.npy", test_data)
