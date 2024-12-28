# gui_maker.py


import functools

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QImage, QPixmap, Qt, QScreen
from PySide6.QtWidgets import QLabel, QTableWidgetItem, QAbstractItemView, QVBoxLayout, QDialog, QApplication, \
    QTableWidget

from configParams import getFieldNames
from helper import jalali
from helper.text_decorators import *


class CenterAlignDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate for aligning table items to the center.
    """

    def initStyleOption(self, option, index):
        super(CenterAlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter


class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
    """
    Custom delegate to make table cells read-only.
    """

    def createEditor(self, *args, **kwargs):
        return


def create_image_label(image):
    """
    Creates a QLabel with a given image.

    Parameters:
    - image (QPixmap): Image to display on the label.

    Returns:
    - QLabel: A label widget displaying the given image.
    """
    imageLabel = QLabel()
    imageLabel.setText("")
    imageLabel.setScaledContents(True)
    imageLabel.setFixedSize(200, 44)
    imageLabel.setPixmap(image)
    return imageLabel


def create_styled_button(type):
    """
    Generates a styled QPushButton based on the specified type.

    Parameters:
    - type (str): The type of button, e.g., 'edit', 'delete'.

    Returns:
    - QPushButton: The styled button.
    """
    button = QtWidgets.QPushButton()
    button.setFlat(True)
    button.setStyleSheet("QPushButton { background-color: transparent; border: 0px }")
    if type == 'edit':
        button.setIcon(QPixmap("./icons/icons8-edit-80.png"))
    elif type == 'delete':
        button.setIcon(QPixmap("./icons/icons8-trash-can-80.png"))
    elif type == 'info':
        button.setIcon(QPixmap("./icons/icons8-info-80.png"))
    elif type == 'add':
        button.setIcon(QPixmap("./icons/icons8-add-80.png"))
    elif type == 'search':
        button.setIcon(QPixmap("./icons/icons8-find-user-male-80.png"))
    button.setIconSize(QSize(24, 24))
    return button


def get_status_color(number):
    """
    Returns RGB color based on a status number.

    Parameters:
    - number (int): The status number.

    Returns:
    - tuple: (R, G, B) color values.
    """
    if number == 0:
        return 224, 27, 36
    elif number == 1:
        return 51, 209, 122
    elif number == 2:
        return 246, 211, 45


def get_status_text(number):
    """
    Converts a status number to its corresponding text.

    Parameters:
    - number (int): The status number.

    Returns:
    - str: The status text.
    """
    if int(number) == 0:
        return 'غیر مجاز'
    elif int(number) == 1:
        return 'مجاز'
    elif int(number) == 2:
        return 'ثبت نشده'


def configure_edit_table_widget(self):
    """
    Configures table widget for editing mode.
    """
    fieldsList = ['status', 'plateNum', 'time', 'date', 'platePic', 'charPercent', 'platePercent', 'moreInfo', 'addNew']

    fieldsList = getFieldNames(fieldsList)

    self.tableWidget.setColumnCount(len(fieldsList))
    self.tableWidget.setRowCount(20)
    self.tableWidget.setHorizontalHeaderLabels(fieldsList)
    self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    self.tableWidget.setLayoutDirection(Qt.RightToLeft)
    self.tableWidget.setSortingEnabled(True)

    delegate = CenterAlignDelegate(self.tableWidget)
    self.tableWidget.setItemDelegate(delegate)
    self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
    self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)


def configure_main_table_widget(self):
    """
       Configures the main table widget.
       """
    fieldsList = ['status', 'plateNum', 'time', 'date', 'platePic', 'moreInfo', 'addNew']

    fieldsList = getFieldNames(fieldsList)

    self.tableWidget.setColumnCount(len(fieldsList))
    self.tableWidget.setRowCount(20)
    self.tableWidget.setHorizontalHeaderLabels(fieldsList)
    self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    self.tableWidget.setLayoutDirection(Qt.RightToLeft)
    self.tableWidget.setSortingEnabled(True)

    delegate = CenterAlignDelegate(self.tableWidget)
    self.tableWidget.setItemDelegate(delegate)
    self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
    self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)


def populate_main_table_with_data(self, dfReadEnteries):
    """
      Populates the main table widget with data.

      Parameters:
      - dfReadEnteries (DataFrame): The DataFrame containing table data.
      """
    delegate = CenterAlignDelegate(self.tableWidget)
    self.tableWidget.setItemDelegate(delegate)
    for each_row in range(len(dfReadEnteries)):
        statusItem = dfReadEnteries.iloc[each_row][0]

        r, g, b = get_status_color(statusItem)
        statusText = get_status_text(statusItem)

        self.tableWidget.setItem(each_row, 0, QTableWidgetItem(statusText))
        self.tableWidget.item(each_row, 0).setBackground(QColor(r, g, b))

        self.tableWidget.setItem(each_row, 1,
                                 QTableWidgetItem(convert_to_local_format(
                                     (split_string_language_specific(dfReadEnteries.iloc[each_row][1])))))
        self.tableWidget.setItem(each_row, 2, QTableWidgetItem((dfReadEnteries.iloc[each_row][2])))
        self.tableWidget.setItem(each_row, 3,
                                 QTableWidgetItem(jalali.Gregorian(dfReadEnteries.iloc[each_row][3]).persian_string()))

        Image = QImage()
        Image.load(dfReadEnteries.iloc[each_row][4])
        QcroppedPlate = QPixmap.fromImage(Image)

        item = create_image_label(QcroppedPlate)
        item.mousePressEvent = functools.partial(on_label_double_click, source_object=item)

        self.tableWidget.setCellWidget(each_row, 4, item)
        self.tableWidget.setRowHeight(each_row, 44)

        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)


def center_widget(wid):
    """
       Centers a widget on the screen.

       Parameters:
       - wid (QWidget): The widget to be centered.
       """
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = wid.frameGeometry()
    geo.moveCenter(center)
    wid.move(geo.topLeft())


def on_label_double_click(event, source_object=None):
    """
       Handles double-click event on label to show image in a dialog.

       Parameters:
       - event: The mouse event.
       - source_object: The source label object containing the pixmap.
       """
    w = QDialog()
    w.setFixedSize(600, 132)
    w.setWindowTitle("نمایش پلاک")

    imageLabel = QLabel(w)
    imageLabel.setText("")
    imageLabel.setScaledContents(True)
    imageLabel.setFixedSize(600, 132)
    imageLabel.setPixmap(source_object.pixmap())

    layout = QVBoxLayout()
    layout.addWidget(imageLabel)
    w.exec()














































    #Text decoration 
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
    Converts a string into a list of characters or words, with special handling for Arabic text.

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
        if str(word).isdigit() is True and len(chars_list) == 0:
            returning_list.append(word)
        elif str(word).isdigit() is False:
            chars_list += word
        elif str(word).isdigit() is True:
            returning_list.append(chars_list)
            chars_list = ""
            returning_list.append(word)
    return returning_list


def reshape_text(string):
    """
    Transforms Persian script for correct display in environments that do not support Arabic text shaping.

    Parameters:
    - string (str): The Persian text to be reshaped and displayed correctly.

    Returns:
    - str: The reshaped Persian text.
    """
    reshaped_text = arabic_reshaper.reshape(string)  # correct its shape
    return get_display(reshaped_text)


def convert_to_local_format(license_plate, display=False):
    """
    Converts English characters in a license plate to Persian equivalents.

    Parameters:
    - license_plate (str): The license plate text to convert.
    - display (bool, optional): Whether to return the result as a display-ready string. Default is False.

    Returns:
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
        return reshape_text(plateString)

    return plateString


def convert_to_standard_format(license_plate):
    """
    Converts Persian characters in a license plate to English equivalents.

    Parameters:
    - license_plate (str): The license plate text to convert.

    Returns:
    - list: A list of English characters equivalent to the Persian input.
    """
    second_license_plate = []
    inv_map = {v: k for k, v in params.alphabetP2.items()}
    for character in license_plate:
        character = inv_map.get(unicodedata.normalize('NFKC', character))
        second_license_plate.append(character)
    return second_license_plate


def get_license_plate_regex(chosen_item='plateWhole'):
    """
    Retrieves regex patterns for different parts of a license plate.

    Parameters:
    - chosen_item (str, optional): The part of the license plate to get the regex for. Default is 'plateWhole'.

    Returns:
    - str: Regex pattern for the chosen item.
    """
    info_dict = {
        'plateWhole': r'\d\d([a-zA-z]+)\d\d\d\d\d',
        'plateNum': r'\d\d([a-zA-z]+)\d\d\d',
        'plateCode': r'\d\d$',
    }
    return info_dict.get(chosen_item, "No info available")


def clean_license_plate_text(plateArray):
    """
    Cleans and extracts valid license plate text from an input array.

    Parameters:
    - plateArray (list): The list representing parts of a license plate.

    Returns:
    - str: The cleaned license plate text.
    """
    plateString = join_elements(plateArray)
    if len(plateArray) == 6:
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


def convert_numbers_to_standard(text):
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


def check_similarity_threshold(a, b):
    """
    Checks if two strings are similar by a set threshold.

    Parameters:
    - a (str): The first string to compare.
    - b (str): The second string to compare.

    Returns:
    - bool: True if the strings are similar by at least 80%, otherwise False.
    """
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










































#jalali.py
import datetime
import re


class Gregorian:

    def __init__(self, *date):
        if len(date) == 1:
            date = date[0]
            if type(date) is str:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    raise Exception("Invalid Input String")
            elif type(date) is datetime.date:
                [year, month, day] = [date.year, date.month, date.day]
            elif type(date) is tuple:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                raise Exception("Invalid Input Type")
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            raise Exception("Invalid Input")
        try:
            datetime.datetime(year, month, day)
        except:
            raise Exception("Invalid Date")

        self.gregorian_year = year
        self.gregorian_month = month
        self.gregorian_day = day
        d_4 = year % 4
        g_a = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        doy_g = g_a[month] + day
        if d_4 == 0 and month > 2:
            doy_g += 1
        d_33 = int(((year - 16) % 132) * .0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 10) / 63) == 30:
            a -= 1
            b += 1
        if doy_g > b:
            jy = year - 621
            doy_j = doy_g - b
        else:
            jy = year - 622
            doy_j = doy_g + a
        if doy_j < 187:
            jm = int((doy_j - 1) / 31)
            jd = doy_j - (31 * jm)
            jm += 1
        else:
            jm = int((doy_j - 187) / 30)
            jd = doy_j - 186 - (jm * 30)
            jm += 7
        self.persian_year = jy
        self.persian_month = jm
        self.persian_day = jd

    def persian_tuple(self):
        return self.persian_year, self.persian_month, self.persian_day

    def persian_string(self, date_format="{}-{}-{}"):
        return date_format.format(self.persian_year, self.persian_month, self.persian_day)


class Persian:

    def __init__(self, *date):
        if len(date) == 1:
            date = date[0]
            if type(date) is str:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', date)
                if m:
                    [year, month, day] = [int(m.group(1)), int(m.group(2)), int(m.group(3))]
                else:
                    raise Exception("Invalid Input String")
            elif type(date) is tuple:
                year, month, day = date
                year = int(year)
                month = int(month)
                day = int(day)
            else:
                raise Exception("Invalid Input Type")
        elif len(date) == 3:
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
        else:
            raise Exception("Invalid Input")
        if year < 1 or month < 1 or month > 12 or day < 1 or day > 31 or (month > 6 and day == 31):
            raise Exception("Incorrect Date")

        self.persian_year = year
        self.persian_month = month
        self.persian_day = day
        d_4 = (year + 1) % 4
        if month < 7:
            doy_j = ((month - 1) * 31) + day
        else:
            doy_j = ((month - 7) * 30) + day + 186
        d_33 = int(((year - 55) % 132) * .0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 19) / 63) == 20:
            a -= 1
            b += 1
        if doy_j <= a:
            gy = year + 621
            gd = doy_j + b
        else:
            gy = year + 622
            gd = doy_j - a
        for gm, v in enumerate([0, 31, 29 if (gy % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gd <= v:
                break
            gd -= v

        self.gregorian_year = gy
        self.gregorian_month = gm
        self.gregorian_day = gd

    def gregorian_tuple(self):
        return self.gregorian_year, self.gregorian_month, self.gregorian_day

    def gregorian_string(self, date_format="{}-{}-{}"):
        return date_format.format(self.gregorian_year, self.gregorian_month, self.gregorian_day)

    def gregorian_datetime(self):
        return datetime.date(self.gregorian_year, self.gregorian_month, self.gregorian_day)

























































#Persian_typer.py
def type_persian(value):
    splitv = value.split(" ")
    i = 0
    while i < len(splitv):
        if splitv[i] == "":
            splitv[i] = ""
            splitv.remove("")
        elif splitv[i] == " ":
            splitv[i] = " "
            splitv.remove(" ")
        elif " " in splitv[i]:
            splitv[i] = " "
            splitv[i] = "#$#$#$#$#|"
            splitv.remove("#$#$#$#$#|")
        i = i + 1
    b = 0
    while b < len(splitv):
        q = 0
        word = ""
        lastw = ""
        splitv[b] = splitv[b]
        for txt in splitv[b]:
            q = q + 1
            if lastw == "":
                if q == 1:
                    txt = checker_do_not_use(txt, "start")
                elif q == len(splitv[b]):
                    txt = checker_do_not_use(txt, "end")
                elif q > len(splitv[b]):
                    txt = checker_do_not_use(txt, "end")
                else:
                    txt = checker_do_not_use(txt, "center")

            else:
                if q == 1:
                    txt = checker_do_not_use(txt, "start")
                elif q == len(splitv[b]):
                    if "ا" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "آ" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "د" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ذ" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ر" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ز" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ژ" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "و" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    else:
                        txt = checker_do_not_use(txt, "end")
                elif q > len(splitv[b]):
                    if "ا" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "آ" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "د" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ذ" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ر" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ز" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "ژ" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    elif "و" in lastw:
                        txt = checker_do_not_use(txt, "endPlus")
                    else:
                        txt = checker_do_not_use(txt, "end")
                else:
                    if "ا" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "آ" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "د" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "ذ" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "ر" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "ز" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "ژ" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    elif "و" in lastw:
                        txt = checker_do_not_use(txt, "start")
                    else:
                        txt = checker_do_not_use(txt, "center")
            lastw = txt
            word = word + txt
        word = word[::-1]
        splitv[b] = word
        b = b + 1
    l = len(splitv)
    all_txt = ""
    while 0 < l:
        m = l - 1
        all_txt = all_txt + splitv[m] + " "
        l = l - 1
    editor = all_txt
    editor = editor[::-1]
    editor = editor.replace(" ", "", 1)
    editor = editor[::-1]
    all_txt = editor
    return all_txt


def checker_do_not_use(string, value):
    if (value == "start"):
        string = string.replace("ا", "ﺍ")
        string = string.replace("آ", "ﺁ")
        string = string.replace("ب", "ﺑ")
        string = string.replace("پ", "ﭘ")
        string = string.replace("ت", "ﺗ")
        string = string.replace("ث", "ﺛ")
        string = string.replace("ج", "ﺟ")
        string = string.replace("چ", "ﭼ")
        string = string.replace("ح", "ﺣ")
        string = string.replace("خ", "ﺧ")
        string = string.replace("د", "ﺩ")
        string = string.replace("ذ", "ﺫ")
        string = string.replace("ر", "ﺭ")
        string = string.replace("ز", "ﺯ")
        string = string.replace("ژ", "ﮊ")
        string = string.replace("س", "ﺳ")
        string = string.replace("ش", "ﺷ")
        string = string.replace("ص", "ﺻ")
        string = string.replace("ض", "ﺿ")
        string = string.replace("ط", "ﻃ")
        string = string.replace("ظ", "ﻇ")
        string = string.replace("ع", "ﻋ")
        string = string.replace("غ", "ﻏ")
        string = string.replace("ف", "ﻓ")
        string = string.replace("ق", "ﻗ")
        string = string.replace("ک", "ﮐ")
        string = string.replace("گ", "ﮔ")
        string = string.replace("ل", "ﻟ")
        string = string.replace("م", "ﻣ")
        string = string.replace("ن", "ﻧ")
        string = string.replace("و", "ﻭ")
        string = string.replace("ه", "ﻫ")
        string = string.replace("ی", "ﯾ")
    elif (value == "center"):
        string = string.replace("ا", "ﺎ")
        string = string.replace("آ", "ﺁ")
        string = string.replace("ب", "ﺒ")
        string = string.replace("پ", "ﭙ")
        string = string.replace("ت", "ﺘ")
        string = string.replace("ث", "ﺜ")
        string = string.replace("ج", "ﺠ")
        string = string.replace("چ", "ﭽ")
        string = string.replace("ح", "ﺤ")
        string = string.replace("خ", "ﺨ")
        string = string.replace("د", "ﺪ")
        string = string.replace("ذ", "ﺬ")
        string = string.replace("ر", "ﺮ")
        string = string.replace("ز", "ﺰ")
        string = string.replace("ژ", "ﮋ")
        string = string.replace("س", "ﺴ")
        string = string.replace("ش", "ﺸ")
        string = string.replace("ص", "ﺼ")
        string = string.replace("ض", "ﻀ")
        string = string.replace("ط", "ﻄ")
        string = string.replace("ظ", "ﻈ")
        string = string.replace("ع", "ﻌ")
        string = string.replace("غ", "ﻐ")
        string = string.replace("ف", "ﻔ")
        string = string.replace("ق", "ﻘ")
        string = string.replace("ک", "ﮑ")
        string = string.replace("گ", "ﮕ")
        string = string.replace("ل", "ﻠ")
        string = string.replace("م", "ﻤ")
        string = string.replace("ن", "ﻨ")
        string = string.replace("و", "ﻮ")
        string = string.replace("ه", "ﻬ")
        string = string.replace("ی", "ﯿ")
    elif (value == "end"):
        string = string.replace("ا", "ﺍ")
        string = string.replace("آ", "ﺁ")
        string = string.replace("ب", "ﺐ")
        string = string.replace("پ", "ﭗ")
        string = string.replace("ت", "ﺖ")
        string = string.replace("ث", "ﺚ")
        string = string.replace("ج", "ﺞ")
        string = string.replace("چ", "ﭻ")
        string = string.replace("ح", "ﺢ")
        string = string.replace("خ", "ﺦ")
        string = string.replace("د", "ﺩ")
        string = string.replace("ذ", "ﺫ")
        string = string.replace("ر", "ﺭ")
        string = string.replace("ز", "ﺯ")
        string = string.replace("ژ", "ژ")
        string = string.replace("س", "ﺲ")
        string = string.replace("ش", "ﺶ")
        string = string.replace("ص", "ﺺ")
        string = string.replace("ض", "ﺾ")
        string = string.replace("ط", "ﻂ")
        string = string.replace("ظ", "ﻆ")
        string = string.replace("ع", "ﻊ")
        string = string.replace("غ", "ﻎ")
        string = string.replace("ف", "ﻒ")
        string = string.replace("ق", "ﻖ")
        string = string.replace("ک", "ﮏ")
        string = string.replace("گ", "ﮓ")
        string = string.replace("ل", "ﻞ")
        string = string.replace("م", "م")
        string = string.replace("ن", "ﻥ")
        string = string.replace("و", "ﻭ")
        string = string.replace("ه", "ﻩ")
        string = string.replace("ی", "ﯼ")
    elif (value == "endPlus"):
        string = string.replace("ا", "ﺍ")
        string = string.replace("آ", "ﺁ")
        string = string.replace("ب", "ب")
        string = string.replace("پ", "پ")
        string = string.replace("ت", "ت")
        string = string.replace("ث", "ث")
        string = string.replace("ج", "ج")
        string = string.replace("چ", "چ")
        string = string.replace("ح", "ح")
        string = string.replace("خ", "خ")
        string = string.replace("د", "د")
        string = string.replace("ذ", "ذ")
        string = string.replace("ر", "ر")
        string = string.replace("ز", "ز")
        string = string.replace("ژ", "ژ")
        string = string.replace("س", "س")
        string = string.replace("ش", "ش")
        string = string.replace("ص", "ص")
        string = string.replace("ض", "ض")
        string = string.replace("ط", "ط")
        string = string.replace("ظ", "ظ")
        string = string.replace("ع", "ع")
        string = string.replace("غ", "غ")
        string = string.replace("ف", "ف")
        string = string.replace("ق", "ق")
        string = string.replace("ک", "ک")
        string = string.replace("گ", "گ")
        string = string.replace("ل", "ل")
        string = string.replace("م", "م")
        string = string.replace("ن", "ن")
        string = string.replace("و", "و")
        string = string.replace("ه", "ه")
        string = string.replace("ی", "ی")
    return string





















































#Home-yolo.py
# home-yolo.py

"""
Main script to run the License Plate Recognition (LPR) application. This application
uses deep learning models to detect and recognize license plates and characters.
It is built with PySide6 for the GUI and utilizes PyTorch for model inference.

Requirements:
- PySide6 for the GUI
- PyTorch for deep learning inference
- Pillow for image processing
- OpenCV for video and image manipulation
"""

import functools
import gc
import statistics
import time
import warnings
from pathlib import Path
import torch
from PIL import ImageOps
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal, QSize
from PySide6.QtGui import QImage, QIcon, QAction, QPainter
from PySide6.QtWidgets import QTableWidgetItem, QGraphicsScene
from qtpy.uic import loadUi

import ai.img_model as imgModel
from ai.img_model import *
from configParams import Parameters
from database.db_entries_utils import db_entries_time, dbGetAllEntries
from database.db_resident_utils import db_get_plate_status, db_get_plate_owner_name
from enteries_window import EnteriesWindow
from helper.gui_maker import configure_main_table_widget, create_image_label, on_label_double_click, center_widget, \
    get_status_text, get_status_color, \
    create_styled_button
from helper.text_decorators import convert_to_local_format, clean_license_plate_text, join_elements, \
    convert_to_standard_format, split_string_language_specific
from resident_view import residentView
from residents_edit import residentsAddNewWindow
from residents_main import residentsWindow

warnings.filterwarnings("ignore", category=UserWarning)
params = Parameters()
import sys

sys.path.append('yolov5')


def get_device():
    """
    Determines the device to run the PyTorch models on.
    Returns a torch.device object representing the device (CUDA, MPS, or CPU).
    """
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


modelPlate = torch.hub.load('yolov5', 'custom', params.modelPlate_path, source='local', force_reload=True)
# modelPlate = modelPlate.to(device())

modelCharX = torch.hub.load('yolov5', 'custom', params.modelCharX_path, source='local', force_reload=True)


# modelCharX = modelCharX.to(device())

class MainWindow(QtWidgets.QMainWindow):
    """
    The main window class of the LPR application.
    It sets up the user interface and connects signals and slots.
    """

    def __init__(self):
        """
       Initializes the main window and its components.
       """
        super(MainWindow, self).__init__()
        loadUi('./gui/mainFinal.ui', self)
        self.setFixedSize(self.size())

        self.camImage = None
        self.plateImage = None
        self.residentsWindow = None
        self.enterieswindow = None
        self.startButton.clicked.connect(self.start_webcam)
        self.stopButton.clicked.connect(self.stop_webcam)
        self.usersListButton.clicked.connect(self.show_residents_list)
        self.enteriesListButton.clicked.connect(self.show_entries_list)

        exitAct = QAction("Exit", self)
        exitAct.setShortcut("Ctrl+Q")

        self.startButton.setIcon(QPixmap("./icons/icons8-play-80.png"))
        self.startButton.setIconSize(QSize(40, 40))

        self.stopButton.setIcon(QPixmap("./icons/icons8-stop-80.png"))
        self.stopButton.setIconSize(QSize(40, 40))

        self.usersListButton.setIcon(QPixmap("./icons/icons8-people-64.png"))
        self.usersListButton.setIconSize(QSize(40, 40))

        self.enteriesListButton.setIcon(QPixmap("./icons/icons8-car-80.png"))
        self.enteriesListButton.setIconSize(QSize(40, 40))

        self.settingsButton.setIcon(QPixmap("./icons/icons8-tools-80.png"))
        self.settingsButton.setIconSize(QSize(40, 40))

        self.plateTextView.setStyleSheet(
            f"""border-image: url("{Path().absolute()}/Templates/template-base.png") 0 0 0 0 stretch stretch;""")

        self.Worker1 = Worker1()
        self.Worker1.plateDataUpdate.connect(self.on_plate_data_update)
        self.Worker1.mainViewUpdate.connect(self.on_main_view_update)

        self.Worker2 = Worker2()
        self.Worker2.mainTableUpdate.connect(self.refresh_table)
        self.Worker2.start()

        configure_main_table_widget(self)
        self.scene = QGraphicsScene()
        self.gv.setScene(self.scene)

        torch.cuda.empty_cache()
        gc.collect()

    def refresh_table(self, plateNum=''):

        # Get all entries from the database with a limit of 10 and where the plate number is like the given plate number
        plateNum = dbGetAllEntries(limit=10, whereLike=plateNum)
        # Set the number of rows in the table widget to the length of the plate number list
        self.tableWidget.setRowCount(len(plateNum))
        # Iterate through the plate number list
        for index, entry in enumerate(plateNum):
            # Get the plate number in English
            plateNum2 = join_elements(
                convert_to_standard_format(split_string_language_specific(entry.getPlateNumber(display=True))))
            # Get the plate status from the database
            statusNum = db_get_plate_status(plateNum2)
            # Set the status of the entry in the table widget
            self.tableWidget.setItem(index, 0, QTableWidgetItem(entry.getStatus(statusNum=statusNum)))
            # Set the plate number of the entry in the table widget
            self.tableWidget.setItem(index, 1, QTableWidgetItem(entry.getPlateNumber(display=True)))
            # Set the time of the entry in the table widget
            self.tableWidget.setItem(index, 2, QTableWidgetItem(entry.getTime()))
            # Set the date of the entry in the table widget
            self.tableWidget.setItem(index, 3, QTableWidgetItem(entry.getDate()))

            # Load the plate picture
            Image = QImage()
            Image.load(entry.getPlatePic())
            # Create a QcroppedPlate from the Image
            QcroppedPlate = QPixmap.fromImage(Image)

            # Create an image label from the QcroppedPlate
            item = create_image_label(QcroppedPlate)
            # Set a mouse press event to on_label_double_click
            item.mousePressEvent = functools.partial(on_label_double_click, source_object=item)
            # Set the cell widget of the table widget to the image label
            self.tableWidget.setCellWidget(index, 4, item)
            # Set the row height of the table widget to 44
            self.tableWidget.setRowHeight(index, 44)

            # Create an info button
            infoBtnItem = create_styled_button('info')
            # Set a mouse press event to on_info_button_clicked
            infoBtnItem.mousePressEvent = functools.partial(self.on_info_button_clicked, source_object=infoBtnItem)
            # Set the cell widget of the table widget to the info button
            self.tableWidget.setCellWidget(index, 5, infoBtnItem)

            # Create an add button
            addBtnItem = create_styled_button('add')
            # Set a mouse press event to on_add_button_clicked
            addBtnItem.mousePressEvent = functools.partial(self.on_add_button_clicked, source_object=addBtnItem)
            # Set the cell widget of the table widget to the add button
            self.tableWidget.setCellWidget(index, 6, addBtnItem)
            # Disable the add button
            addBtnItem.setEnabled(False)

            # If the status is 2, enable the add button and disable the info button
            if statusNum == 2:
                addBtnItem.setEnabled(True)
                infoBtnItem.setEnabled(False)

    def on_info_button_clicked(self, event, source_object=None):
        r = self.tableWidget.currentRow()
        field1 = self.tableWidget.item(r, 1)
        residentView(residnetPlate=field1.text()).exec()

    def on_add_button_clicked(self, event, source_object=None):
        r = self.tableWidget.currentRow()
        field1 = self.tableWidget.item(r, 1)
        residentAddWindow = residentsAddNewWindow(self, isNew=True,
                                                  residnetPlate=field1.text())
        residentAddWindow.exec()
        self.refresh_table()

    def closeEvent(self, event):
        """### IT OVERRIDES closeEvent from PySide6"""
        if self.residentsWindow is not None and self.enterieswindow is not None:
            self.residentsWindow.close()
            self.enterieswindow.close()  # TODO if not openned any window will crash
        event.accept()

    def show_residents_list(self):
        residentsMain = residentsWindow()
        center_widget(residentsMain)
        residentsMain.exec()
        self.Worker2.start()

    def show_entries_list(self):
        enterieswindow = EnteriesWindow()
        center_widget(enterieswindow)
        enterieswindow.exec()

    def on_main_view_update(self, mainViewImage):

        qp = QPixmap.fromImage(mainViewImage)

        self.scene.addPixmap(qp)
        self.scene.setSceneRect(0, 0, 960, 540)
        self.gv.fitInView(self.scene.sceneRect())
        self.gv.setRenderHints(QPainter.Antialiasing)

    def on_plate_data_update(self, cropped_plate: QImage, plate_text: str, char_conf_avg: float,
                             plate_conf_avg: float) -> None:

        # Check if the plate text is 8 characters long and the character confidence is above 70
        if len(plate_text) == 8 and char_conf_avg >= 70:
            # Set the plate view to display the cropped plate
            self.plate_view.setScaledContents(True)
            self.plate_view.setPixmap(QPixmap.fromImage(cropped_plate))

            # Convert the plate text to Persian and set the text for the plate number and plate text in Persian
            plt_text_num = convert_to_local_format(plate_text[:6], display=True)
            plt_text_ir = convert_to_local_format(plate_text[6:], display=True)
            self.plate_text_num.setText(plt_text_num)
            self.plate_text_ir.setText(plt_text_ir)

            # Clean the plate text and get the status from the database
            plate_text_clean = clean_license_plate_text(plate_text)
            status = db_get_plate_status(plate_text_clean)

            # Update the plate owner and permission
            self.update_plate_owner(db_get_plate_owner_name(plate_text_clean))
            self.update_plate_permission(status)

            # Create data for send into services
            external_service_data = {
                'plate_number': plt_text_num + '-' + plt_text_ir,
                'image': cropped_plate
            }
            # Add the plate text, character confidence, plate confidence, cropped plate, and status to the database
            db_entries_time(plate_text_clean, char_conf_avg, plate_conf_avg, cropped_plate, status,
                            external_service_data=external_service_data)
            self.Worker2.start()

    def update_plate_owner(self, name):
        if name:
            self.plate_owner_name_view.setText(name)
        else:
            self.plate_owner_name_view.setText('')

    def update_plate_permission(self, status):
        r, g, b = get_status_color(status)
        statusText = get_status_text(status)

        self.plate_permission_view.setText(statusText)
        self.plate_permission_view.setStyleSheet("background-color: rgb({}, {}, {});".format(r, g, b))

    def start_webcam(self):
        if not self.Worker1.isRunning():
            self.Worker1.start()
        else:
            self.Worker1.unPause()

    def stop_webcam(self):
        self.Worker1.stop()


class Worker1(QThread):
    """
    Worker thread that handles frame grabbing and processing in the background.
    It is responsible for detecting plates and recognizing characters.
    """
    mainViewUpdate = Signal(QImage)
    plateDataUpdate = Signal(QImage, list, int, int)
    TotalFramePass = 0

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.prepare_capture()
        while self.ThreadActive:
            success, frame = self.Capture.read()
            if success:
                self.process_frame(frame)
                self.manageFrameRate()

    def prepare_capture(self):
        self.prev_frame_time = 0
        self.ThreadActive = True
        """
        # you can change 0 in >>>cv2.VideoCapture(0)<<< (which is webcam) to params.video
        # and it will read the config.ini >>> video = anpr_video.mp4
        # you should add your file path instead of anpr_video.mp4
        # if you want to use stream just replace your address in config.ini 
        >>> rtps = rtsp://172.17.0.1:8554/webCamStream
        """
        self.Capture = cv2.VideoCapture(params.video) # (params.rtps)  # 0 -> use for local webcam
        self.adjust_video_position()

    def adjust_video_position(self):
        if params.source == 'video':
            total = int(self.Capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.TotalFramePass = 0 if self.TotalFramePass > total else self.TotalFramePass
            self.Capture.set(1, self.TotalFramePass)

    def process_frame(self, frame):
        self.TotalFramePass += 1
        resize = self.prepareImage(frame)

        platesResult = modelPlate(resize).pandas().xyxy[0]
        for _, plate in platesResult.iterrows():
            plateConf = int(plate['confidence'] * 100)
            if plateConf >= 90:
                self.highlightPlate(resize, plate)
                croppedPlate = self.cropPlate(resize, plate)
                plateText, char_detected, charConfAvg = self.detectPlateChars(croppedPlate)
                self.emitPlateData(croppedPlate, plateText, char_detected, charConfAvg, plateConf)

        self.emitFrame(resize)

    def prepareImage(self, frame):
        resize = cv2.resize(frame, (960, 540))
        effect = ImageOps.autocontrast(imgModel.to_img_pil(resize), cutoff=1)
        return cv2.cvtColor(imgModel.to_img_opencv(effect), cv2.COLOR_BGR2RGB)

    def highlightPlate(self, resize, plate):
        cv2.rectangle(resize, (int(plate['xmin']) - 3, int(plate['ymin']) - 3),
                      (int(plate['xmax']) + 3, int(plate['ymax']) + 3),
                      color=(0, 0, 255), thickness=3)

    def cropPlate(self, resize, plate):
        return resize[int(plate['ymin']): int(plate['ymax']), int(plate['xmin']): int(plate['xmax'])]

    def emitPlateData(self, croppedPlate, plateText, char_detected, charConfAvg, plateConf):
        croppedPlate = cv2.resize(croppedPlate, (600, 132))
        croppedPlateImage = QImage(croppedPlate.data, croppedPlate.shape[1], croppedPlate.shape[0],
                                   QImage.Format_RGB888)
        self.plateDataUpdate.emit(croppedPlateImage, plateText, charConfAvg, plateConf)

    def manageFrameRate(self):
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - self.prev_frame_time)
        self.prev_frame_time = new_frame_time
        self.currentFPS = fps  # Save the current FPS for later drawing on the frame

    def emitFrame(self, resize):
        if hasattr(self, 'currentFPS'):  # Check if currentFPS has been calculated
            imgModel.draw_fps(resize, self.currentFPS)  # Draw FPS on the frame
        mainFrame = QImage(resize.data, resize.shape[1], resize.shape[0], QImage.Format_RGB888)
        self.mainViewUpdate.emit(mainFrame)

    def detectPlateChars(self, croppedPlate):
        chars, confidences, char_detected = [], [], []
        results = modelCharX(croppedPlate)
        detections = results.pred[0]
        detections = sorted(detections, key=lambda x: x[0])  # sort by x coordinate
        for det in detections:
            conf = det[4]
            if conf > 0.5:
                cls = det[5].item()
                char = params.char_id_dict.get(str(int(cls)), '')
                chars.append(char)
                confidences.append(conf.item())
                char_detected.append(det.tolist())
        charConfAvg = round(statistics.mean(confidences) * 100) if confidences else 0
        return ''.join(chars), char_detected, charConfAvg

    def unPause(self):
        self.ThreadActive = True

    def stop(self):
        self.ThreadActive = False


class Worker2(QThread):
    mainTableUpdate = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        self.mainTableUpdate.emit()
        time.sleep(.5)

    def unPause(self):
        self.ThreadActive = True

    def stop(self):
        self.ThreadActive = False


def get_platform():
    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


if __name__ == "__main__":
    # QApplication.setAttribute(Qt.AA_UseSoftwareOpenGL) # OpenGL issue, Use before creating the QCoreApplication.
    app = QtWidgets.QApplication(sys.argv)

    app.setStyle('Windows')

    window = MainWindow()
    window.setWindowIcon(QIcon("./icons/65th_xs.png"))
    window.setIconSize(QSize(16, 16))
    center_widget(window)
    window.show()
    sys.exit(app.exec())
