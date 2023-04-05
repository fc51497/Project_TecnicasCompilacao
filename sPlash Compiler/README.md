Faculdade de Ciências da Universidade de Lisboa
Unidade Curricular: Técnicas de Compilação (2022/2023)
Docente: Alcides Fonseca
Bernardo Godinho, fc51497


## Phase 1 - Parser

The goal is to implement a parser that takes sPLash programs and prints the AST of the program. This will be the first step torwards a full compiler.

As part of this task, you must also build a set of diverse programs written in `sPLash` both grammatically correct and incorrect to validate your parser.

----
### Language Description

- Comments in simPLe (meant sPLash) start with `(*` and end with `*)`.
- sPLash is white space insensitive.
- A program is made of several declarations or definitions that precede the main body.
- A declaration includes the name of the function, it's arguments, types and refinments, as well as the return type.

```sPLash
sample_normalDouble (meanDouble, stddevDouble where stddev != 0);
```
- The refinement (where p(a)) is optional. The refinement can refer to the variable, and constrains possible values allowed as parameters.
- The return type can also be refined

```sPLash
  absInt where abs  0 (valInt);  
```

- A definition is similar, but includes a block of code that defines the funcion, or a declaration of the value.

```sPLash
maxInt (a Int, bInt){
    if a  b {
        return a;
    }
    return b;
}

piInt = 3; ( Engineers, am i right )
```

- Statements, declarations and definitions with values end with semicolon. Definitions of functions do not need semicolon, as the curly braces delimit the function.
    - Blocks are enclosed with { and } and are comprised of 0 or more statements.
    - Expressions are statements 1; or f(3);
    - If statements have a condition, a then block and optionally an else block, separated by the else keyword.
    - While statements are similar to if statements, without the else block.
    - Local variables statements are defined similarly to global ones (with a mandatory starting value)
    - Variable assignments can be statements.

- Expressions represent values. They can be
    - Binary operators, with a C-like precedence and parenthesis to force other precedences `&&`, ``, `==`, `!=`, `=`, ``, `=`, ``, `+`, `-`, ``, ``, `%` em que a divisão tem sempre a semântica da divisão de floats.
    - The not unary operator (!true)
    - Boolean literals (`true`, `false`)
    - Integer literals (`1`, `01`, `12312341341`, `1_000_000`) where underscores can be present in any position.
    - Float literals (`1.1`, `.5`, `1233123131231321`)
    - String literals (``, `a`, `aa`, `qwertyuiop`, `qwertytuiop`)
    - Variables, which start with a letter or understore and are followed by any number of letters, underscores or numbers.
    - index access, (`a[0]` or `get_array()[i+1]`)