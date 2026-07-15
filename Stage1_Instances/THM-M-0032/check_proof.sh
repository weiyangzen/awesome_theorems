#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 300s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0032"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0032-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/DomainProof.lean" "$tmp/DomainProof.lean"

cd "$lean_root"
lean="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
for module in Statement ObligationTree DomainProof; do
  if [[ "$module" == "Statement" ]]; then
    module_path="$lean_path"
  else
    module_path="$tmp:$lean_path"
  fi
  if ! LEAN_PATH="$module_path" LEAN_NUM_THREADS=1 "$lean" --trust=0 -t0 \
      --root="$tmp" -o "$tmp/$module.olean" "$tmp/$module.lean" >"$tmp/$module.out" 2>&1; then
    cat "$tmp/$module.out"
    exit 1
  fi
  cat "$tmp/$module.out"
  test -s "$tmp/$module.olean"
done

python3 - "$tmp/DomainProof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
namespace = "Stage1Instances.THM_M_0032.DomainProof."
allowed = {"propext", "Classical.choice", "Quot.sound"}
for name in ("regularLocalRing_isDomain", "regularLocalDomainPackage"):
    declaration = namespace + name
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "contains sorry" not in output
assert "error:" not in output.lower()
print("PASS THM-M-0032 M0032-N-DOMAIN: exact package checked at trust zero")
PY

sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" "$tmp/DomainProof.olean"
