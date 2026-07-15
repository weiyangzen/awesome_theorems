#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 900s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0996"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0996-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

module_dir="$tmp/Stage1_Instances/THM-M-0996"
mkdir -p "$module_dir"
cp "$target/Statement.lean" "$target/ObligationTree.lean" "$target/Proof.lean" \
  "$module_dir/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

run_lean() {
  local seconds="$1"
  shift
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
    timeout --foreground "$seconds" "$lean_bin" --trust=0 -t0 -R "$tmp" "$@"
}

run_lean 120 -o "$module_dir/Statement.olean" "$module_dir/Statement.lean" \
  >"$tmp/statement.out" 2>&1
run_lean 180 -o "$module_dir/ObligationTree.olean" "$module_dir/ObligationTree.lean" \
  >"$tmp/obligation-tree.out" 2>&1
run_lean 540 -o "$module_dir/Proof.olean" "$module_dir/Proof.lean" \
  >"$tmp/proof.out" 2>&1

python3 - "$module_dir/ObligationTree.lean" "$module_dir/Proof.lean" \
  "$tmp/statement.out" "$tmp/obligation-tree.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

tree_source, proof_source, statement_log, tree_log, proof_log = map(Path, sys.argv[1:])
allowed = {"propext", "Classical.choice", "Quot.sound"}


def printed_declarations(path: Path) -> list[str]:
    values = re.findall(r"^#print axioms\s+(\S+)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    assert values, f"no #print axioms declarations in {path.name}"
    assert len(values) == len(set(values)), f"duplicate #print axioms declaration in {path.name}"
    return values


def check_axioms(path: Path, declarations: list[str]) -> None:
    output = path.read_text(encoding="utf-8")
    assert "sorryAx" not in output
    assert "declaration uses 'sorry'" not in output
    assert "error:" not in output
    for declaration in declarations:
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
            output,
            re.DOTALL,
        )
        assert match, f"missing axiom report for {declaration}"
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"


statement_output = statement_log.read_text(encoding="utf-8")
assert "error:" not in statement_output
tree_declarations = printed_declarations(tree_source)
proof_declarations = printed_declarations(proof_source)
check_axioms(tree_log, tree_declarations)
check_axioms(proof_log, proof_declarations)
print(
    "PASS THM-M-0996 isolated module chain: "
    f"Statement -> ObligationTree ({len(tree_declarations)}) -> Proof ({len(proof_declarations)})"
)
PY

printf 'STATEMENT_SOURCE_SHA256=%s\n' "$(sha256sum "$module_dir/Statement.lean" | cut -d' ' -f1)"
printf 'OBLIGATION_TREE_SOURCE_SHA256=%s\n' "$(sha256sum "$module_dir/ObligationTree.lean" | cut -d' ' -f1)"
printf 'PROOF_SOURCE_SHA256=%s\n' "$(sha256sum "$module_dir/Proof.lean" | cut -d' ' -f1)"
printf 'STATEMENT_OUTPUT_SHA256=%s\n' "$(sha256sum "$tmp/statement.out" | cut -d' ' -f1)"
printf 'OBLIGATION_TREE_OUTPUT_SHA256=%s\n' "$(sha256sum "$tmp/obligation-tree.out" | cut -d' ' -f1)"
printf 'PROOF_OUTPUT_SHA256=%s\n' "$(sha256sum "$tmp/proof.out" | cut -d' ' -f1)"
printf 'STATEMENT_OLEAN_SHA256=%s\n' "$(sha256sum "$module_dir/Statement.olean" | cut -d' ' -f1)"
printf 'OBLIGATION_TREE_OLEAN_SHA256=%s\n' "$(sha256sum "$module_dir/ObligationTree.olean" | cut -d' ' -f1)"
printf 'PROOF_OLEAN_SHA256=%s\n' "$(sha256sum "$module_dir/Proof.olean" | cut -d' ' -f1)"

printf 'PASS THM-M-0996 trust-zero isolated replay\n'
