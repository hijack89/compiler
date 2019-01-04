# -*- coding: utf-8 -*-
# author:hijack89
# date:2018.11

help = """Cython Compiler 

Usage: python compiler.py file [options]

Options:
    -h, --h         show help                      
    -l              lexer
    -p              parser
    -a              assembler

Examples:
    python compiler.py -h
    python compiler.py source.c -a

"""

import sys
import getopt
import lexicalAnalysis
import syntaxAnalysis
import assemble


def lexer(content):
    lexer = lexicalAnalysis.Lexer(content)
    lexer.main()
    for token in lexer.tokens:
        print '[%s, %s]' % (token.type, token.value.replace("\n", r"\n"))


def parser(content):
    parser = syntaxAnalysis.Parser(content)
    parser.main()
    parser.display(parser.tree.root)


def assembler(file_name, content):
    assem = assemble.Assembler(file_name, content)
    assem.traverse(assem.tree.root)
    assem.ass_file_handler.generate_ass_file()


if __name__ == '__main__':
    file_name = sys.argv[1]
    option = sys.argv[2]

    if file_name:
        with open(file_name, 'r') as f:
            content = f.read()
        if option == '-l':
            lexer(content)
        elif option == '-p':
            parser(content)
        elif option == '-a':
            assembler(file_name.split(".")[0], content)
