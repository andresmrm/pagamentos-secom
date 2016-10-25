#!/usr/bin/env python3
# coding: utf-8

import re

apelidos = {
    'Globo': [
        'GLOBO COMUNICAÇÃO E PARTICIPAÇÕES S/A',
        'GLOBO COMUNICAÇÃO E PARTICIPAÇÕES SA',
        'GLOBO COMUNICAÇÃO E PARTICIPAÇÕES S.A.',
        'GLOBOSAT PROGRAMADORA LTDA',
        'INFOGLOBO COMUNICACÃO E PARTICIPAÇÕES S/A',
        'TELECINE PROGRAMAÇÃO DE FILMES LTDA',
        'RÁDIO GLOBO DE SÃO PAULO LTDA',
        'RÁDIO GLOBO S/A',
        'EDITORA GLOBO S/A',
        'EDIÇÕES GLOBO CONDE NAST S/A',
        'RADIO EXCELSIOR S/A ',
        'VALOR ECONOMICO S/A',
        'RÁDIO GLOBO ELDORADO LTDA',
        'RÁDIO GLOBO IJUI LTDA',
        'CANAL BRAZIL S/A',
    ],
    'Turner': [
        'TURNER BROADCASTING SYSTEM LATIN AMERICA INC',
        'TURNER INTERNATIONAL DO BRASIL LTDA',
    ],
    'Microsoft': [
        'MICROSOFT INFORMATICA LTDA',
        'MICROSOFT DO BRASIL IMPORTAÇÃO E COMÉRCIO DE SOFTWARE E VÍDEO GAMES LTDA'
    ],
    'Record': [
        'RADIO E TELEVISAO RECORD S.A',
        'RÁDIO E TELEVISÃO RECORD S.A',
    ],
    'Folha': [
        'EMPRESA FOLHA DA MANHÃ S/A',
    ],
    'Estadão': [
        'S/A O ESTADO DE S.PAULO',
    ],
    'Abril': [
        'ABRIL COMUNICAÇÕES S/A',
        'EDITORA ABRIL S.A',
        'EDITORA CARAS S/A',
        'ABRIL RADIODIFUSÃO S/A',
    ],
    'SBT': [
        'TV SBT CANAL 4 DE SÃO PAULO S.A',
    ],
    'Band': [
        'RADIO E TELEVISAO BANDEIRANTES SA',
        'METRO JORNAL S.A.',
    ],
    'Facebook': [
        'FACEBOOK SERVICOS ONLINE DO BRASIL LTDA',
    ],
    'UOL': [
        'UNIVERSO ONLINE S.A',
    ],
    'RedeTV': [
        'TV ÔMEGA LTDA',
    ],
    'JovenPan': [
        'RADIO PANAMERICANA S/A',
    ],
    'Yahoo': [
        'YAHOO! DO BRASIL INTERNET LTDA',
    ],
    'Telefônica': [
        'TERRA NETWORKS BRASIL SA',
        'TERRA NETWORKS BRASIL S.A.',
    ],
    'Fox': [
        'FOX LATIN AMERICAN CHANNELS DO BRASIL LTDA',
    ]
}

# reverter
reverso = {}
for apelido, formais in apelidos.items():
    for formal in formais:
        reverso[formal] = apelido


def generalizar(nome):
    '''
    Faz alguns processamentos no nome e tenta substituí-lo por
    um dos grupos, caso faça parte de algum.
    '''
    # remove espaços e CPFs
    nome = re.sub(
        '(CPF)?\s?(\d{11})|(\d{3}\.\d{3}\.\d{3}-\d{2})',
        '', nome.strip())
    return reverso.get(nome, nome)
