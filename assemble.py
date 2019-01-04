# -*- coding: utf-8 -*-
# author:hijack89
# date:2018.11

from words import *
import syntaxAnalysis

#生成汇编文件
class AssemblerFileHandler(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.result = ['.model small\n.data', '.stack', '.code\nmain:\nmov ax,@data\nmov ds,ax']
        self.printn = ["printn proc near", "mov bx,10", "mov cx,0", "yazhan: mov dx,0", "div bx", "push dx", "inc cx",
                       "cmp ax,0", "jz chuzhan", "jmp yazhan", "chuzhan: pop dx", "add dl,30h", "mov ah,2", "int 21h",
                       "loop chuzhan", "ret", "printn endp"]
        self.inputn = ['inputn proc near', 'mov bl,0', 'mov al,48', 'input_start:', 'sub al,48', 'add bl,al',
                       'mov ah,01', 'int 21h', 'cmp al,13', 'jne input_start', 'ret', 'inputn endp']
        self.printn_flag = 0
        self.inputn_flag = 0
        self.data_pointer = 1
        self.stack_pointer = 2
        self.code_pointer = 3

    def insert(self, value, _type):
        # 插入到data域
        if _type == 'DATA':
            self.result.insert(self.data_pointer, value)
            self.data_pointer += 1
            self.stack_pointer += 1
            self.code_pointer += 1
        # 插入到stack域
        elif _type == 'STACK':
            self.result.insert(self.stack_pointer, value)
            self.stack_pointer += 1
            self.code_pointer += 1
        # 插入到代码段
        elif _type == 'CODE':
            self.result.insert(self.code_pointer, value)
            self.code_pointer += 1
        else:
            print 'error!'
            exit()

    # 将结果保存到文件中
    def generate_ass_file(self):
        self.file = open(self.file_name + '.asm', 'w+')
        self.file.write('\n'.join(self.result) + '\n')
        if self.printn_flag == 1:
            self.file.write('\n'.join(self.printn) + '\n')
        if self.inputn_flag == 1:
            self.file.write('\n'.join(self.inputn) + '\n')
        self.file.write('END main\n')
        self.file.close()

#生成汇编语言
class Assembler(object):

    def __init__(self, file_name, content):
        self.parser = syntaxAnalysis.Parser(content)
        self.parser.main()
        # 生成的语法树
        self.tree = self.parser.tree
        # 要生成的汇编文件管理器
        self.ass_file_handler = AssemblerFileHandler(file_name)
        # 符号表
        self.symbol_table = {}
        # 语法类型
        self.sentence_type = ['Sentence', 'FunctionStatement', 'Print', 'Input',
                              'Statement', 'FunctionCall', 'Assignment', 'Control', 'Expression', 'Return']
        # 表达式中的符号栈
        self.operator_stack = []
        # 表达式中的操作符栈
        self.operand_stack = []
        # 已经声明了多少个label
        self.label_cnt = 0
        # ifelse中的标签
        self.labels_ifelse = {}
        # 字符串数量
        self.strn = 0

    # 函数定义句型
    def _function_statement(self, node=None):
        line = ""
        # 第一个儿子
        current_node = node.first_son
        while current_node:
            if current_node.value == 'FunctionName':
                if current_node.first_son.value == 'cython':
                    line = 'mov ah,4ch\nint 21h'
                else:
                    print 'other function defination not support.'
            elif current_node.value == 'Type':
                pass
            elif current_node.value == 'StateParameterList':
                pass
            elif current_node.value == 'Sentence':
                self.traverse(current_node.first_son)
                self.ass_file_handler.insert(line, 'CODE')
            current_node = current_node.right

    # 简单的sizeof
    def _sizeof(self, _type):
        size = -1
        if _type == 'int':
            size = 'db '
        else:
            pass
        return size

    # input语句
    def _input(self, node=None):
        line = None
        current_node = node.first_son
        if current_node.value not in self.symbol_table.keys():
            print 'input id not define.'
            exit()
        elif current_node.right:
            line = 'call inputn'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov cl,' + current_node.right.value
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov ch,0'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov di,cx'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov ' + current_node.value + '[di]' + ',bl'
            self.ass_file_handler.insert(line, 'CODE')
            self.ass_file_handler.inputn_flag = 1
        else:
            line = 'call inputn'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov ' + current_node.value + ',bl'
            self.ass_file_handler.insert(line, 'CODE')
            self.ass_file_handler.inputn_flag = 1

    # print语句
    def _print(self, node=None):
        current_node = node.first_son
        if current_node.type == '_Constant':
            current_node = node.first_son
            if current_node.type == 'String_Constant':
                line = 'str' + str(self.strn) + ' db ' + '"' + current_node.value + '","$"'
                self.strn += 1
                self.ass_file_handler.insert(line, 'DATA')
                line = 'mov dx,offset str' + str(self.strn - 1)
                self.ass_file_handler.insert(line, 'CODE')
                line = 'mov ah,9'
                self.ass_file_handler.insert(line, 'CODE')
                line = 'int 21h'
                self.ass_file_handler.insert(line, 'CODE')
            elif current_node.type == 'Digit_Constant':
                self.ass_file_handler.printn_flag = 1
                line = 'mov ' + 'ax,' + current_node.value
                self.ass_file_handler.insert(line, 'CODE')
                line = 'call printn'
                self.ass_file_handler.insert(line, 'CODE')
            # 该变量的类型
        else:
            self.ass_file_handler.printn_flag = 1
            self._expression(current_node)
            line = 'pop ax'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov ah,0'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'call printn'
            self.ass_file_handler.insert(line, 'CODE')

    # 声明语句
    def _statement(self, node=None):
        # 对应的汇编代码中的声明语句
        line = None
        # 1:初始化的，0:没有初始化
        flag = 0
        # 变量数据类型
        variable_field_type = None
        # 变量类型，是数组还是单个变量
        variable_type = None
        # 变量名
        variable_name = None
        current_node = node.first_son
        while current_node:
            array = []
            # 类型
            if current_node.value == 'Type':
                variable_field_type = current_node.first_son.value
            # 变量名
            elif current_node.type == 'IDENTIFIER':
                variable_name = current_node.value
            # 变量大小
            elif current_node.value == 'Constant':
                variable_con = current_node.first_son.value
            # 变量元素
            elif current_node.value == 'ConstantList':
                tmp_node = current_node.first_son
                # 保存该数组
                while tmp_node:
                    array.append(tmp_node.value)
                    tmp_node = tmp_node.right
            current_node = current_node.right
        if array:
            line = variable_name + ' ' + self._sizeof(variable_field_type) + ' ' + ', '.join(array)
        else:
            line = variable_name + ' ' + self._sizeof(variable_field_type) + ' ' + variable_con + ' dup(?)'
        self.ass_file_handler.insert(line, 'DATA')
        # 将该变量存入符号表
        if variable_name in self.symbol_table.keys():
            print 'variable_name "' + variable_name + '" duplicate definition.'
            exit()
        self.symbol_table[variable_name] = {'type': variable_field_type, 'con': variable_con}

    # 函数调用
    def _function_call(self, node=None):
        pass

    # 赋值语句
    def _assignment(self, node=None):
        current_node = node.first_son
        if current_node.type == 'IDENTIFIER':
            type = self.symbol_table[current_node.value]['type']
            if current_node.right.value == 'Expression':
                self._expression(current_node.right)
                # 该变量的类型
                if type == 'int':
                    line = 'pop ax'
                    self.ass_file_handler.insert(line, 'CODE')
                    line = 'mov ' + current_node.value + ',al'
                    self.ass_file_handler.insert(line, 'CODE')
                else:
                    print 'field type except int not supported!'
                    exit()
            elif current_node.right.type == 'CONSTANT':
                self._expression(current_node.right.right)
                # 该变量的类型
                if type == 'int':
                    line = 'pop ax'
                    self.ass_file_handler.insert(line, 'CODE')
                    line = 'mov cl,' + current_node.right.value
                    self.ass_file_handler.insert(line, 'CODE')
                    line = 'mov ch,0'
                    self.ass_file_handler.insert(line, 'CODE')
                    line = 'mov di,cx'
                    self.ass_file_handler.insert(line, 'CODE')
                    line = 'mov ' + current_node.value + '[' + 'di' + ']' + ',al'
                    self.ass_file_handler.insert(line, 'CODE')
                else:
                    print 'field type except int not supported!'
                    exit()
        else:
            print 'assignment wrong.'
            exit()

    # for语句
    def _control_for(self, node=None):
        current_node = node.first_son
        # 遍历的是for循环中的那个部分
        cnt = 2
        lables_for = {}
        lables_for['condition'] = 'label_' + str(self.label_cnt)
        self.label_cnt += 1
        lables_for['end'] = 'label_' + str(self.label_cnt)
        self.label_cnt += 1
        while current_node:
            # for第一部分
            if current_node.value == 'Assignment':
                self._assignment(current_node)
            # for第二、三部分
            elif current_node.value == 'Expression':
                if cnt == 2:
                    cnt += 1
                    line = lables_for['condition'] + ':'
                    self.ass_file_handler.insert(line, 'CODE')
                    self._expression(current_node)
                else:
                    self._expression(current_node)
            # for语句部分
            elif current_node.value == 'Sentence':
                self.traverse(current_node.first_son)
            current_node = current_node.right
        line = 'jmp ' + lables_for['condition']
        self.ass_file_handler.insert(line, 'CODE')
        line = lables_for['end'] + ':'
        self.ass_file_handler.insert(line, 'CODE')
        self.label_cnt += 1

    # if else语句
    def _control_if(self, node=None):
        current_node = node.first_son
        labels_ifelse = {}
        labels_ifelse['label_else'] = 'label_' + str(self.label_cnt)
        self.label_cnt += 1
        while current_node:
            if current_node.value == 'IfControl':
                if current_node.first_son.value != 'Expression' or current_node.first_son.right.value != 'Sentence':
                    print 'control_if error!'
                    exit()
                self._expression(current_node.first_son)
                self.traverse(current_node.first_son.right.first_son)
                labels_ifelse['label_end'] = 'label_' + str(self.label_cnt)
                self.label_cnt += 1
                line = 'jmp ' + labels_ifelse['label_end']
                self.ass_file_handler.insert(line, 'CODE')
                line = labels_ifelse['label_else'] + ':'
                self.ass_file_handler.insert(line, 'CODE')
            elif current_node.value == 'ElseControl':
                self.traverse(current_node.first_son)
            current_node = current_node.right

        line = labels_ifelse['label_end'] + ':'
        self.ass_file_handler.insert(line, 'CODE')

    # while语句
    def _control_while(self, node=None):
        current_node = node.first_son
        while_lable = {}
        while_lable['condition'] = 'label_' + str(self.label_cnt)
        self.label_cnt += 1
        while_lable['end'] = 'label_' + str(self.label_cnt)
        self.label_cnt += 1
        while current_node:
            if current_node.value == 'Expression':
                line = while_lable['condition'] + ':'
                self.ass_file_handler.insert(line, 'CODE')
                self._expression(current_node)
            # while语句部分
            elif current_node.value == 'Sentence':
                self.traverse(current_node.first_son)
            current_node = current_node.right

        line = 'jmp ' + while_lable['condition']
        self.ass_file_handler.insert(line, 'CODE')
        line = while_lable['end'] + ':'
        self.ass_file_handler.insert(line, 'CODE')

    # return语句
    def _return(self, node=None):
        current_node = node.first_son
        if current_node.value != 'return' or current_node.right.value != 'Expression':
            print 'return error!'
            exit()
        else:
            current_node = current_node.right
            self._expression(current_node)
            if current_node.type == 'Constant' or current_node.type == 'Variable':
                line = 'pop ax'
                self.ass_file_handler.insert(line, 'CODE')
                line = 'mov ah,0'
                self.ass_file_handler.insert(line, 'CODE')
                line = 'push ax'
                self.ass_file_handler.insert(line, 'CODE')
            else:
                print 'return type not supported!'
                exit()

    # 遍历表达式
    def _traverse_expression(self, node=None):
        if not node:
            return
        if node.type == '_Variable':
            self.operand_stack.append(
                {'type': 'VARIABLE', 'operand': node.value})
        elif node.type == 'Digit_Constant':
            self.operand_stack.append(
                {'type': 'CONSTANT', 'operand': node.value})
        elif node.type == '_Operator':
            self.operator_stack.append(node.value)
        elif node.type == '_ArrayName':
            self.operand_stack.append(
                {'type': 'ARRAY_ITEM', 'operand': [node.value, node.right.value]})
            return
        current_node = node.first_son
        while current_node:
            self._traverse_expression(current_node)
            current_node = current_node.right

    #处理双目运算
    def _Dexpression(self, node=None):
        line = None
        if node.type == 'Constant' or node.type == 'Variable' or node.type == 'ArrayItem':
            if node.type == 'ArrayItem':
                line = 'mov cl,' + node.first_son.right.value + '\n'
                line += 'mov ch,0\n'
                line += 'mov di,cx\n'
                line += 'mov al,' + node.first_son.value + '[' + '+ di' + ']\n'
            else:
                line = 'mov al,' + node.first_son.value + '\n'

        elif node.type == 'DoubleOperand':
            self._Dexpression(node.first_son)
            line = 'pop ax\n'

        operator = node.right.first_son.value
        node = node.right.right
        if node.type == 'Constant' or node.type == 'Variable' or node.type == 'ArrayItem':
            if node.type == 'ArrayItem':
                line = 'mov cl,' + node.first_son.right.value + '\n'
                line += 'mov ch,0\n'
                line += 'mov di,cx\n'
                line += 'mov bl,' + node.first_son.value + '[' + '+ di' + ']\n'
            else:
                line += 'mov bl,' + node.first_son.value + '\n'

        elif node.type == 'DoubleOperand':
            self._Dexpression(node.first_son)
            line += 'pop bx\n'

        if operator == '+':
            line += 'add al,bl\n'
        elif operator == '-':
            line += 'sub al,bl\n'
        elif operator == '*':
            line += 'mul bl\n'
        elif operator == '/':
            line += 'div bl\n'

        line += 'mov ah,0\npush ax'
        self.ass_file_handler.insert(line, 'CODE')

    # 处理单目运算
    def _Sexpression(self, node=None):
        line = None
        operator = node.first_son.first_son.value
        if operator == '++':
            line = 'inc ' + node.first_son.right.first_son.value
        elif operator == '--':
            line = 'dec ' + node.first_son.right.first_son.value
        self.ass_file_handler.insert(line, 'CODE')

    # 表达式
    def _expression(self, node=None):
        if node.type == 'Constant' or node.type == 'Variable':
            line = 'mov al,' + node.first_son.value
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov ah,0\npush ax'
            self.ass_file_handler.insert(line, 'CODE')

        elif node.type == 'ArrayItem':
            line = 'mov cl,' + node.first_son.right.value + '\n'
            line += 'mov ch,0\n'
            line += 'mov di,cx'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov al,' + node.first_son.value + '[di]'
            self.ass_file_handler.insert(line, 'CODE')
            line = 'mov ah,0\npush ax'
            self.ass_file_handler.insert(line, 'CODE')

        elif node.type == 'DoubleOperand':
            self._Dexpression(node.first_son)
        elif node.type == 'SingleOperand':
            self._Sexpression(node)
        else:
            # 先清空
            self.operator_priority = []
            self.operand_stack = []
            # 遍历该表达式
            self._traverse_expression(node)

            # 双目运算符
            compare_operators = ['>', '<', '>=', '<=']
            # 运算符对汇编指令的映射
            operator_map = {'>': 'jle ', '<': 'jge ', '>=': 'jl ', '<=': 'jg '}
            while self.operator_stack:
                operator = self.operator_stack.pop()
                if operator in compare_operators:
                    operand_b = self.operand_stack.pop()
                    operand_a = self.operand_stack.pop()

                    if operator == '>=':
                        line = 'mov ' + 'al,' + operand_a['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'mov ' + 'bl,' + operand_b['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'cmp al,bl'
                        self.ass_file_handler.insert(line, 'CODE')

                        line = operator_map['>='] + 'label_' + str(self.label_cnt - 1)
                        self.ass_file_handler.insert(line, 'CODE')

                    elif operator == '<=':
                        line = 'mov ' + 'al,' + operand_a['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'mov ' + 'bl,' + operand_b['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'cmp al,bl'
                        self.ass_file_handler.insert(line, 'CODE')

                        line = operator_map['<='] + 'label_' + str(self.label_cnt - 1)
                        self.ass_file_handler.insert(line, 'CODE')

                    elif operator == '>':
                        line = 'mov ' + 'al,' + operand_a['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'mov ' + 'bl,' + operand_b['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'cmp al,bl'
                        self.ass_file_handler.insert(line, 'CODE')

                        line = operator_map['>'] + 'label_' + str(self.label_cnt - 1)
                        self.ass_file_handler.insert(line, 'CODE')


                    elif operator == '<':
                        line = 'mov ' + 'al,' + operand_a['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'mov ' + 'bl,' + operand_b['operand']
                        self.ass_file_handler.insert(line, 'CODE')

                        line = 'cmp al,bl'
                        self.ass_file_handler.insert(line, 'CODE')

                        line = operator_map['<'] + 'label_' + str(self.label_cnt - 1)
                        self.ass_file_handler.insert(line, 'CODE')

                else:
                    print 'operator not supported!'
                    exit()
        self.expn = 1

    # 处理某一种句型
    def _handler_block(self, node=None):
        if not node:
            return
        # 下一个将要遍历的节点
        if node.value in self.sentence_type:
            # 如果是根节点
            if node.value == 'Sentence':
                self.traverse(node.first_son)
            # 函数声明
            elif node.value == 'FunctionStatement':
                self._function_statement(node)
            # 声明语句
            elif node.value == 'Statement':
                self._statement(node)
            # 函数调用
            elif node.value == 'FunctionCall':
                self._function_call(node)
            # 赋值语句
            elif node.value == 'Assignment':
                self._assignment(node)
            # 控制语句
            elif node.value == 'Control':
                if node.type == 'IfElseControl':
                    self._control_if(node)
                elif node.type == 'ForControl':
                    self._control_for(node)
                elif node.type == 'WhileControl':
                    self._control_while(node)
                else:
                    print 'control type not supported!'
                    exit()
            elif node.value == 'Input':
                self._input(node)
            elif node.value == 'Print':
                self._print(node)
            # return语句
            elif node.value == 'Return':
                self._return(node)
            else:
                print 'sentence type not supported yet.'
                exit()

    # 遍历节点
    def traverse(self, node=None):
        self._handler_block(node)
        next_node = node.right
        while next_node:
            self._handler_block(next_node)
            next_node = next_node.right
