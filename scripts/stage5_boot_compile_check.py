#!/usr/bin/env python3
"""Read-only syntax compiler for Stage5 BOOT Python artifacts.

The BOOT sandbox executes this reviewed helper with isolated Python.  Unlike
``py_compile``, it never writes bytecode beside an immutable snapshot input.
"""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import sys


class CompileCheckError(RuntimeError):
    pass


def canonical_relative(value: str) -> str:
    pure = PurePosixPath(value)
    if (
        not value
        or "\x00" in value
        or "\\" in value
        or pure.is_absolute()
        or pure.as_posix() != value
        or any(part in {"", ".", ".."} for part in pure.parts)
        or pure.suffix != ".py"
    ):
        raise CompileCheckError(f"unsafe Python source path: {value!r}")
    return value


def check(path_text: str) -> None:
    relative = canonical_relative(path_text)
    path = Path(relative)
    if path.is_symlink() or not path.is_file():
        raise CompileCheckError(f"Python source is not a regular file: {relative}")
    raw = path.read_bytes()
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CompileCheckError(f"Python source is not UTF-8: {relative}") from exc
    compile(source, relative, "exec", dont_inherit=True, optimize=0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args()
    try:
        for value in args.paths:
            check(value)
    except (CompileCheckError, OSError, SyntaxError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"PASS read-only syntax compile files={len(args.paths)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
