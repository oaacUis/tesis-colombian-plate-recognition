# text_decorators.py

import math
import re
import unicodedata
from difflib import SequenceMatcher
from itertools import groupby

import arabic_reshaper
from bidi.algorithm import get_display

from configParams import Parameters

params = Parameters()


def join_elements(s):
    """
    Concatenate list elements into a single string, ignoring None values.

    Parameters:
    - s (list): The list of elements to concatenate.

    Returns:
    - str: A single string result of concatenating all list elements.
    """
<<<<<<< HEAD

=======
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    str1 = ""
    for ele in s:
        if ele is not None:
            str1 += ele
    return str1


<<<<<<< HEAD
def split_string_language_specific(s, english=True):
    """
    Converts a string into a list of characters or words, with special handling for Arabic text.
=======
def split_string_language_specific(s, english=False):
    """
    Converts a string into a list of characters or words, with special handling for text directionality.
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388

    Parameters:
    - s (str): The input string to convert.
    - english (bool, optional): Whether to split the string considering English rules. Default is False.

    Returns:
    - list: A list of characters or words, split according to the input string's language.
    """
    if english:
        res = re.split('(\d|\W)', s)
        return list(filter(None, res))

<<<<<<< HEAD
    # reshaped_text = arabic_reshaper.reshape(s)
    # f = get_display(reshaped_text)
    # returning_list = []
    # chars_list = ""
    # words = list(f.strip())
    # for word in words:
    #     if str(word).isdigit() is True and len(chars_list) == 0:
    #         returning_list.append(word)
    #     elif str(word).isdigit() is False:
    #         chars_list += word
    #     elif str(word).isdigit() is True:
    #         returning_list.append(chars_list)
    #         chars_list = ""
    #         returning_list.append(word)
    # return returning_list


def reshape_persian_text(string):
    """
    Transforms Persian script for correct display in environments that do not support Arabic text shaping.

    Parameters:
    - string (str): The Persian text to be reshaped and displayed correctly.

    Returns:
    - str: The reshaped Persian text.
    """
    reshaped_text = arabic_reshaper.reshape(string)  # correct its shape
    return get_display(reshaped_text)


def convert_english_to_persian(license_plate, display=False):
    """
    Converts English characters in a license plate to Persian equivalents.
=======
    reshaped_text = arabic_reshaper.reshape(s)
    f = get_display(reshaped_text)
    returning_list = []
    chars_list = ""
    words = list(f.strip())
    for word in words:
        if str(word).isdigit() and len(chars_list) == 0:
            returning_list.append(word)
        elif not str(word).isdigit():
            chars_list += word
        elif str(word).isdigit():
            returning_list.append(chars_list)
            chars_list = ""
            returning_list.append(word)
    return returning_list


def reshape_text(string):
    """
    Transforms text for correct display in environments that do not support bidirectional text shaping.

    Parameters:
    - string (str): The text to be reshaped and displayed correctly.

    Returns:
    - str: The reshaped text.
    """
    reshaped_text = arabic_reshaper.reshape(string)
    return get_display(reshaped_text)


def convert_to_local_format(license_plate, display=False):
    """
    Converts standard characters in a license plate to local format.
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388

    Parameters:
    - license_plate (str): The license plate text to convert.
    - display (bool, optional): Whether to return the result as a display-ready string. Default is False.

    Returns:
<<<<<<< HEAD
    - str: The converted license plate with Persian characters.
    """
    second_license_plate = []
    for character in license_plate:
        if character.isdigit() is True:
            character = unicodedata.name(character)[6:]
        else:
            pass
        character = params.alphabetP.get(character)
        second_license_plate.append(character)
    plateString = join_elements(second_license_plate)
    if display:
        return reshape_persian_text(plateString)

    return plateString


def convert_persian_to_english(license_plate):
    """
    Converts Persian characters in a license plate to English equivalents.
=======
    - str: The converted license plate in local format.
    """
    converted_plate = []
    for character in license_plate:
        if character.isdigit():
            character = unicodedata.name(character)[6:]
        character = params.alphabetP.get(character)
        converted_plate.append(character)
    plate_string = join_elements(converted_plate)
    if display:
        return reshape_text(plate_string)
    return plate_string


def convert_to_standard_format(license_plate):
    """
    Converts local format characters in a license plate to standard format.
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388

    Parameters:
    - license_plate (str): The license plate text to convert.

    Returns:
<<<<<<< HEAD
    - list: A list of English characters equivalent to the Persian input.
    """
    second_license_plate = []
    inv_map = {v: k for k, v in params.alphabetP2.items()}
    for character in license_plate:
        character = inv_map.get(unicodedata.normalize('NFKC', character))
        second_license_plate.append(character)
    return second_license_plate
=======
    - list: A list of standard format characters.
    """
    converted_plate = []
    format_map = {v: k for k, v in params.alphabetP2.items()}
    for character in license_plate:
        character = format_map.get(unicodedata.normalize('NFKC', character))
        converted_plate.append(character)
    return converted_plate
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388


def get_license_plate_regex(chosen_item='plateWhole'):
    """
    Retrieves regex patterns for different parts of a license plate.

    Parameters:
    - chosen_item (str, optional): The part of the license plate to get the regex for. Default is 'plateWhole'.

    Returns:
    - str: Regex pattern for the chosen item.
    """
<<<<<<< HEAD
    info_dict = {
        'plateWhole': r'([a-zA-z]+)\d\d\d',
        'plateNum': r'\d\d\d',
        'plateCode': r'$\d\d\d',
    }
    return info_dict.get(chosen_item, "No info available")


def clean_license_plate_text(plateArray):
=======
    patterns = {
        'plateWhole': r'\d\d([a-zA-z]+)\d\d\d\d\d',
        'plateNum': r'\d\d([a-zA-z]+)\d\d\d',
        'plateCode': r'\d\d$',
    }
    return patterns.get(chosen_item, "No info available")


def clean_license_plate_text(plate_array):
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
    """
    Cleans and extracts valid license plate text from an input array.

    Parameters:
<<<<<<< HEAD
    - plateArray (list): The list representing parts of a license plate.
=======
    - plate_array (list): The list representing parts of a license plate.
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388

    Returns:
    - str: The cleaned license plate text.
    """
<<<<<<< HEAD
    plateString = join_elements(plateArray)
    if len(plateArray) == 4:
        plateStrTemp = re.search(get_license_plate_regex('plateNum'), plateString)
    elif len(plateArray) == 2:
        plateStrTemp = re.match(get_license_plate_regex('plateCode'), plateString)
    else:
        plateStrTemp = re.match(get_license_plate_regex('plateWhole'), plateString)

    if plateStrTemp is not None:
        if plateStrTemp.group(0):
            plateString = plateStrTemp.group(0)
    else:
        plateString = ''
    return plateString


def convert_persian_numbers(text):
    """
    Converts Persian numbers to their English equivalents in a string.

    Parameters:
    - text (str): The string containing Persian numbers.

    Returns:
    - str: The converted string with English numbers.
    """
    persiannumber = text
    number = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
    }

    for i, j in number.items():
        persiannumber = persiannumber.replace(i, j)

    return persiannumber
=======
    plate_string = join_elements(plate_array)
    if len(plate_array) == 6:
        plate_temp = re.search(get_license_plate_regex('plateNum'), plate_string)
    elif len(plate_array) == 2:
        plate_temp = re.match(get_license_plate_regex('plateCode'), plate_string)
    else:
        plate_temp = re.match(get_license_plate_regex('plateWhole'), plate_string)

    if plate_temp is not None and plate_temp.group(0):
        return plate_temp.group(0)
    return ''


def convert_numbers_to_standard(text):
    """
    Converts local format numbers to standard format in a string.

    Parameters:
    - text (str): The string containing local format numbers.

    Returns:
    - str: The converted string with standard numbers.
    """
    number_map = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }
    for local, standard in number_map.items():
        text = text.replace(local, standard)
    return text
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388


def check_similarity_threshold(a, b):
    """
    Checks if two strings are similar by a set threshold.

    Parameters:
    - a (str): The first string to compare.
    - b (str): The second string to compare.

    Returns:
    - bool: True if the strings are similar by at least 80%, otherwise False.
    """
<<<<<<< HEAD
    s = SequenceMatcher(None, a, b).ratio()
    s = math.ceil(s * 100)
    if s >= 80:
        return True
    else:
        return False


def find_longest_common_substring(s1, s2):
    """
    Finds the longest common substring between two strings.

    Parameters:
    - s1 (str): The first string.
    - s2 (str): The second string.

    Returns:
    - str: The longest common substring found.
    """
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def calculate_similarity_percentage(s1, s2):
    """
    Computes the similarity percentage between two strings based on the longest common substring.

    Parameters:
    - s1 (str): The first string.
    - s2 (str): The second string.

    Returns:
    - float: The similarity percentage between the two strings.
    """
    return 2. * len(find_longest_common_substring(s1, s2)) / (len(s1) + len(s2)) * 100


import jellyfish
import difflib

a = '46L21299'
b = '46L21399'

c = '73T13877'
d = '72T13877'

e = '86T46637'
f = '86T46627'

g = '65Sad92124'
h = '65Sin92124'

dif = difflib.Differ()


def print_string_similarity_measures(aa, bb):
    """
    Prints various similarity measures and edit distances between two strings.

    Parameters:
    - aa (str): The first string.
    - bb (str): The second string.
    """
    diff = dif.compare(aa, bb)
    print(1, math.ceil(calculate_similarity_percentage(aa, bb)))
    print(2, math.ceil(check_similarity_threshold(aa, bb) * 100))
    print(3, jellyfish.damerau_levenshtein_distance(aa, bb))
    print(4, list(diff))


def convert_string_to_ascii(s):
    """
    Converts a string to its equivalent ASCII value representation.

    Parameters:
    - s (str): The string to convert.

    Returns:
    - int: The ASCII value of the input string.
    """

    x = 0
    for i in range(len(s)):
        x += ord(s[i]) * 2 ** (8 * (len(s) - i - 1))
    return x


sss = ['4', '4', 'PuV', '1', '5', '4', '2', '5']
vvv = '۹۲۱۲۴الف۶۵'
ttt = '77PuV88899'
lll = '۲۴۳۵۲ﺁ۳۴'
eee = '۵۵پو۷۷۷۱۱'
ccc = 'ﻒﻟﺍ'

res = [''.join(g) for _, g in groupby(lll, str.isalpha)]

resE = ''.join(r'\u{:04X}'.format(ord(chr)) for chr in lll)

res = re.split('(\d|\W)', ttt)
results = list(filter(None, res))

time_infos = [x for x in re.split('(\d|\W)', vvv) if x]
=======
    similarity = SequenceMatcher(None, a, b).ratio()
    return math.ceil(similarity * 100) >= 80


# ... Rest of the utility functions remain unchanged as they already use English ...
>>>>>>> ced2859ed93f5909c9251f160af885b41bca2388
