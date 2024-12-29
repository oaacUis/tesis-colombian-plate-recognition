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
    str1 = ""
    for ele in s:
        if ele is not None:
            str1 += ele
    return str1


def split_string_language_specific(s, english=False):
    """
    Converts a string into a list of characters or words, with special handling for text directionality.

    Parameters:
    - s (str): The input string to convert.
    - english (bool, optional): Whether to split the string considering English rules. Default is False.

    Returns:
    - list: A list of characters or words, split according to the input string's language.
    """
    if english:
        res = re.split('(\d|\W)', s)
        return list(filter(None, res))

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

    Parameters:
    - license_plate (str): The license plate text to convert.
    - display (bool, optional): Whether to return the result as a display-ready string. Default is False.

    Returns:
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

    Parameters:
    - license_plate (str): The license plate text to convert.

    Returns:
    - list: A list of standard format characters.
    """
    converted_plate = []
    format_map = {v: k for k, v in params.alphabetP2.items()}
    for character in license_plate:
        character = format_map.get(unicodedata.normalize('NFKC', character))
        converted_plate.append(character)
    return converted_plate


def get_license_plate_regex(chosen_item='plateWhole'):
    """
    Retrieves regex patterns for different parts of a license plate.

    Parameters:
    - chosen_item (str, optional): The part of the license plate to get the regex for. Default is 'plateWhole'.

    Returns:
    - str: Regex pattern for the chosen item.
    """
    patterns = {
        'plateWhole': r'\d\d([a-zA-z]+)\d\d\d\d\d',
        'plateNum': r'\d\d([a-zA-z]+)\d\d\d',
        'plateCode': r'\d\d$',
    }
    return patterns.get(chosen_item, "No info available")


def clean_license_plate_text(plate_array):
    """
    Cleans and extracts valid license plate text from an input array.

    Parameters:
    - plate_array (list): The list representing parts of a license plate.

    Returns:
    - str: The cleaned license plate text.
    """
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


def check_similarity_threshold(a, b):
    """
    Checks if two strings are similar by a set threshold.

    Parameters:
    - a (str): The first string to compare.
    - b (str): The second string to compare.

    Returns:
    - bool: True if the strings are similar by at least 80%, otherwise False.
    """
    similarity = SequenceMatcher(None, a, b).ratio()
    return math.ceil(similarity * 100) >= 80


# ... Rest of the utility functions remain unchanged as they already use English ...