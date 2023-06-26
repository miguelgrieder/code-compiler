from typing import Any, List, Tuple

from ply import lex, yacc  # type: ignore
from pydantic import BaseModel

from code_compiler.lexer import Lexer


class PrecedenceModel(BaseModel):
    left: List[Tuple[str, ...]]


class Parser:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code
        specific_lexer = Lexer(self.source_code)
        self.lexer = lex.lex(module=specific_lexer)

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
        parser = self.build()
        parser.parse(self.source_code)

    def p_error(self, p: yacc.YaccProduction) -> None:
        raise SyntaxError("Syntax error in input!")  # noqa: TRY003

    def p_PROGRAM(self, p: yacc.YaccProduction) -> None:
        """PROGRAM : STATEMENT
        | FUNCLIST
        | EMPTY.
        """
        pass

    def p_FUNCLIST(self, p: yacc.YaccProduction) -> None:
        """FUNCLIST : FUNCDEF FUNCLIST_2."""
        pass

    def p_FUNCLIST_2(self, p: yacc.YaccProduction) -> None:
        """FUNCLIST_2 : FUNCLIST
        | EMPTY.
        """
        pass

    def p_FUNCDEF(self, p: yacc.YaccProduction) -> None:
        """FUNCDEF : DEF IDENTIFIER LEFT_PAREN PARAMLIST RIGHT_PAREN LEFT_BRACE STATELIST RIGHT_BRACE."""  # noqa: E501
        pass

    def p_PARAMLIST(self, p: yacc.YaccProduction) -> None:
        """PARAMLIST : PARAMLIST_2
        | EMPTY.
        """
        pass

    def p_PARAMLIST_2(self, p: yacc.YaccProduction) -> None:
        """PARAMLIST_2 : INT_OR_FLOAT_OR_STRING IDENTIFIER PARAMLIST_3."""
        pass

    def p_INT_OR_FLOAT_OR_STRING(self, p: yacc.YaccProduction) -> None:
        """INT_OR_FLOAT_OR_STRING : INT
        | FLOAT
        | STRING.
        """
        pass

    def p_PARAMLIST_3(self, p: yacc.YaccProduction) -> None:
        """PARAMLIST_3 : COMMA PARAMLIST
        | EMPTY.
        """
        pass

    def p_STATEMENT(self, p: yacc.YaccProduction) -> None:
        """Statement : expression
        | assignment
        | if_statement
        | while_statement
        | print_statement
        | break_statement
        | empty.
        """
        pass

    def p_VARDECL(self, p: yacc.YaccProduction) -> None:
        """VARDECL : INT_OR_FLOAT_OR_STRING IDENTIFIER VARDECL_2."""
        pass

    def p_VARDECL_2(self, p: yacc.YaccProduction) -> None:
        """VARDECL_2 : LEFT_BRACKET INT_LITERAL RIGHT_BRACKET VARDECL_2
        | EMPTY.
        """
        pass

    def p_ATRIBSTAT(self, p: yacc.YaccProduction) -> None:
        """ATRIBSTAT : LVALUE ASSIGN ATRIBSTAT_2."""
        pass

    def p_ATRIBSTAT_2(self, p: yacc.YaccProduction) -> None:
        """ATRIBSTAT_2 : INT_LITERAL
        | FLOAT_LITERAL
        | STRING_LITERAL
        | LVALUE.
        """
        pass

    def p_PRINTSTAT(self, p: yacc.YaccProduction) -> None:
        """PRINTSTAT : PRINT LEFT_PAREN PRINTSTAT_2 RIGHT_PAREN."""
        pass

    def p_PRINTSTAT_2(self, p: yacc.YaccProduction) -> None:
        """PRINTSTAT_2 : STRING_LITERAL
        | INT_LITERAL
        | FLOAT_LITERAL
        | LVALUE.
        """
        pass

    def p_READSTAT(self, p: yacc.YaccProduction) -> None:
        """READSTAT : READ LEFT_PAREN LVALUE RIGHT_PAREN."""
        pass

    def p_RETURNSTAT(self, p: yacc.YaccProduction) -> None:
        """RETURNSTAT : RETURN RETURNSTAT_2."""
        pass

    def p_RETURNSTAT_2(self, p: yacc.YaccProduction) -> None:
        """RETURNSTAT_2 : LVALUE
        | INT_LITERAL
        | FLOAT_LITERAL
        | STRING_LITERAL.
        """
        pass

    def p_IFSTAT(self, p: yacc.YaccProduction) -> None:
        """IFSTAT : IF LEFT_PAREN LVALUE RIGHT_PAREN LEFT_BRACE STATELIST RIGHT_BRACE ELSE IFSTAT_2
        | IF LEFT_PAREN LVALUE RIGHT_PAREN LEFT_BRACE STATELIST RIGHT_BRACE.
        """
        pass

    def p_IFSTAT_2(self, p: yacc.YaccProduction) -> None:
        """IFSTAT_2 : IF LEFT_PAREN LVALUE RIGHT_PAREN LEFT_BRACE STATELIST RIGHT_BRACE
        | EMPTY.
        """
        pass

    def p_FORSTAT(self, p: yacc.YaccProduction) -> None:
        """FORSTAT : FOR LEFT_PAREN VARDECL SEMICOLON LVALUE FORSTAT_2 RIGHT_PAREN LEFT_BRACE STATELIST RIGHT_BRACE."""  # noqa: E501
        pass

    def p_FORSTAT_2(self, p: yacc.YaccProduction) -> None:
        """FORSTAT_2 : LVALUE
        | INT_LITERAL
        | FLOAT_LITERAL.
        """
        pass

    def p_STATELIST(self, p: yacc.YaccProduction) -> None:
        """STATELIST : STATEMENT STATELIST
        | EMPTY.
        """
        pass

    def p_EMPTY(self, p: yacc.YaccProduction) -> None:
        """EMPTY :"""
        pass

    def p_EXPRESSION(self, p: yacc.YaccProduction) -> None:
        """EXPRESSION : expression PLUS term
        | expression MINUS term
        | term.
        """
        pass

    def p_ASSIGNMENT(self, p: yacc.YaccProduction) -> None:
        """ASSIGNMENT : IDENTIFIER EQUALS expression."""
        pass

    def p_WHILE_STATEMENT(self, p: yacc.YaccProduction) -> None:
        """WHILE_STATEMENT : WHILE expression DO statement END."""
        pass

    def p_PRINT_STATEMENT(self, p: yacc.YaccProduction) -> None:
        """PRINT_STATEMENT : PRINT expression."""
        pass

    def p_BREAK_STATEMENT(self, p: yacc.YaccProduction) -> None:
        """BREAK_STATEMENT : BREAK."""
        pass

    def p_TERM(self, p: yacc.YaccProduction) -> None:
        """TERM : term TIMES factor
        | term DIVIDE factor
        | factor.
        """
        pass

    def p_FACTOR(self, p: yacc.YaccProduction) -> None:
        """FACTOR : LPAREN expression RPAREN
        | NUMBER
        | IDENTIFIER.
        """
        pass

    def p_IF_STATEMENT(self, p: yacc.YaccProduction) -> None:
        """IF_STATEMENT : IF expression THEN statement END
        | IF expression THEN statement ELSE statement END.
        """
        pass

    def p_LVALUE(self, p: yacc.YaccProduction) -> None:
        """LVALUE : IDENTIFIER LVALUE_2."""
        pass

    def p_LVALUE_2(self, p: yacc.YaccProduction) -> None:
        """LVALUE_2 : LEFT_BRACKET INT_LITERAL RIGHT_BRACKET LVALUE_2
        | EMPTY.
        """
        pass
