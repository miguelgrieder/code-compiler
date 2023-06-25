import sys

from code_compiler import lexer, utils

if len(sys.argv) < 2:
    print("Error: No file path provided!", flush=True)  # noqa: T201
    sys.exit(1)
else:
    provided_argv = sys.argv[1]
    source_code = utils.read_file_content(file_path=provided_argv)
    lexer.Lexer(source_code)
