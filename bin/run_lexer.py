import sys
import os

from code_compiler import lexer, utils

if len(sys.argv) > 1 and sys.argv[1].startswith('FILE='):
    provided_argv = sys.argv[1][5:]
elif 'FILE' in os.environ:
    provided_argv = os.environ['FILE']
else:
    print("Error: No file path provided! Pass it as FILE= argument or in the environment.", flush=True)
    sys.exit(1)

source_code = utils.read_file_content(file_path=provided_argv)
lexer.Lexer(source_code)
