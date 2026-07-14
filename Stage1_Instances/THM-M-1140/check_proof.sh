#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-1140"
tmp=$(mktemp -d /tmp/thm-m-1140-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
evidence_dir=${THM_M_1140_EVIDENCE_DIR:-}

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"

lean_path=$(cd "$root/Formalizations/Lean" && lake env bash -c 'printf %s "$LEAN_PATH"')
lean_env=(lake env lean)
test -d "$root/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean"

(
  cd "$root/Formalizations/Lean"
  LEAN_NUM_THREADS=2 LEAN_PATH="$lean_path" \
    "${lean_env[@]}" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
) \
  > "$tmp/statement.out" 2>&1
(
  cd "$root/Formalizations/Lean"
  LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
    "${lean_env[@]}" --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
) \
  > "$tmp/obligation.out" 2>&1
(
  cd "$root/Formalizations/Lean"
  LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
    "${lean_env[@]}" --trust=0 -t0 -R "$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
) \
  > "$tmp/proof.out" 2>&1

python3 - "$tmp/obligation.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

allowed = {"propext", "Classical.choice", "Quot.sound"}
checks = {
    Path(sys.argv[1]): [
        ("Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple_of_packages", False),
    ],
    Path(sys.argv[2]): [
        ("Stage1Instances.THM_M_1140.interiorLocalRigidity", True),
        ("Stage1Instances.THM_M_1140.connectedLevelPropagation", True),
        ("Stage1Instances.THM_M_1140.harmonicStrongMaximumPrinciple", True),
    ],
}
for path, declarations in checks.items():
    output = path.read_text(encoding="utf-8")
    assert "sorryAx" not in output, f"sorryAx reported in {path}"
    assert "declaration uses 'sorry'" not in output, f"sorry declaration reported in {path}"
    assert "error:" not in output, f"Lean error reported in {path}"
    for declaration, has_sorry_report in declarations:
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
            output,
            re.DOTALL,
        )
        assert match, f"missing axiom report for {declaration}"
        actual = {name.strip() for name in match.group(1).split(",")}
        assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
    expected_sorry_reports = sum(has_report for _, has_report in declarations)
    assert output.count("Declarations are sorry-free!") == expected_sorry_reports, (
        f"unexpected number of sorry-free reports in {path}"
    )
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
if test -n "$evidence_dir"; then
  mkdir -p "$evidence_dir"
  cp "$tmp/statement.out" "$evidence_dir/statement.out"
  cp "$tmp/obligation.out" "$evidence_dir/obligation.out"
  cp "$tmp/proof.out" "$evidence_dir/proof.out"
fi
echo "PASS THM-M-1140 isolated trust-zero proof elaboration"
