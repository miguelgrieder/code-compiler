from typing import Any, Dict, List
import sys
from ply import lex  # type: ignore
from pydantic import BaseModel


class Tokens(BaseModel):
    t_WHITESPACE: str = r"\s+"
    t_LEFT_PAREN: str = r"\("
    t_RIGHT_PAREN: str = r"\)"
    t_LEFT_BRACE: str = r"\{"
    t_RIGHT_BRACE: str = r"\}"
    t_SEMICOLON: str = r";"
    t_IGNORE: str = r"\t "
    t_LEFT_BRACKET: str = r"\["
    t_RIGHT_BRACKET: str = r"\]"
    t_INT_CONSTANT: str = r"[0-9]+"
    t_COMMA: str = r","
    t_ASSIGN: str = r"="
    t_GREATER: str = r">"
    t_LESS: str = r"<"
    t_GREATER_EQUAL: str = r">="
    t_LESS_EQUAL: str = r"<="
    t_EQUAL: str = r"=="
    t_NOT_EQUAL: str = r"!="
    t_PLUS: str = r"\+"
    t_MINUS: str = r"-"
    t_MULTIPLY: str = r"\*"
    t_DIVIDE: str = r"/"
    t_MODULO: str = r"%"
    t_FLOAT_CONSTANT: str = r"[0-9]*\.[0-9]+"
    t_STRING_CONSTANT: str = r'"[^"]*"'


class SymbolTableEntry(BaseModel):
    Lines: List[int]


class Lexical:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code

        self._symbol_table: Dict[str, SymbolTableEntry] = {}
        self.tokens_model = Tokens()

        self.reserved_words: List[str] = [
            "NEW",
            "INT",
            "FLOAT",
            "STRING",
            "NULL",
            "IF",
            "ELSE",
            "FOR",
            "BREAK",
            "DEF",
            "RETURN",
            "READ",
            "PRINT",
        ]

        self.tokens = (
            [attr_name[2:] for attr_name in self.tokens_model.dict() if attr_name.startswith("t_")]
            + self.reserved_words
            + ["IDENT"]
        )

        self.load_tokens()
        self.line_number = 1

    def load_tokens(self) -> None:
        for attr_name, attr_value in self.tokens_model.__dict__.items():
            if attr_name.startswith("t_"):
                setattr(self, attr_name, attr_value)

    def get_tokens_model(self) -> Tokens:
        return self.tokens_model

    def run(self, **kwargs: Dict[str, Any]) -> None:
        ply_lexer = lex.lex(module=self, **kwargs)
        ply_lexer.input(self.source_code)

        token_list: List[str] = []
        found_token = ply_lexer.token()
        while found_token:
            token_list.append(found_token.type)
            found_token = ply_lexer.token()

        symbol_table_output = ""
        purple = "\033[0;35m"
        green = "\033[0;32m"
        reset = "\033[0m"
        for name, value in self._symbol_table.items():
            symbol_table_output += f"{green}{name}{reset} -> {value}\n"

        print(  # noqa: T201
            f"-------------------\n"
            f"{purple}Token list:{reset}\n"
            f"-------------------\n"
            f"{green}{token_list}{reset}\n"
            f"-------------------\n"
            f"{purple}Symbol table:{reset}\n"
            f"-------------------\n"
            f"{symbol_table_output}{reset}"
        )

    def t_IDENT(self, t: lex.LexToken) -> Any:
        r"[A-Za-z]+[A-Za-z0-9]*."
        if t.value in self.reserved_words:
            t.type = t.value
        else:
            t.type = "IDENT"

        if t.value not in self._symbol_table:
            entry = SymbolTableEntry(Lines=[self.line_number])
            self._symbol_table[t.value] = entry
        else:
            self._symbol_table[t.value].Lines.append(self.line_number)

        return t

    def t_FLOAT_CONSTANT(self, t: lex.LexToken) -> Any:
        r"[0-9]*\.[0-9]+."
        t.value = float(t.value)
        return t

    def t_INT_CONSTANT(self, t: lex.LexToken) -> Any:
        r"[0-9]+."
        t.value = int(t.value)
        return t

    def t_STRING_CONSTANT(self, t: lex.LexToken) -> Any:
        r'"[^"]*".'
        t.type = "STRING_CONSTANT"
        t.value = t.value[1:-1]
        return t

    def t_BREAK(self, t: lex.LexToken) -> Any:
        r"\n+."
        self.line_number += 1
        return t

    def t_error(self, t: lex.LexToken) -> None:
        print(  # noqa: T201
            f"Lexical Error: Unexpected character '{t.value[0]}' at line {self.line_number}"
        )
        sys.exit(1)
