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
        
        # Convert Gregorian to Persian date
        d_4 = year % 4
        gregorian_days = [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        day_of_year_gregorian = gregorian_days[month] + day
        if d_4 == 0 and month > 2:
            day_of_year_gregorian += 1
        d_33 = int(((year - 16) % 132) * .0305)
        a = 286 if (d_33 == 3 or d_33 < (d_4 - 1) or d_4 == 0) else 287
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 10) / 63) == 30:
            a -= 1
            b += 1
        if day_of_year_gregorian > b:
            persian_year = year - 621
            day_of_year_persian = day_of_year_gregorian - b
        else:
            persian_year = year - 622
            day_of_year_persian = day_of_year_gregorian + a
        if day_of_year_persian < 187:
            persian_month = int((day_of_year_persian - 1) / 31)
            persian_day = day_of_year_persian - (31 * persian_month)
            persian_month += 1
        else:
            persian_month = int((day_of_year_persian - 187) / 30)
            persian_day = day_of_year_persian - 186 - (persian_month * 30)
            persian_month += 7
        self.persian_year = persian_year
        self.persian_month = persian_month
        self.persian_day = persian_day

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
        
        # Convert Persian to Gregorian date
        d_4 = (year + 1) % 4
        if month < 7:
            day_of_year_persian = ((month - 1) * 31) + day
        else:
            day_of_year_persian = ((month - 7) * 30) + day + 186
        d_33 = int(((year - 55) % 132) * .0305)
        a = 287 if (d_33 != 3 and d_4 <= d_33) else 286
        if (d_33 == 1 or d_33 == 2) and (d_33 == d_4 or d_4 == 1):
            b = 78
        else:
            b = 80 if (d_33 == 3 and d_4 == 0) else 79
        if int((year - 19) / 63) == 20:
            a -= 1
            b += 1
        if day_of_year_persian <= a:
            gregorian_year = year + 621
            gregorian_day = day_of_year_persian + b
        else:
            gregorian_year = year + 622
            gregorian_day = day_of_year_persian - a
        for gregorian_month, v in enumerate([0, 31, 29 if (gregorian_year % 4 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
            if gregorian_day <= v:
                break
            gregorian_day -= v

        self.gregorian_year = gregorian_year
        self.gregorian_month = gregorian_month
        self.gregorian_day = gregorian_day

    def gregorian_tuple(self):
        return self.gregorian_year, self.gregorian_month, self.gregorian_day

    def gregorian_string(self, date_format="{}-{}-{}"):
        return date_format.format(self.gregorian_year, self.gregorian_month, self.gregorian_day)

    def gregorian_datetime(self):
        return datetime.date(self.gregorian_year, self.gregorian_month, self.gregorian_day)