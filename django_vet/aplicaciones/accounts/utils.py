
import re

# def validar_rut(rut):
#     rut_simple = rut.replace('.', '').replace('-', '')[:-1]
#     rut_arreglo = list(map(int, reversed(rut_simple)))

#     acumulador = 0
#     multiplo = 2
#     for digito in rut_arreglo:
#         acumulador += digito * multiplo
#         multiplo += 1
#         if multiplo > 7:
#             multiplo = 2

#     resto = acumulador % 11
#     dv_calculado = 11 - resto
#     if dv_calculado == 11:
#         dv_calculado = '0'
#     elif dv_calculado == 10:
#         dv_calculado = 'K'

#     dv_rut = rut[-1].upper()
#     if dv_rut == str(dv_calculado):
#         return True
#     else:
#         return False




    
# def validar_rut(rut):
#     rut_simple = rut.replace('.', '').replace('-', '')[:-1]
#     rut_arreglo = list(map(int, reversed(rut_simple)))

#     acumulador = 0
#     multiplo = 2
#     for digito in rut_arreglo:
#         acumulador += digito * multiplo
#         multiplo += 1
#         if multiplo > 7:
#             multiplo = 2

#     resto = acumulador % 11
#     dv_calculado = 11 - resto
#     if dv_calculado == 11:
#         dv_calculado = '0'
#     elif dv_calculado == 10:
#         dv_calculado = 'K'

#     dv_rut = rut[-1].upper()
#     if dv_rut == str(dv_calculado):
#         rut_formateado = '{}.{}.{}-{}'.format(rut[:2], rut[2:5], rut[5:8], dv_rut)
#         return rut_formateado
#     else:
#         return False


def validar_rut(rut):
    rut_simple = rut.replace('.', '').replace('-', '')[:-1]
    rut_arreglo = list(map(int, reversed(rut_simple)))
    acumulador = 0
    multiplo = 2
    for digito in rut_arreglo:
        acumulador += digito * multiplo
        multiplo += 1
        if multiplo > 7:
            multiplo = 2
    resto = acumulador % 11
    dv_calculado = 11 - resto
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'

    print('dv_calculado: ',dv_calculado)

    dv_rut = rut[-1].upper()
    if dv_rut == str(dv_calculado):
        return True
    else:
        return False
    