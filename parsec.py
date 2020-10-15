from parsita import *
from parsita.util import constant
import sys


def add_tab(str):
    return '\t' + '\t'.join(str.splitlines(True))


def print_nothing(x):
    return ''


def print_newline(x):
    return '\n'.join(x)


def print_atom(x):
    return 'atom\n' + add_tab('\n'.join(x))


class PrologParser(TextParsers, whitespace=r'[ \t\n\r]*'):
    keyword_module = lit('module') > print_nothing
    keyword_type = lit('type') > print_nothing

    dot = lit('.') > print_nothing
    cork = lit(':-') > print_nothing
    arrow = lit('->') > print_nothing
    disj_sep = lit(';') > print_nothing
    conj_sep = lit(',') > print_nothing
    left_br = lit('(') > print_nothing
    right_br = lit(')') > print_nothing

    var = reg(r'[A-Z][a-zA-Z_0-9]*') > (lambda x: 'variable = ' + x)
    ident = pred(reg(r'[a-z_][a-zA-Z_0-9]*'), lambda x: x != 'module' and x != 'type',
                 'identifier which is not a keyword') > (lambda x: 'identifier = ' + x)

    atom = (atom_body > print_atom) | (ident > (lambda x: ''.join(x)))
    atom_body = (ident & (rep1(bracket_atom | ident | var) > print_newline))
    bracket_atom = (((left_br & bracket_atom & right_br) > (lambda x: ''.join(x[1]))) 
            | ( var | atom> (lambda x: ''.join(x))))

    element = ((left_br & disj & right_br) | atom > (lambda x: ''.join(x)))
    conj = (((element & conj_sep & conj) > (lambda x: 'conjunction\n' + add_tab(x[0]) + '\n' + add_tab(x[2])))
            | ((element) > (lambda x: ''.join(x))))
    disj = (((conj & disj_sep & disj) > (lambda x: 'disjunction\n' + add_tab(x[0]) + '\n' + add_tab(x[2]))) 
            | ((conj) > (lambda x: ''.join(x))))

    relation = (((atom & dot) > (lambda x: 'relation\n' + add_tab('head\n' + add_tab(x[0])))) | (
            (atom & cork & disj & dot) > (
        lambda x: 'relation\n' + add_tab('head\n' + add_tab(x[0]) + '\nbody\n' + add_tab(x[2])))))

    module = opt(keyword_module & ident & dot) > (lambda x: 'module\n' + add_tab(''.join(x[0])) if len(x) > 0 else '')

    bracket_type_body = ((left_br & type_seq & right_br) > (lambda x: ''.join(x[1])))
    type_seq =  (((bracket_type_body | atom | var) & arrow & ((rep1sep(bracket_type_body | atom | var , arrow) > (lambda x: '\n'.join(x)))) > (lambda x: 'typeseq\n' + add_tab(x[0] + '\n' + x[2]))) 
            | ((atom | var | bracket_type_body>(lambda x: ''.join(x)))))
    typedef = (keyword_type & ident & type_seq & dot) > (lambda x: 'typedef\n' + add_tab('typename\n' + add_tab(x[1]) + '\n' + x[2]))

    program = ((module) & (rep(typedef) > print_newline) & (rep(relation) > print_newline)) > print_newline



def getResult(arg, str):
    if arg == '--atom':
        return PrologParser.atom.parse(str)
    if arg == '--typeexpr':
        return PrologParser.type_seq.parse(str)
    if arg == '--type':
        return PrologParser.typedef.parse(str)
    if arg == '--module':
        return PrologParser.module.parse(str)
    if arg == '--relation':
        return PrologParser.relation.parse(str)
    if arg == '--prog':
        return PrologParser.program.parse(str)


if __name__ == '__main__':
    strings = [
        '.'
    ]
    if len(sys.argv) == 3:
        sys.stdout = open(sys.argv[2] + '.out', 'w')
        with open(sys.argv[2], 'r') as inputfile:
            result = getResult(sys.argv[1], inputfile.read())
            if type(result) == Success:
                print(result.value)
            else:
                sys.stdout = sys.__stdout__
                print(result.message)

    else:
        sys.stdout = open(sys.argv[1] + '.out', 'w')
        with open(sys.argv[1], 'r') as inputfile:
            result = PrologParser.program.parse(inputfile.read())
            if type(result) == Success:
                print(result.value)
            else:
                sys.stdout = sys.__stdout__
                print(result.message)
