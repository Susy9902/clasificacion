import json
import re
from django.core.exceptions import ValidationError
from .utils import validate_text


def validate_only_letters(value):
    p = re.compile(u"[a-zA-ZñÑáéíóú_ ]+$")
    m = p.match(value)
    if not m:
        raise ValidationError('Admite solo caracteres alfabéticos (Letras).')
    words = validate_text(value)
    if words:
        raise ValidationError('El Formulario contiene las siquientes malas palabras: ' + ', '.join(words) + '.')


def validate_only_numbers(value):
    p = re.compile(u"[-0-9]+$")
    m = p.match(str(value))
    if not m:
        raise ValidationError('Introduzca un valor numérico (Numeros).')


def validate_only_letters_numbers(value):
    p = re.compile(u"[a-zA-ZñÑáéíóú0-9_ ]+$")
    m = p.match(value)
    if not m:
        raise ValidationError('Admite solo caracteres alfanuméricos (Letras y Numeros).')
    words = validate_text(value)
    if words:
        raise ValidationError('El Formulario contiene las siquientes malas palabras: ' + ', '.join(words) + '.')


# Example: validate_expression('[0-9]+')('123')
def validate_expression(expression):
    def innerfn(value):
        p = re.compile(u"" + expression + "$")
        m = p.match(value)
        if not m:
            raise ValidationError('Ajústese al siguiente formato: ' + expression)

    return innerfn


def validate_empty(value):
    if not bool(value and not value.isspace()):
        raise ValidationError('El campo esta vacio')


def validate_max_length(value, max_length):
    if len(value) > max_length:
        raise ValidationError('Supera el maximo de: ' + str(max_length))


def validate_bad_words(value):
    words = validate_text(value)
    if words:
        raise ValidationError('El Formulario contiene las siquientes malas palabras: ' + ', '.join(words) + '.')


def file_size(value):
    try:
        limit = 2048 * 1024  # 2mb
        if value.size > limit:
            raise ValidationError('Foto muy grande. Excede a 2MB')
    except FileNotFoundError:
        pass


def json_validator(value):
    try:
        return json.loads(value)
    except Exception:
        raise ValidationError('La informacion no es un JSON')

def equals(array):
    for i in range(len(array)):
        for j in range(len(array)):
            if i==j:
                continue
            if array[i] == array[j]:
                raise ValidationError('Valores de dominios iguales')
