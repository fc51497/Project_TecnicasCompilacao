import sys
import os
from lark import Lark, Transformer, v_args

with open("grammars/sPLash.lark") as _grammar:
    grammar = _grammar.read()


comments = []

_parser = Lark(grammar, parser='lalr', start='start',
               lexer_callbacks={"COMMENT": comments.append})
parse = _parser.parse


def main():
    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        print(parse(s))



def test(to_parse: str):

    prsd = parse(to_parse)

    print(prsd)
    print(prsd.pretty())
    print(comments)
    # print(parse("1+a*-3"))

def run_tests(args):

    
    if len(args) == 1:
        tests = ["P_example1.splash"]
    else: 
        tests1 = [ x for x in os.listdir("./tests/positive/") if x.split(".")[0] in args[1:] ] #Testes Positivos
        tests2 = [ x for x in os.listdir("./tests/negative/") if x.split(".")[0] in args[1:] ] #Testes Negativos

    for t in tests1:

        print("\n A testar os positivos: ", t)
        with open("./tests/positive"+t) as f:
            test(f.read())
            
    for t in tests2:

        print("\n A testar os negativos: ", t)
        with open("./tests/negative"+t) as f:
            test(f.read())
        

if __name__ == '__main__':
    run_tests(sys.argv)
    # test()
    # main()