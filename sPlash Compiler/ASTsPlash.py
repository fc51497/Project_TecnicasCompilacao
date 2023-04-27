import json
from dataclasses import dataclass
from typing import List, Any, Union

from lark  import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta

from dataclasses import dataclass
from typing import List

t_int = "Int"
t_double = "Double"
t_string = "String"
t_bool = "Bool"

@dataclass
class _Node(ast_utils.Ast):
    pass

@dataclass
class _Ty(_Node):
    pass

@dataclass
class Array(_Ty):
    innerType: _Ty

@dataclass
class BasicType(_Ty):
    pass

@dataclass
class Numeric(BasicType):
    pass

@dataclass
class Int(Numeric):
    pass

@dataclass
class Double(Numeric):
    pass

@dataclass
class Bool(BasicType):
    pass

@dataclass
class String(BasicType):
    pass

@dataclass
class Literal():
    type_ : _Ty
    val: any

@dataclass
class Argumentos(_Node):
    pass

@dataclass
class Programa(_Node, ast_utils.AsList):
    argumentos: List[Argumentos] = None

@dataclass
class Expressao(Argumentos):
    pass    

@dataclass
class Declaracao(_Node):
    pass

@dataclass
class Test(_Node):
    pass

@dataclass
class Variavel(_Node):
    pass

@dataclass
class Comparacao(_Node):
    E_expr : Expressao
    op: str
    D_expr : Expressao

@dataclass
class Retoque(_Node):
    cond: Test

@dataclass
class Block(_Node, ast_utils.AsList):
    argumentos: List[Argumentos] = None

@dataclass
class Declaration(Argumentos):
        type_ : BasicType
        name : str 
        retoques : List[Retoque] = None

@dataclass
class FuncArgs(_Node, ast_utils.AsList):
    args: List = None

@dataclass
class Arg(_Node, ast_utils.WithMeta):
    meta: Meta
    name: str
    type_: _Ty
    retoque: Retoque = None

@dataclass
class VarDef(Argumentos, ast_utils.WithMeta):
    meta:Meta
    name:str
    type_:_Ty
    value:str

@dataclass
class VarDec(Argumentos):
    name:str
    type_:_Ty

@dataclass
class SetVal(Argumentos):
    varToSet: Union[str, IndexAccess]
    value: Expressao

@dataclass
class FuncCall(Expressao, ast_utils.WithMeta):
    meta: Meta
    called: str
    args: List[Expressao]

    def __init__(self, *params):
        self.meta = params[0]
        self.called = params[1]
        self.args = list(params[2:])

@dataclass
class FuncDef(Argumentos):

    name: str = ""
    type_: str  = "Void"
    retoque: Retoque = None
    params: FuncArgs = None
    block: Block = None    

@dataclass
class Not(Argumentos):
    expr: Expressao

@dataclass
class A(Argumentos):
    expr: Expressao

@dataclass
class Add(Argumentos):
    E_expr: Expressao
    D_expr: Expressao

@dataclass
class IfThenElse(Argumentos):
    test: Test
    then_do: Block
    else_do: Block = None

@dataclass
class While(Argumentos):
    condicao: Test
    block: Block

@dataclass
class Return(Argumentos, ast_utils.WithMeta):
    meta:Meta
    value: Expressao

@dataclass
class Var(_Node):
    name:str

class to_AST(Transformer):
    type_dict = {
        "int" : Int,
        "double": Double,
        "float": Double,
        "bool": Bool,
        "string": String,
    }
    
    def NAME(self, n):
        return n.value

    def BOOL(self, b):
        return Literal(type_=Bool(), val=bool(b.value.lower()))

    def STRING(self, s):
        return Literal(type_=String(), val=s[1:-1])
    
    def INT(self, i):
        return Literal(type_=Int(), val=int(i))
        
    def DOUBLE(self, d):
        return Literal(type_=Double(), val=float(d))

    def TYPE(self, t):
        if t.value.lower() in self.type_dict:
            return self.type_dict[t.value.lower()]()
        return BasicType(t.value)

    @v_args(inline=True)
    def start(self, x):
        return x
    
class jsonAST(json.JSONEncoder):
    def default(self, o: Any) -> Any: 
        return { o.__class__.__name__.lower() : { k:v for k, v in o.__dict__.items() if v != None }}
