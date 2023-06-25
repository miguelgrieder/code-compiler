import sys

from code_compiler import parser, utils

if len(sys.argv) < 2 or not sys.argv[1].startswith('FILE='):
    print("Error: No file path provided! Pass it as FILE= as an argumet", flush=True)  # noqa: T201
    sys.exit(1)
else:
    provided_argv = sys.argv[1][5:]
    source_code = utils.read_file_content(file_path=provided_argv)
    parser.Parser(source_code)
