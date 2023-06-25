from textwrap import dedent
from typing import Dict, List

from ply import lex  # type: ignore
from pydantic import BaseModel


class SymbolTableEntry(BaseModel):
    Lines: List[int]


class Tokens(BaseModel):
    t_DEF: str = r"def"
    t_IDENT: str = r"[A-Za-z]+[A-Za-z0-9]*"
    t_LEFT_PAREN: str = r"\("
    t_RIGHT_PAREN: str = r"\)"
    t_LEFT_BRACE: str = r"\{"
    t_RIGHT_BRACE: str = r"\}"
    t_FLOAT: str = r"\d+\.\d+"
    t_INT: str = r"\d+"
    t_STRING: str = r'"([\w\d]|[^"])*"'
    t_SEMICOLON: str = r";"
    t_IGNORE: str = r"\t "


class Lexer:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code

        self._symbol_table: Dict[str, SymbolTableEntry] = {}
        self.reserved_words = [
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

        self.tokens_model = Tokens(reserved_words=self.reserved_words)
        self.tokens = [
            attr_name[2:] for attr_name in self.tokens_model.dict() if attr_name.startswith("t_")
        ] + self.reserved_words

        for attr_name, attr_value in self.tokens_model.__dict__.items():
            if attr_name.startswith("t_"):
                setattr(self, attr_name, attr_value)
        print('setup ok')

    def get_tokens_model(self) -> Tokens:
        return self.tokens_model

    def execute(self, **kwargs) -> None:
        ply_lexer = lex.lex(module=self, **kwargs)
        ply_lexer.input(self.source_code)

        token_list: List[str] = []
        while True:
            found_token = ply_lexer.token()
            if not found_token:
                break
            token_list.append(found_token.type)

        print(  # noqa: T201
            dedent(
                f"""
            -------------------
            -> Token list:
            -------------------
            {token_list}
            -------------------
            Symbol table:
            -------------------
            {self._symbol_table}
            """
            )
        )
