from dataclasses import dataclass
from lark.tree import Meta
from splashAST import *
from splashAST import _Ty, _Node

RETURN="#return"

class TypeError(Exception):

    def __init__(self, message: str, meta:Meta = None):

        print("META:", meta)

        if not meta :
            super().__init__(message)
        else:
            super().__init__(f"Erro encontrado em {meta.line},{meta.column}: ", message)

@dataclass
class Contexto():

    stack = [{}]
    
    def get_type(self, name:str):

        for scope in self.stack.__reversed__():
            if name in scope:
                return scope[name]
        raise TypeError(f"Identificador {name} não está contextualizado")

    def set_type(self, name:str, value:str, retoque:Retoque=None):
        self.stack[-1][name] = {"type": value, "ref":retoque}
        
    def has_var(self, name:str):
        for scope in self.stack.__reversed__():
            if name in scope:
                return True
        return False
    
    def is_var_in_current_scope(self, name:str):
        return name in self.stack[-1]

    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        self.stack.pop()

def is_subtype(ctx:Contexto, this, that ):
    print(f"{this.__class__.__name__} subclasse de {that.__class__.__name__}?:",
          issubclass(this.__class__, that.__class__))
    return issubclass(this.__class__, that.__class__) and liquid_type_check(ctx, this, that)

def liquid_type_check(ctx: Contexto, this, that) -> bool:
    print("Não foi feita esta parte")
    return True

def infer_type(ctx:Contexto, expr:Expressao) -> _Ty:
    if isinstance(expr, IndexAccess):
        if ctx.has_var(expr.name):
            return ctx.get_type(expr.name).innerType
        
    elif isinstance(expr, Literal):
        return expr.type_

    elif isinstance(expr, Var):
        return ctx.get_type(expr.name)

    elif isinstance(expr, FuncCall):
        func_sign: FuncDef = ctx.get_type(expr.called)
        return func_sign.type_
    
    return ctx.get_type(expr)

def verify(ctx:Contexto, node):

    if isinstance(node, Programa):
        for st in node.argumentos:
            verify(ctx, st)
    
    elif isinstance(node, FuncDef):
        ctx.set_type(node.name, value=node)
        ctx.enter_scope()
        ctx.set_type(RETURN, node.type_)
        for param in node.params.args:
            ctx.set_type(param.name, param.type_)
        ctx.enter_scope()
        for st in node.block.argumentos:
            verify(ctx, st)
        ctx.exit_scope()
        ctx.exit_scope()

    elif isinstance(node, IfThenElse):
        if verify(ctx, node.test) != Bool:
            raise TypeError(f"A condição: {node.test}, deve avaliar para um valor booleano")
        ctx.enter_scope()
        for st in node.then_do.argumentos:
            verify(ctx, st)
        ctx.exit_scope()
        if node.else_do != None:
            ctx.enter_scope()
            for st in node.else_do.argumentos:
                verify(ctx, st)
            ctx.exit_scope()
    
    elif isinstance(node, Comparacao):
        print(verify(ctx, node.l_expr), verify(ctx, node.r_expr))
        if infer_type(ctx, node.l_expr) != infer_type(ctx, node.r_expr):
            raise TypeError(f"Operador ({node.l_expr}) e ({node.r_expr}) não são comparáveis")
        return Bool

    elif isinstance(node, Var):
        if not ctx.has_var(node.name):
            raise TypeError(f"Variável {node.name} não está definida")
        return ctx.get_type(node.name)
    
    elif isinstance(node, VarDef):
        if ctx.is_var_in_current_scope(node.name):
            raise TypeError(f"Variável {node.name} já está definida")
        ctx.set_type(node.name, node.type_)
    
    elif isinstance(node, Neg):
        tmp = infer_type(ctx, node.expr)
        if not is_subtype(ctx, tmp , Numeric()):
            raise TypeError(f"Não é possível usar notação negativa em valores não numéricos. Tipo: {tmp}")
        return tmp
    
    elif isinstance(node, Return):
        expected = ctx.get_type(RETURN)
        if node.value != None:
            actual = verify(ctx, node.value)
        else:
            actual = Void()
        if not is_subtype(ctx, actual, expected):
            raise TypeError(f"Retorno inválido. Tipo esperado: {expected.__class__.__name__} em vez de {actual.__class__.__name__}", meta=node.meta)
        
    elif isinstance(node, VarDec):
        if ctx.is_var_in_current_scope(node.name):
            raise TypeError(f"Variável já está definida")
        ctx.set_type(node.name, node.type_)
        
    elif isinstance(node, SetVal):
        name = None
        expected = None
        expected = infer_type(ctx, node.varToSet)
        if ctx.has_var( name ):
            actual = infer_type(ctx, node.value)
            if not is_subtype(ctx, actual, expected):
                raise TypeError(f"Tipo não correspondido: Esperado {expected} , recebido {actual}")
               
    elif isinstance(node, FuncCall):
        if ctx.has_var(node.called):
            fd:FuncDef = ctx.get_type(node.called)
            if len(fd.params.args) != len(node.args) :
                raise TypeError(f"Número inesperado de argumentos na função {node.called}", meta=node.meta)
            for act, exp in zip(node.args, fd.params.args):
                if not is_subtype(ctx, infer_type(ctx,act),  exp.type_):
                    raise TypeError(f"Tipo não correspondido: Esperado {exp} , recebido {act}", meta=node.meta)
    
    elif isinstance(node, While):
        if verify(ctx, node.condition) != Bool:
            raise TypeError(f"Condição While deve ser do tipo {Bool}")
        ctx.enter_scope()
        for stmt in node.block.argumentos:
            verify(ctx, stmt)
        ctx.exit_scope()
    
    elif isinstance(node, Literal):
        return infer_type(ctx, node)
    
    else:
        print(f"Impossível de correr, programa não tem as funcionalidades necessárias para continuar/analisar {node.__class__.__name__}:{node}")
