import os
import sys

current_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_path)
src_dir = os.path.join(parent_dir, "src")
sys.path.append(src_dir)

from code_compiler import lexer, utils  # noqa: E402

if len(sys.argv) < 2:
    print("Error: No file path provided!", flush=True)  # noqa: T201
    sys.exit(1)
else:
    provided_argv = sys.argv[1]
    source_code = utils.read_file_content(file_path=provided_argv)
    lexer.Lexer(source_code)
