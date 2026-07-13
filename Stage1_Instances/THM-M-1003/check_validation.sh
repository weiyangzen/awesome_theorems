#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1003"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1003-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
test -x "$lean_bin"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/Martingale/Convergence.olean"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --new-session
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)

"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -t0 -o Statement.olean Statement.lean > "$tmp/statement.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -t0 -o Proof.olean Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -t0 Validation.lean > "$tmp/validation.out"

python3 - "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
  "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

statement, obligation, proof, validation = (
    Path(path).read_text(encoding="utf-8") for path in sys.argv[1:]
)
allowed = {"propext", "Classical.choice", "Quot.sound"}


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


composition = "Stage1Instances.THM_M_1003.root_of_limit_packages"
assert observed_axioms(obligation, composition) == allowed

proof_declarations = (
    "Stage1Instances.THM_M_1003.Proof.convexOn_univ_norm_rpow",
    "Stage1Instances.THM_M_1003.Proof.continuous_norm_rpow",
    "Stage1Instances.THM_M_1003.Proof.eLpNorm_condExp_le",
    "Stage1Instances.THM_M_1003.Proof.boundedCondExpTendstoLp",
    "Stage1Instances.THM_M_1003.Proof.unifIntegrableOfAeBound",
    "Stage1Instances.THM_M_1003.Proof.memLpTendstoCondExp",
    "Stage1Instances.THM_M_1003.Proof.uniformL1Bound",
    "Stage1Instances.THM_M_1003.Proof.limitCandidate",
    "Stage1Instances.THM_M_1003.Proof.candidatePackage",
    "Stage1Instances.THM_M_1003.Proof.uniformL1UI",
    "Stage1Instances.THM_M_1003.Proof.sameExponentNormCanonical",
    "Stage1Instances.THM_M_1003.Proof.sameExponentPackage",
    "Stage1Instances.THM_M_1003.Proof.target",
)
for declaration in proof_declarations:
    assert observed_axioms(proof, declaration) == allowed, declaration

root = "Stage1Instances.THM_M_1003.Proof.target"
probe = "Stage1Instances.THM_M_1003.Validation.exactRootTypeProbe"
assert observed_axioms(validation, root) == allowed
assert observed_axioms(validation, probe) == allowed
assert proof.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation.count("Declarations are sorry-free!") == 2
assert "Stage1Instances.THM_M_1003.Proof.target.{u} : LpMartingaleConvergenceTarget" in proof
combined = statement + obligation + proof + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined

print("PASS THM-M-1003 network-isolated trust-zero kernel replay")
print("PASS exact proof/composition/type probe: propext, Classical.choice, Quot.sound")
print("PASS transitive sorry check: all proof declarations and exact-type probe are sorry-free")
PY
