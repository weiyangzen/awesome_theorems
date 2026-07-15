#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 600s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0005"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0005-direct-sum-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target/KunnethStatement.lean" "$target/ProofDirectSum20260715Head5bb51543Slot21.lean" \
  "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

run_lean() {
  local source="$1"
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
    timeout --foreground 540s "$lean_bin" --trust=0 -t0 -R "$tmp" \
      -o "$tmp/${source%.lean}.olean" "$tmp/$source"
}

run_lean KunnethStatement.lean >"$tmp/statement.out" 2>&1
run_lean ProofDirectSum20260715Head5bb51543Slot21.lean >"$tmp/proof.out" 2>&1

python3 - "$tmp/ProofDirectSum20260715Head5bb51543Slot21.lean" "$tmp/statement.out" \
  "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

proof_source, statement_log, proof_log = map(Path, sys.argv[1:])
allowed = {"propext", "Classical.choice", "Quot.sound"}

source = proof_source.read_text(encoding="utf-8")
source_without_comments = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
source_without_comments = re.sub(r"--.*", "", source_without_comments)
prohibited = re.compile(
    r"\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|"
    r"^[ \t]*(?:axiom|constant|opaque|unsafe|extern)\b",
    re.MULTILINE,
)
assert prohibited.search(source_without_comments) is None
short_declarations = re.findall(r"^#print axioms\s+(\S+)\s*$", source, re.MULTILINE)
assert len(short_declarations) == 8, short_declarations
assert len(short_declarations) == len(set(short_declarations))

assert "error:" not in statement_log.read_text(encoding="utf-8")
output = proof_log.read_text(encoding="utf-8")
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
namespace = "AwesomeTheorems.Stage1.THM_M_0005.ProofDirectSum20260715Head5bb51543Slot21"
for short_declaration in short_declarations:
    declaration = f"{namespace}.{short_declaration}"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"

print("PASS THM-M-0005 direct-sum proof: eight declarations checked under --trust=0")
print("provisional closures: none; root remains open M3; theorem_complete=false")
PY

printf 'STATEMENT_SOURCE_SHA256=%s\n' \
  "$(sha256sum "$tmp/KunnethStatement.lean" | cut -d' ' -f1)"
printf 'PROOF_SOURCE_SHA256=%s\n' \
  "$(sha256sum "$tmp/ProofDirectSum20260715Head5bb51543Slot21.lean" | cut -d' ' -f1)"
printf 'STATEMENT_OUTPUT_SHA256=%s\n' "$(sha256sum "$tmp/statement.out" | cut -d' ' -f1)"
printf 'PROOF_OUTPUT_SHA256=%s\n' "$(sha256sum "$tmp/proof.out" | cut -d' ' -f1)"
printf 'STATEMENT_OLEAN_SHA256=%s\n' \
  "$(sha256sum "$tmp/KunnethStatement.olean" | cut -d' ' -f1)"
printf 'PROOF_OLEAN_SHA256=%s\n' \
  "$(sha256sum "$tmp/ProofDirectSum20260715Head5bb51543Slot21.olean" | cut -d' ' -f1)"
