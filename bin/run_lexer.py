import sys
import os

from code_compiler import lexer, utils

if (len(sys.argv) < 2 or not sys.argv[1].startswith('FILE=')) and 'FILE' not in os.environ:
    print("Error: No file path provided! Pass it as FILE= as an argumet or in .env", flush=True)  # noqa: T201
    sys.exit(1)
else:
    provided_argv = os.environ['FILE']
    source_code = utils.read_file_content(file_path=provided_argv)
    lexer.Lexer(source_code)
