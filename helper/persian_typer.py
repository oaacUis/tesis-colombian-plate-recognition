# persian_typer.py
"""
Module for handling text typing and character position-based formatting.
Converts between standard and formatted text using English alphabet.
"""

def type_persian(value):
    """
    Process and format text with proper character connections.

    Args:
        value (str): Input text to be formatted

    Returns:
        str: Formatted text with proper character connections
    """
    # Split input text into words
    words = value.split(" ")
    
    # Clean empty spaces
    i = 0
    while i < len(words):
        if words[i] in ["", " "]:
            words.remove(words[i])
        elif " " in words[i]:
            words.remove("#$#$#$#$#|")
        else:
            i += 1

    # Process each word
    for word_index in range(len(words)):
        char_position = 0
        formatted_word = ""
        last_char = ""
        
        # Process each character in the word
        for current_char in words[word_index]:
            char_position += 1
            
            # Format first character
            if not last_char:
                if char_position == 1:
                    current_char = checker_do_not_use(current_char, "start")
                elif char_position == len(words[word_index]):
                    current_char = checker_do_not_use(current_char, "end")
                else:
                    current_char = checker_do_not_use(current_char, "center")
            
            # Format subsequent characters
            else:
                if char_position == 1:
                    current_char = checker_do_not_use(current_char, "start")
                elif char_position == len(words[word_index]):
                    # Check for non-connecting characters
                    non_connecting_chars = ["A", "V", "D", "Z", "R", "O", "E", "W"]
                    if any(char in last_char for char in non_connecting_chars):
                        current_char = checker_do_not_use(current_char, "endPlus")
                    else:
                        current_char = checker_do_not_use(current_char, "end")
                else:
                    # Check for non-connecting characters
                    non_connecting_chars = ["A", "V", "D", "Z", "R", "O", "E", "W"]
                    if any(char in last_char for char in non_connecting_chars):
                        current_char = checker_do_not_use(current_char, "start")
                    else:
                        current_char = checker_do_not_use(current_char, "center")
            
            last_char = current_char
            formatted_word += current_char
        
        words[word_index] = formatted_word[::-1]

    # Combine words in reverse order
    result = " ".join(reversed(words))
    result = result[::-1].replace(" ", "", 1)[::-1]
    
    return result


def checker_do_not_use(character, position):
    """
    Convert characters to their position-specific forms using English alphabet.

    Args:
        character (str): Single character to convert
        position (str): Position type ('start', 'center', 'end', or 'endPlus')

    Returns:
        str: Converted character in its position-specific form
    """
    # Character mappings for different positions
    position_mappings = {
        "start": {
            "A": "A", "V": "V", "B": "B", "P": "P", "T": "T", "S": "S",
            "J": "J", "C": "C", "H": "H", "K": "K", "D": "D", "Z": "Z",
            "R": "R", "X": "X", "Q": "Q", "W": "W", "E": "E", "F": "F",
            "G": "G", "Y": "Y", "U": "U", "I": "I", "O": "O", "L": "L",
            "M": "M", "N": "N"
        },
        "center": {
            "A": "A", "V": "V", "B": "B", "P": "P", "T": "T", "S": "S",
            "J": "J", "C": "C", "H": "H", "K": "K", "D": "D", "Z": "Z",
            "R": "R", "X": "X", "Q": "Q", "W": "W", "E": "E", "F": "F",
            "G": "G", "Y": "Y", "U": "U", "I": "I", "O": "O", "L": "L",
            "M": "M", "N": "N"
        },
        "end": {
            "A": "A", "V": "V", "B": "B", "P": "P", "T": "T", "S": "S",
            "J": "J", "C": "C", "H": "H", "K": "K", "D": "D", "Z": "Z",
            "R": "R", "X": "X", "Q": "Q", "W": "W", "E": "E", "F": "F",
            "G": "G", "Y": "Y", "U": "U", "I": "I", "O": "O", "L": "L",
            "M": "M", "N": "N"
        },
        "endPlus": {
            "A": "A", "V": "V", "B": "B", "P": "P", "T": "T", "S": "S",
            "J": "J", "C": "C", "H": "H", "K": "K", "D": "D", "Z": "Z",
            "R": "R", "X": "X", "Q": "Q", "W": "W", "E": "E", "F": "F",
            "G": "G", "Y": "Y", "U": "U", "I": "I", "O": "O", "L": "L",
            "M": "M", "N": "N"
        }
    }

    # Get the appropriate mapping for the position
    mapping = position_mappings.get(position, {})
    
    # Return the converted character or the original if no mapping exists
    return mapping.get(character.upper(), character)