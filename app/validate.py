import re
import datetime


def email(value):
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
        return True
    else:
        return False


def name(value):
    if re.match(r"^[a-zA-Zа-яА-ЯіІїЇЬь']{3,50}$", value):
        return True
    else:
        return False


def phone(value):
    if re.match(r"^[0-9]{12}$", value):
        return True
    else:
        return False


def adress(value):
    if re.match(r".{3,30}, .{1,3}, .{3,30}$", value):
        return True
    else:
        return False


def passwd(value):
    if re.match(r".{6,64}$", value):
        return True
    else:
        return False


def hash(value):
    if re.match(r"^[A-Fa-f0-9]{64}$", value):
        return True
    else:
        return False


def description(value):
    if re.match(r"^[a-zA-Zа-яА-ЯіІїЇЬь\.\,\-\№\s*\d]{3,100}$", value):
        return True
    else:
        return False


def location(value):
    if re.match(r"^([1-9]{1,2}\.[0-9]+),([1-9]{1,2}\.[0-9]+)$", value):
        return True
    else:
        return False


def worktime(value):
    if re.match(r"^(([0-1][0-9]|[2][3]):[0-5][0-9])-(([0-1][0-9]|[2][3]):[0-5][0-9])$", value):
        return True
    else:
        return False


def date(value):
    if re.match(r"^(19[5-9][0-9]|20[0-4][0-9]|2050)[/](0?[1-9]|1[0-2])[/](0?[1-9]|[12][0-9]|3[01])$", value):
        return True
    else:
        return False


def format_date(value):
    return datetime.datetime.strptime(value, "%Y/%m/%d")


def date_time(value):
    if re.match(
            r"^(0?[1-9]|[12][0-9]|3[01])-(0?[1-9]|1[0-2])-\d\d\d\d (00|[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9])$",
            value):
        return True
    else:
        return False


def format_date_time(value):
    return datetime.datetime.strptime(value, "%d-%m-%y %H:%M")


def blood_type(value):
    if re.match(r"^-?[1-4]$", value):
        return True
    else:
        return False


def file_type(value):
    if re.match(r"^.+\.(png|jpg|jpeg)$", value):
        return True
    else:
        return False


if __name__ == '__main__':
    print(email('asd@adasd.com'))
    print(date('1997/01/09'))
    print(name('Кіра'))
    print(phone('380971151577'))
    print(adress('Івана Франка, 30, Івано-Франківськ'))
    print('date_time', date_time('05-02-2018 23:33'))
    print('blood_type', blood_type('2'))
    print('file_type', file_type('asasdasdd.png'))

