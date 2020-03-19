import re
import sys
from enum import Enum

path = sys.argv[1]

py_code = open(path, 'r').read().split('\n')

output_code = list()
stack = list()
depth = 0


class Scopes(Enum):
    if_operator = 1
    loop_operator = 2


def line_depth(line: str):
    res = re.search('^( +)', line)
    if res:
        return round(len(res[1]) / 4)
    else:
        return 0


def replace_codewords_operators(line):
    line = re.sub('True', 'Истина', line)
    line = re.sub('False', 'Ложь', line)

    line = re.sub(' not ', ' НЕ ', line)
    line = re.sub(' and ', ' И ', line)
    line = re.sub(' or ', ' ИЛИ ', line)
    line = re.sub(' != ', ' <> ', line)
    line = re.sub(' == ', ' = ', line)

    return line


for line in py_code:
    _depth = line_depth(line)

    line = replace_codewords_operators(line)

    if re.search('(elif|else)', line) and stack[len(stack) - 1] == Scopes.loop_operator:
        new_line = ' ' * (depth - 1) * 4
        stack.pop(len(stack) - 1)
        new_line += 'КонецЦикла;'
        output_code.append(new_line)
        depth -= 1

    if _depth < depth and not re.search('(elif|else)', line):
        for i in range(depth - _depth):
            new_line = ' ' * (depth - 1 - i) * 4
            if stack.pop(len(stack) - 1) == Scopes.if_operator:
                new_line += 'КонецЕсли;'
            else:
                new_line += 'КонецЦикла;'
            output_code.append(new_line)
        depth = _depth

    if re.search('for (.+) in range\\((.+), (.+)\\):', line):
        cond = re.search('for (.+) in range\\((.+), (.+)\\):', line)
        new_line = ' ' * depth * 4
        new_line += 'Для ' + cond[1]
        new_line += ' = ' + cond[2] + ' По ' + str(int(cond[3]) - 1) + ' Цикл'
        output_code.append(new_line)

        depth += 1
        stack.append(Scopes.loop_operator)

    elif re.search('for (.+) in range\\((.+)\\):', line):
        cond = re.search('for (.+) in range\\((.+)\\):', line)
        new_line = ' ' * depth * 4
        new_line += 'Для ' + cond[1]
        new_line += ' = ' + '0' + ' По ' + str(int(cond[2]) - 1) + ' Цикл'
        output_code.append(new_line)

        depth += 1
        stack.append(Scopes.loop_operator)

    elif re.search('for (.+) in (.+):', line):
        cond = re.search('for (.+) in (.+):', line)
        new_line = ' ' * depth * 4
        new_line += 'Для Каждого ' + cond[1]
        new_line += ' Из ' + cond[2] + ' Цикл'
        output_code.append(new_line)

        depth += 1
        stack.append(Scopes.loop_operator)

    elif re.search('while (.+):', line):
        cond = re.search('while (.+):', line)
        new_line = ' ' * depth * 4
        new_line += 'Пока ' + cond[1] + ' Цикл'
        output_code.append(new_line)

        depth += 1
        stack.append(Scopes.loop_operator)

    elif re.search('elif (.+):', line):
        cond = re.search('elif (.+):', line)
        new_line = ' ' * (depth - 1) * 4
        new_line += 'ИначеЕсли ' + cond[1] + ' Тогда'
        output_code.append(new_line)

    elif re.search('if (.+):', line):
        cond = re.search('if (.+):', line)
        new_line = ' ' * depth * 4
        new_line += 'Если ' + cond[1] + ' Тогда'
        output_code.append(new_line)

        depth += 1
        stack.append(Scopes.if_operator)

    elif re.search('else:', line):
        cond = re.search('else:', line)
        new_line = ' ' * (depth - 1) * 4 + 'Иначе'
        output_code.append(new_line)

    elif not line == '':
        output_code.append(line + ';')

    else:
        output_code.append(line)

with open('output.txt', 'w') as f:
    for line in output_code:
        f.write("%s\n" % line)
