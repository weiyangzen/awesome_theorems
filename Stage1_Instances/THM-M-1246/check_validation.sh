#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1246"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1246-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,ObligationTree,RegularizedIBP,SharpEstimate,HardyLimit,Proof,ProofAudit,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --clearenv
  --setenv HOME "$tmp" --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)

run_lean() {
  local module_path="$1"
  local log="$2"
  shift 2
  timeout 540 "${base[@]}" --setenv LEAN_PATH "$module_path" \
    "$lean_bin" --trust=0 -t0 "$@" > "$tmp/$log" 2>&1
}

run_lean "$lean_path" statement.out -o Statement.olean Statement.lean
run_lean "$tmp:$lean_path" obligation.out -o ObligationTree.olean ObligationTree.lean
run_lean "$tmp:$lean_path" ibp.out -o RegularizedIBP.olean RegularizedIBP.lean
run_lean "$tmp:$lean_path" estimate.out -o SharpEstimate.olean SharpEstimate.lean
run_lean "$tmp:$lean_path" limit.out -o HardyLimit.olean HardyLimit.lean
run_lean "$tmp:$lean_path" proof.out -o Proof.olean Proof.lean
run_lean "$tmp:$lean_path" audit.out ProofAudit.lean
rm -f "$tmp/Proof.olean" "$tmp/Proof.ilean" "$tmp/Proof.lean"
test ! -e "$tmp/Proof.olean" && test ! -e "$tmp/Proof.lean"
run_lean "$tmp:$lean_path" validation.out Validation.lean

cat "$tmp"/{statement,obligation,ibp,estimate,limit,proof,audit,validation}.out

python3 - "$tmp/audit.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

audit = Path(sys.argv[1]).read_text(encoding="utf-8")
validation = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
audit_declarations = (
    "Stage1Instances.THM_M_1246.hardyInequalityTarget_iff_expanded",
    "Stage1Instances.THM_M_1246.ObligationTree.root_of_hardyTerminal",
    "Stage1Instances.THM_M_1246.Proof.hardyTerminal",
    "Stage1Instances.THM_M_1246.Proof.hardyInequality",
)
differential_declarations = (
    "Stage1Instances.THM_M_1246.Validation.independentlyReconstructedHardyTerminal",
    "Stage1Instances.THM_M_1246.Validation.independentlyReconstructedHardyInequality",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {name.strip() for name in matches[0].split(",") if name.strip()}


for declaration in audit_declarations:
    assert observed_axioms(audit, declaration) == allowed, declaration
for declaration in differential_declarations:
    assert observed_axioms(validation, declaration) == allowed, declaration
assert audit.count("Declarations are sorry-free!") == len(audit_declarations)
assert validation.count("Declarations are sorry-free!") == len(differential_declarations)
combined = audit + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
print("PASS axiom profile: six exact declarations use only propext, Classical.choice, and Quot.sound")
print("PASS kernel sorry traversal: statement, composition, proof, and no-Proof-module replay roots are sorry-free")
PY
