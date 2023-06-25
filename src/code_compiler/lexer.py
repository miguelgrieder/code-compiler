from typing import Dict, List

from pydantic import BaseModel


class SymbolTableEntry(BaseModel):
    Lines: List[int]


class ReservedWords(BaseModel):
    words: List[str]


class Tokens(BaseModel):
    reserved_words: List[str]

    DEF: str = r"def"
    IDENT: str = r"[A-Za-z]+[A-Za-z0-9]*"
    LEFT_PAREN: str = r"\("
    RIGHT_PAREN: str = r"\)"
    LEFT_BRACE: str = r"\{"
    RIGHT_BRACE: str = r"\}"
    FLOAT: str = r"\d+\.\d+"
    INT: str = r"\d+"
    STRING: str = r'"([\w\d]|[^"])*"'
    SEMICOLON: str = r";"
    IGNORE: str = r"\t "


class Lexer:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code

        self._symbol_table: Dict[str, SymbolTableEntry] = {}
        self.reserved_words = ReservedWords(
            words=[
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
        )
        self.tokens = Tokens(reserved_words=self.reserved_words.words)

    def get_tokens(self) -> Tokens:
        return self.tokens
