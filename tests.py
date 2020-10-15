from parsita import Success, Failure

from parsec import PrologParser


def test_ident():
    parse = PrologParser.ident.parse
    assert type(parse('qwerty')) == Success
    assert type(parse('aSD9JIDJEIDIJJ')) == Success
    assert type(parse('f')) == Success

    assert type(parse('module')) == Failure
    assert type(parse('type')) == Failure
    assert type(parse('Qwerty')) == Failure
    assert type(parse('qwerty.')) == Failure
    assert type(parse('.')) == Failure


def test_variable():
    parse = PrologParser.var.parse
    assert type(parse('Qwerty')) == Success
    assert type(parse('QSD9JIDJEIDIJJ')) == Success
    assert type(parse('F')) == Success

    assert type(parse('module')) == Failure
    assert type(parse('type')) == Failure
    assert type(parse('qwerty')) == Failure
    assert type(parse('Qwerty.')) == Failure
    assert type(parse('.')) == Failure


def test_atom():
    parse = PrologParser.atom.parse
    assert type(parse('a')) == Success
    assert type(parse('a b c d')) == Success
    assert type(parse('a b C')) == Success
    assert type(parse('a B c D E f')) == Success
    assert type(parse('a (b C)')) == Success
    assert type(parse('a (((c))) b')) == Success
    assert type(parse('a (b C) d E f')) == Success
    assert type(parse('a (b C) (((d ((E))))) f')) == Success
    assert type(parse('a (b (c))')) == Success
    assert type(parse('a ((A)) b')) == Success

    assert type(parse('type b')) == Failure
    assert type(parse('a (b c d')) == Failure
    assert type(parse('a module')) == Failure
    assert type(parse('A')) == Failure
    assert type(parse('A b')) == Failure
    assert type(parse('A B c d')) == Failure
    assert type(parse('a ((b) c)')) == Failure
    assert type(parse('a (((b c))')) == Failure
    assert type(parse('a (((b (((c)) d e f))))')) == Failure
    assert type(parse('a b ()')) == Failure
    assert type(parse('a (B c)')) == Failure
    assert type(parse('(a)')) == Failure
    assert type(parse('(a) b c')) == Failure


def test_module():
    parse = PrologParser.module.parse
    assert type(parse('module qwerty.')) == Success
    assert type(parse('module aSD9JIDJEIDIJJ.')) == Success
    assert type(parse('module f.')) == Success

    assert type(parse('modUle qwerty.')) == Failure
    assert type(parse('module qwerty')) == Failure
    assert type(parse('module Qwerty.')) == Failure
    assert type(parse('module type.')) == Failure
    assert type(parse('module module.')) == Failure
    assert type(parse('module a b.')) == Failure
    assert type(parse('module.')) == Failure
    assert type(parse('.')) == Failure


def test_type():
    parse = PrologParser.typedef.parse
    assert type(parse('type fruit string -> string -> string -> o.')) == Success
    assert type(parse('type filter (A -> o) -> o.')) == Success
    assert type(parse('type filter t.')) == Success
    assert type(parse('type filter (A -> o) -> list A -> list A -> o.')) == Success
    assert type(parse('type filter string -> list A.')) == Success
    assert type(parse('type filter (A -> (B -> C -> (A -> list A) -> C)) -> o.')) == Success
    assert type(parse('type filter ((A -> (B -> C -> (A -> list A) -> C))) -> o.')) == Success
    assert type(parse('type filter (A -> (B -> C -> (A -> (list A)) -> C)) -> o.')) == Success

    assert type(parse('type.')) == Failure
    assert type(parse('.')) == Failure
    assert type(parse('type kavo.')) == Failure
    assert type(parse('type -> x.')) == Failure
    assert type(parse('type foo ->.')) == Failure
    assert type(parse('type type type -> type.')) == Failure
    assert type(parse('type x -> y -> z.')) == Failure
    assert type(parse('tupe x o.')) == Failure
    assert type(parse('type filter A -> B -> o')) == Failure


def test_rel():
    parse = PrologParser.relation.parse
    assert type(parse('f.')) == Success
    assert type(parse('f :- g.')) == Success
    assert type(parse('f :- (((a))).')) == Success
    assert type(parse('f :- g, h; t.')) == Success
    assert type(parse('f :- g, (h; t).')) == Success
    assert type(parse('f a :- g, h (t c d).')) == Success
    assert type(parse('f (cons h t) :- g h, f t.')) == Success
    assert type(parse('f :- (a ; (b)) , (((c ; d))).')) == Success

    assert type(parse('(f).')) == Failure
    assert type(parse('f')) == Failure
    assert type(parse(':- f.')) == Failure
    assert type(parse('f :- .')) == Failure
    assert type(parse('f :- g; h, .')) == Failure
    assert type(parse('f :- (g; (f).')) == Failure
    assert type(parse('f ().')) == Failure
    assert type(parse('f (a.')) == Failure
    assert type(parse('(a) b.')) == Failure


def test_prog():
    parse = PrologParser.program.parse
    assert type(parse('module test.')) == Success
    assert type(parse('module test. type t f -> o.')) == Success
    assert type(parse('module test. type t f -> o. type t f -> o.')) == Success
    assert type(parse('module test. type t f -> o. type t f -> o. f :- name.')) == Success
    assert type(parse('module test. type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse('type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse('type t f -> o. f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse('f :- name. a (b c) :- x, y, z.')) == Success
    assert type(parse('a (b c) :- x, y, z.')) == Success
    assert type(parse('f.')) == Success


    assert type(parse('module test. module test2. a (b c) :- x, y, z.')) == Failure
    assert type(parse('module test. type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z. type x y.')) == Failure
    assert type(parse('type t f -> o. type t f -> o. f :- name. a (b c) :- x, y, z. module test.')) == Failure
    assert type(parse('type t f -> o. type t f -> o f :- name. a (b c) :- x, y, z.')) == Failure
    assert type(parse('module test. type t f -> o.. type t f -> o. f :- name. a (b c) :- x, y, z.')) == Failure
    assert type(parse('module test. type t f -> o. type t f -> o f :- name. a (b c) :- x, y, z.')) == Failure
    assert type(parse('module test. type t f -> o. (type t f -> o.)')) == Failure
    assert type(parse('module test. (type t f -> o. type t f -> o.)')) == Failure


if __name__ == '__main__':
	test_module()
	test_ident()
	test_variable()
	test_atom()
	test_type()
	test_rel()
	test_prog()
	print('All tests passed')
	