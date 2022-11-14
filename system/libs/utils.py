import json
import random
import re
import time
import unidecode
from datetime import datetime

from django.conf import settings
from django.contrib.auth.hashers import get_hasher
from django.template.defaultfilters import slugify
from django.utils import timezone


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(date_time):
    return int(time.mktime(date_time.timetuple()))


def string_to_int(value) -> int:
    try:
        return int(value)
    except ValueError:
        pass
    return -1


def get_timestamp():
    return int(timezone.now().timestamp())


def get_now():
    return timezone.now()


def get_equivalent_char(char):
    char = str(char).lower()
    if char == '@' or char == '4' or char == 'á':
        return 'a'
    elif char == '3' or char == '€' or char == 'é':
        return 'e'
    elif char == '1' or char == '&' or char == 'í':
        return 'i'
    elif char == '0' or char == 'ó':
        return 'o'
    elif char == 'ú':
        return 'u'
    elif char == '$':
        return 's'
    elif not char.isalpha() and not char.isnumeric():
        return ' '
    else:
        return char


def validate_text(text):
    text = str(text).lower()
    content = open(str(settings.BASE_DIR / 'system' / 'libs' / 'json' / 'denied_words.json')).read()
    words = json.loads(content)
    found = []
    new_text = ''
    for char in text:
        new_text += get_equivalent_char(char)
    new_text = re.sub(r'\s\s+', ' ', new_text)
    split = new_text.split(' ')
    for word in split:
        if word in words:
            found.append(word)
    return found


def unique_slug(name, mayor=100):
    hasher = get_hasher()
    return slugify(name)[:mayor] + '-' + str(hasher.salt())


def generate_key():
    hasher = get_hasher()
    return hasher.salt() + hasher.salt() + hasher.salt()


def generate_string(special_character=False, n=10):
    return ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789*!@#$%^&()+=:;{}[]<>?/,.-_ ') for i
        in range(0, n)) if special_character else ''.join(
        random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for i in range(0, n))


def generate_num(n=9):
    return ''.join(random.choice('0123456789') for i in range(0, n))


def remove_accents(data):
    return unidecode.unidecode(data)
