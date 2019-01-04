# -*- coding: utf-8 -*-
# author:hijack89
# date:2018.11

from words import *


class Token(object):
    '''记录分析出来的单词'''

    def __init__(self, type_index, value):
        if type_index == 'key':
            self.type = DETAIL_TOKEN_STYLE[value]
        else:
            self.type = DETAIL_TOKEN_STYLE[type_index]
        self.value = value


# 词法分析器
class Lexer(object):

    def __init__(self, content):
        # 用来保存词法分析出来的结果
        self.tokens = []
        self.content = content

    # 判断当前字符是否是空白字符
    def is_blank(self, index):
        if self.content[index] == ' ' or self.content[index] == '\t' or self.content[index] == '\r':
            return True
        else:
            return False

    # 若当前字符是空白符则跳过
    def skip_blank(self, index):
        while index < len(self.content) and self.is_blank(index):
            index += 1
        return index

    # 判断是否是关键字
    def is_keyword(self, value):
        for item in keywords:
            if value in item:
                return True
        return False

    # 词法分析主程序
    def main(self):
        i = 0
        while i < len(self.content):
            i = self.skip_blank(i)
            #跳过注释
            if self.content[i] == '#':
                while self.content[i] != '\n':
                    i += 1
                i += 1
            # 如果是字母或者是以下划线开头
            if self.content[i].isalpha() or self.content[i] == '_':
                # 找到该字符串
                temp = ''
                while i < len(self.content) and (
                        self.content[i].isalpha() or
                        self.content[i] == '_' or
                        self.content[i].isdigit()):
                    temp += self.content[i]
                    i += 1
                # 判断该字符串
                if self.is_keyword(temp):
                    self.tokens.append(Token('key', temp))
                else:
                    self.tokens.append(Token('id', temp))
                i = self.skip_blank(i)
            # 如果是数字开头
            elif self.content[i].isdigit():
                temp = ''
                while i < len(self.content):
                    if self.content[i].isdigit():
                        temp += self.content[i]
                        i += 1
                    else:
                        break
                self.tokens.append(Token('digit', temp))
                i = self.skip_blank(i)
            # 如果是分隔符
            elif self.content[i] in delimiters:
                self.tokens.append(Token('key', self.content[i]))
                # 如果是字符串常量
                if self.content[i] == '\"':
                    i += 1
                    temp = ''
                    while i < len(self.content):
                        if self.content[i] != '\"':
                            temp += self.content[i]
                            i += 1
                        else:
                            break
                    else:
                        print 'error:lack of \"'
                        exit()
                    self.tokens.append(Token('string', temp))
                    self.tokens.append(Token('key', '\"'))
                i = self.skip_blank(i + 1)
            # 如果是运算符
            elif self.content[i] in operators:
                # 如果是++或者--
                if (self.content[i] == '+' or self.content[i] == '-') and (
                        self.content[i + 1] == self.content[i]):
                    self.tokens.append(Token('key', self.content[i] * 2))
                    i = self.skip_blank(i + 2)
                # 如果是>=或者<=
                elif (self.content[i] == '>' or self.content[i] == '<') and self.content[i + 1] == '=':
                    self.tokens.append(Token('key', self.content[i] + '='))
                    i = self.skip_blank(i + 2)
                # 其他
                else:
                    self.tokens.append(Token('key', self.content[i]))
                    i = self.skip_blank(i + 1)
