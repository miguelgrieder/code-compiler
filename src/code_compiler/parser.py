from typing import List, Tuple

from ply import lex  # type: ignore
from pydantic import BaseModel

from code_compiler.lexer import Lexer


class PrecedenceModel(BaseModel):
    left: List[Tuple[str, ...]]


class Parser:
    def __init__(self, source_code: str) -> None:
        self.source_code = source_code
        specific_lexer = Lexer(self.source_code)

        self.application_lexer = lex.lex(specific_lexer)
        self.tokens = specific_lexer.get_tokens()
        self.precedence = PrecedenceModel(
            left=[
                ("LEFT_BRACE", "RIGHT_BRACE"),
            ]
        )
