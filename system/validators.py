from telnetlib import PRAGMA_HEARTBEAT
from django.core.exceptions import ValidationError

from system.libs.utils import string_to_int
from system.libs.validators import (equals, validate_empty, validate_max_length,
                                    validate_only_letters_numbers, validate_only_numbers, validate_only_letters)


class Validator:
    @staticmethod
    def db_is_valid(data: dict) -> bool:
        try:
            # Validamos el nombre (255, solo letras y numeros)
            nombre = data.get('nombre', None)
            validate_empty(nombre)
            validate_max_length(nombre, 255)
            validate_only_letters_numbers(nombre)
            # Rasgos
            for rasgo in data.get('rasgos', []):
                # - Nombre (50, solo letras y numeros)
                rasgo_nombre = rasgo.get('nombre', None)
                validate_empty(rasgo_nombre)
                validate_max_length(rasgo_nombre, 50)
                validate_only_letters_numbers(rasgo_nombre)
                # - Tipo de Criterio (0-3)
                criterio = string_to_int(rasgo.get('criterio', -1))
                if criterio == -1 or 0 > criterio > 3:
                    raise ValueError('Criterio invalido!')
                # - Dominio
                last_value_interval = None
                for dominio in rasgo.get('dominio'):
                    if criterio == 0:
                        # - Nominal (150, solo letras)
                        validate_empty(dominio)
                        validate_max_length(dominio, 150)
                        validate_only_letters(dominio)
                        
                    elif criterio == 1:
                        # - Booleano (Booleanos)
                        if dominio not in ["No", "Si"]:
                            raise ValidationError('Criterio booleano invalido!')
                    elif criterio == 2:
                        # - Cuantitativo (Numeros)
                        validate_empty(dominio)
                        validate_only_numbers(dominio)
                        pass
                    else:  # DEMACIADO TRAUMAAAAAA!!!!!!! MUCHOS LLOROS!!!! T_T
                        # - Intervalos (2 numeros de tal a cual)
                        intervalo = dominio.split('-')
                        first, second = string_to_int(intervalo[0]), string_to_int(intervalo[1])
                        # Comprobamos los valores de los intervalos
                        if first >= second:
                            raise ValidationError('Intervalo "' + str(first) + '-' + str(second) + '" esta incorrecto!')
                        # Comprobar ultimo intervalo
                        if last_value_interval is not None and last_value_interval >= first:
                            raise ValidationError('Intervalo "' + str(first) + '-' + str(second) + '" fuera de intervalo!')
                        last_value_interval = second
                equals(rasgo.get('dominio'))
        except ValidationError:
            return False
        return True
