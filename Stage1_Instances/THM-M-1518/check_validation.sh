#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1518"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1518-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/Stage1_Instances/THM-M-1518"
cp "$target"/{Statement,ObligationTree,Proof,WeakToPointwise,ExactProof,Validation}.lean \
  "$tmp/Stage1_Instances/THM-M-1518/"

cd "$lean_root"
lake_bin="$(lake env which lake)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$lean_root"
)
module="$tmp/Stage1_Instances/THM-M-1518"
"${base[@]}" "$lake_bin" env lean --trust=0 -R "$tmp" \
  -o "$module/Statement.olean" \
  "$module/Statement.lean" > "$tmp/statement.out"
"${base[@]}" --setenv LEAN_PATH "$tmp" \
  "$lake_bin" env lean --trust=0 -R "$tmp" \
  -o "$module/ObligationTree.olean" \
  "$module/ObligationTree.lean" > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp" \
  "$lake_bin" env lean --trust=0 -R "$tmp" -o "$module/Proof.olean" \
  "$module/Proof.lean" > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp" \
  "$lake_bin" env lean --trust=0 -R "$tmp" \
  -o "$module/WeakToPointwise.olean" \
  "$module/WeakToPointwise.lean" > "$tmp/weak.out"
"${base[@]}" --setenv LEAN_PATH "$tmp" \
  "$lake_bin" env lean --trust=0 -R "$tmp" \
  "$module/ExactProof.lean" > "$tmp/exact.out"
"${base[@]}" --setenv LEAN_PATH "$tmp" \
  "$lake_bin" env lean --trust=0 -R "$tmp" \
  "$module/Validation.lean" > "$tmp/validation.out"
cat "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" "$tmp/weak.out" \
  "$tmp/exact.out" "$tmp/validation.out"

python3 - "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" "$tmp/weak.out" \
  "$tmp/exact.out" "$tmp/validation.out" <<'PY'
import hashlib
import re
import sys
from pathlib import Path

outputs = [Path(name).read_text(encoding="utf-8") for name in sys.argv[1:]]
statement, obligation, proof, weak, exact, validation = outputs
allowed = {"propext", "Classical.choice", "Quot.sound"}
checks = (
    (obligation, ("Stage1Instances.THM_M_1518.ObligationTree.exactTarget_of_packages",)),
    (proof, ("Stage1Instances.THM_M_1518.firstVariationFormula",)),
    (weak, ("Stage1Instances.THM_M_1518.ObligationTree.weakToPointwise",)),
    (exact, ("Stage1Instances.THM_M_1518.stationaryActionEulerLagrange",)),
    (validation, (
        "Stage1Instances.THM_M_1518.firstVariationFormula",
        "Stage1Instances.THM_M_1518.ObligationTree.weakToPointwise",
        "Stage1Instances.THM_M_1518.Validation."
        "independentlyRecomposedStationaryActionEulerLagrange",
    )),
)

match = re.search(r" : Prop :=\n(?P<expression>.*)\Z", statement, re.DOTALL)
assert match, "missing explicit canonical target expression"
expression = match.group("expression").strip()
assert hashlib.sha256(expression.encode()).hexdigest() == (
    "4cc15786f13f4e4ad7594012ab3e96613f5bffbf572523e8282b41139fe6979f"
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for output, declarations in checks:
    for declaration in declarations:
        assert observed_axioms(output, declaration) == allowed, declaration

assert validation.count("Declarations are sorry-free!") == 3
combined = "\n".join(outputs)
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
