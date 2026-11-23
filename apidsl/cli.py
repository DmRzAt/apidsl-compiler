import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

from apidsl.codegen import slug
from apidsl.compiler import CompilationFailed, compile_source
from apidsl.errors import CompileError
from apidsl.lexer import tokenize
from apidsl.parser import parse
from apidsl.printer import format_ast, format_tokens


class UsageError(Exception):
    pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="apidsl", description="Compile API test DSL files to pytest code.")
    commands = parser.add_subparsers(dest="command", required=True)

    compile_command = commands.add_parser("compile", help="compile a .api file to Python")
    compile_command.add_argument("file", type=Path)
    compile_command.add_argument("-o", "--output", type=Path, help="write generated code to this file")
    view = compile_command.add_mutually_exclusive_group()
    view.add_argument("--tokens", action="store_true", help="print tokens and stop")
    view.add_argument("--ast", action="store_true", help="print the AST and stop")

    run_command = commands.add_parser("run", help="compile a .api file and run it with pytest")
    run_command.add_argument("file", type=Path)
    return parser


def read_source(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except OSError as error:
        raise UsageError(f"cannot read {path}: {error.strerror}") from None
    except UnicodeDecodeError:
        raise UsageError(f"cannot read {path}: file is not valid UTF-8") from None


def compile_file(args: argparse.Namespace, source: str) -> int:
    if args.tokens:
        print(format_tokens(tokenize(source)))
        return 0
    if args.ast:
        print(format_ast(parse(source)))
        return 0
    code = compile_source(source, args.file.name)
    if args.output is None:
        sys.stdout.write(code)
        return 0
    try:
        args.output.write_text(code, encoding="utf-8")
    except OSError as error:
        raise UsageError(f"cannot write {args.output}: {error.strerror}") from None
    print(f"compiled {args.file} -> {args.output}")
    return 0


def run_file(args: argparse.Namespace, source: str) -> int:
    code = compile_source(source, args.file.name)
    with tempfile.TemporaryDirectory(prefix="apidsl-") as directory:
        target = Path(directory) / f"test_{slug(args.file.stem)}.py"
        target.write_text(code, encoding="utf-8")
        sys.stdout.flush()
        command = [sys.executable, "-m", "pytest", str(target), "-v", "-p", "no:cacheprovider", "--rootdir", directory]
        return subprocess.run(command, check=False).returncode


def report(path: Path, errors: list[CompileError]) -> None:
    for error in errors:
        print(error.format(str(path)), file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        source = read_source(args.file)
        if args.command == "compile":
            return compile_file(args, source)
        return run_file(args, source)
    except UsageError as error:
        print(f"apidsl: {error}", file=sys.stderr)
        return 2
    except CompileError as error:
        report(args.file, [error])
        return 1
    except CompilationFailed as failure:
        report(args.file, failure.errors)
        return 1
