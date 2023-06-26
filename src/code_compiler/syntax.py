from typing import Any, List, Tuple

from ply import lex, yacc
from pydantic import BaseModel

from code_compiler.lexical import Lexical


class PrecedenceModel(BaseModel):
    left: List[Tuple[str, ...]]


class Syntax:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code
        specific_lexer = Lexical(self.source_code)
        self.lexical = lex.lex(module=specific_lexer)
        self.tokens = specific_lexer.tokens
        self.precedence = (
            ("left", "LESS", "LESS_EQUAL", "GREATER", "GREATER_EQUAL"),
            ("left", "PLUS", "MINUS"),
            ("left", "MULTIPLY", "DIVIDE"),
            ("left", "LEFT_PAREN", "RIGHT_PAREN"),
        )

    def build(self, **kwargs: Any) -> yacc.LRParser:
        return yacc.yacc(module=self, **kwargs)

    def execute(self) -> None:
        syntax = self.build()
        syntax.parse(self.source_code)

    def p_error(self, p: yacc.YaccProduction) -> None:
        raise SyntaxError(f"Syntax error in input! {p}")  # noqa: TRY003

    def p_PROGRAM(self, p: yacc.YaccProduction) -> None:
        """PROGRAM : STATEMENT
        | FUNCLIST
        | EMPTY
        """
        pass

    def p_FUNCLIST(self, p: yacc.YaccProduction) -> None:
        """FUNCLIST : FUNCDEF FUNCLIST_2"""
        pass

    def p_FUNCLIST_2(self, p: yacc.YaccProduction) -> None:
        """FUNCLIST_2 : FUNCLIST
        | EMPTY
        """
        pass

    def p_FUNCDEF(self, p: yacc.YaccProduction) -> None:
        """FUNCDEF : DEF IDENT LEFT_PAREN PARAMLIST RIGHT_PAREN LEFT_BRACE STATELIST RIGHT_BRACE"""  # noqa
        pass

    def p_PARAMLIST(self, p: yacc.YaccProduction) -> None:
        """PARAMLIST : PARAMLIST_2
        | EMPTY
        """
        pass

    def p_PARAMLIST_2(self, p: yacc.YaccProduction) -> None:
        """PARAMLIST_2 : INT_OR_FLOAT_OR_STRING IDENT PARAMLIST_3"""
        pass

    def p_INT_OR_FLOAT_OR_STRING(self, p: yacc.YaccProduction) -> None:
        """INT_OR_FLOAT_OR_STRING : INT
        | FLOAT
        | STRING
        """
        pass

    def p_PARAMLIST_3(self, p):
        """PARAMLIST_3 : COMMA PARAMLIST
        | EMPTY
        """
        pass

    def p_STATEMENT(self, p: yacc.YaccProduction) -> None:
        """STATEMENT : VARDECL SEMICOLON
        | ATRIBSTAT SEMICOLON
        | PRINTSTAT SEMICOLON
        | READSTAT SEMICOLON
        | RETURNSTAT SEMICOLON
        | IFSTAT
        | FORSTAT
        | LEFT_BRACE STATELIST RIGHT_BRACE
        | BREAK SEMICOLON
        | SEMICOLON
        """
        pass

    def p_VARDECL(self, p: yacc.YaccProduction) -> None:
        """VARDECL : INT_OR_FLOAT_OR_STRING IDENT VARDECL_2"""
        pass

    def p_VARDECL_2(self, p: yacc.YaccProduction) -> None:
        """VARDECL_2 : LEFT_BRACKET INT_CONSTANT RIGHT_BRACKET VARDECL_2
        | EMPTY
        """
        pass

    def p_ATRIBSTAT(self, p: yacc.YaccProduction) -> None:
        """ATRIBSTAT : LVALUE ASSIGN ATRIBSTAT_2"""
        pass

    def p_ATRIBSTAT_2(self, p: yacc.YaccProduction) -> None:
        """ATRIBSTAT_2 : FUNCCALL_EXPRESSION
        | ALLOCEXPRESSION
        """
        pass

    def p_FUNCCALL_EXPRESSION(self, p: yacc.YaccProduction) -> None:
        """FUNCCALL_EXPRESSION : PLUS FACTOR TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | MINUS FACTOR TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | INT_CONSTANT TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | FLOAT_CONSTANT TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | STRING_CONSTANT TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | NULL TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | LEFT_PAREN NUMEXPRESSION RIGHT_PAREN TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | FUNCCALL"""  # noqa
        pass

    def p_FUNCCALL(self, p):
        """FUNCCALL : IDENT FUNCCALL_2"""
        pass

    def p_FUNCCALL_2(self, p):
        """FUNCCALL_2 : ALLOCEXPRESSION_2 TERM_2 NUMEXPRESSION_2 EXPRESSION_2
        | LEFT_PAREN PARAMLISTCALL RIGHT_PAREN
        """

    def p_PARAMLISTCALL(self, p: yacc.YaccProduction) -> None:
        """PARAMLISTCALL : IDENT PARAMLISTCALL_2
        | EMPTY
        """
        pass

    def p_PARAMLISTCALL_2(self, p: yacc.YaccProduction) -> None:
        """PARAMLISTCALL_2 : COMMA PARAMLISTCALL
        | EMPTY
        """
        pass

    def p_PRINTSTAT(self, p: yacc.YaccProduction) -> None:
        """PRINTSTAT : PRINT EXPRESSION"""
        pass

    def p_READSTAT(self, p: yacc.YaccProduction) -> None:
        """READSTAT : READ LVALUE"""
        pass

    def p_RETURNSTAT(self, p: yacc.YaccProduction) -> None:
        """RETURNSTAT : RETURN"""
        pass

    def p_IFSTAT(self, p: yacc.YaccProduction) -> None:
        """IFSTAT : IF LEFT_PAREN EXPRESSION RIGHT_PAREN STATEMENT IFSTAT_2"""
        pass

    def p_IFSTAT_2(self, p: yacc.YaccProduction) -> None:
        """IFSTAT_2 : ELSE STATEMENT
        | EMPTY
        """
        pass

    def p_FORSTAT(self, p: yacc.YaccProduction) -> None:
        """FORSTAT : FOR LEFT_PAREN ATRIBSTAT SEMICOLON EXPRESSION SEMICOLON ATRIBSTAT RIGHT_PAREN STATEMENT"""  # noqa
        pass

    def p_STATELIST(self, p: yacc.YaccProduction) -> None:
        """STATELIST : STATEMENT STATELIST_2"""
        pass

    def p_STATELIST_2(self, p: yacc.YaccProduction) -> None:
        """STATELIST_2 : STATELIST
        | EMPTY
        """
        pass

    def p_ALLOCEXPRESSION(self, p: yacc.YaccProduction) -> None:
        """ALLOCEXPRESSION :  NEW INT_OR_FLOAT_OR_STRING LEFT_BRACKET NUMEXPRESSION RIGHT_BRACKET ALLOCEXPRESSION_2"""  # noqa
        pass

    def p_ALLOCEXPRESSION_2(self, p: yacc.YaccProduction) -> None:
        """ALLOCEXPRESSION_2 : LEFT_BRACKET NUMEXPRESSION RIGHT_BRACKET ALLOCEXPRESSION_2
        | EMPTY"""  # noqa
        pass

    def p_EXPRESSION(self, p: yacc.YaccProduction) -> None:
        """EXPRESSION : NUMEXPRESSION EXPRESSION_2"""
        pass

    def p_EXPRESSION_2(self, p: yacc.YaccProduction) -> None:
        """EXPRESSION_2 : COMPAREOPERANDS NUMEXPRESSION
        | EMPTY
        """
        pass

    def p_COMPAREOPERANDS(self, p: yacc.YaccProduction) -> None:
        """COMPAREOPERANDS : LESS
        | GREATER
        | LESS_EQUAL
        | GREATER_EQUAL
        | EQUAL
        | NOT_EQUAL
        """
        pass

    def p_NUMEXPRESSION(self, p: yacc.YaccProduction) -> None:
        """NUMEXPRESSION : TERM NUMEXPRESSION_2"""
        pass

    def p_NUMEXPRESSION_2(self, p: yacc.YaccProduction) -> None:
        """NUMEXPRESSION_2 : NUMEXPRESSION_3 TERM NUMEXPRESSION_2
        | EMPTY
        """
        pass

    def p_NUMEXPRESSION_3(self, p: yacc.YaccProduction) -> None:
        """NUMEXPRESSION_3 : PLUS
        | MINUS
        """
        pass

    def p_TERM(self, p: yacc.YaccProduction) -> None:
        """TERM : UNARYEXPRESSION TERM_2"""
        pass

    def p_TERM_2(self, p: yacc.YaccProduction) -> None:
        """TERM_2 : MULT_OR_DIV_OR_MOD TERM
        | EMPTY
        """
        pass

    def p_MULT_OR_DIV_OR_MOD(self, p: yacc.YaccProduction) -> None:
        """MULT_OR_DIV_OR_MOD : MULTIPLY
        | DIVIDE
        | MODULO
        """
        pass

    def p_UNARYEXPRESSION(self, p: yacc.YaccProduction) -> None:
        """UNARYEXPRESSION : NUMEXPRESSION_3 FACTOR
        | FACTOR
        """
        pass

    def p_FACTOR(self, p: yacc.YaccProduction) -> None:
        """FACTOR : INT_CONSTANT
        | FLOAT_CONSTANT
        | STRING_CONSTANT
        | NULL
        | LVALUE
        | LEFT_PAREN NUMEXPRESSION RIGHT_PAREN
        """
        pass

    def p_LVALUE(self, p: yacc.YaccProduction) -> None:
        """LVALUE : IDENT ALLOCEXPRESSION_2"""
        pass

    def p_EMPTY(self, p: yacc.YaccProduction) -> None:
        """EMPTY :"""
        pass
