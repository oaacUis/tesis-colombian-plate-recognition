# text_decorators.py

import math
import re
import unicodedata
from difflib import SequenceMatcher

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
    Converts standard characters in a license plate to a simple string format.

    Parameters:
    - license_plate (list or str): The license plate text to convert. Can be a list of characters or a string.
    - display (bool, optional): Whether to return the result as a display-ready string. Default is False.

    Returns:
    - str: The converted license plate as a string.

    Example:
        >>> convert_to_local_format(['8', 'X', 'O', '9', '8', '8'])
        '8XO988'
    """
    # Si la entrada es una lista, convertir directamente a string
    if isinstance(license_plate, list):
        plate_string = ''.join(str(char) for char in license_plate)
        if display:
            return reshape_text(plate_string)
        return plate_string
    
    # Mantener la funcionalidad original para entradas que no son listas
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

