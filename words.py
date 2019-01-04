# -*- coding: utf-8 -*-
# author:hijack89
# date:2018.11

# 将关键字、运算符、分隔符进行具体化
DETAIL_TOKEN_STYLE = {
    'id': 'IDENTIFIER',
    'digit': 'DIGIT_CONSTANT',
    'string': 'STRING_CONSTANT',
    'int': 'INT',
    'for': 'FOR',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'input': 'INPUT',
    'print': 'PRINT',
    'return': 'RETURN',
    '=': 'ASSIGN',
    '<': 'LT',
    '>': 'GT',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MUL',
    '/': 'DIV',
    '++': 'SELF_PLUS',
    '--': 'SELF_MINUS',
    '>=': 'GET',
    '<=': 'LET',
    '(': 'LL_BRACKET',
    ')': 'RL_BRACKET',
    '{': 'LB_BRACKET',
    '}': 'RB_BRACKET',
    '[': 'LM_BRACKET',
    ']': 'RM_BRACKET',
    ',': 'COMMA',
    '"': 'DOUBLE_QUOTE',
    '\n': 'NEWLINE',
    ';': 'SEMICOLON',
    '#': 'SHARP'
}

# 关键字
keywords = [
    ['int'],
    ['if', 'for', 'while', 'else'], ['input', 'print', 'return'],
]

# 运算符
operators = [
    '=', '<', '>', '++', '--', '+', '-', '*', '/', '>=', '<='
]

# 分隔符
delimiters = ['(', ')', '{', '}', '[', ']', ',', '\"', '\n', ';']
