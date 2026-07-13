#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1553"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1553-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,ProofLemmas,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -o Statement.olean Statement.lean > "$tmp/statement.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean \
  > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o ProofLemmas.olean ProofLemmas.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 Validation.lean > "$tmp/validation.out"
cat "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
  "$tmp/validation.out" <<'PY'
import hashlib
import re
import sys
from pathlib import Path

statement = Path(sys.argv[1]).read_text(encoding="utf-8")
obligation = Path(sys.argv[2]).read_text(encoding="utf-8")
proof = Path(sys.argv[3]).read_text(encoding="utf-8")
validation = Path(sys.argv[4]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
obligation_declarations = (
    "Stage1Instances.THM_M_1553.hirotaKdVTarget_of_logDerivativeBridge",
)
proof_declarations = (
    "Stage1Instances.THM_M_1553.logarithmic_bilinear_identity",
    "Stage1Instances.THM_M_1553.logDerivativeBridge",
    "Stage1Instances.THM_M_1553.hirotaKdVTarget_proof",
)
validation_declarations = (
    "Stage1Instances.THM_M_1553.Validation."
    "independentlyReconstructedLogarithmicIdentity",
    "Stage1Instances.THM_M_1553.Validation."
    "independentlyReconstructedHirotaKdVTarget",
)

names = (
    "HirotaKdVTarget",
    "mutationNonnegativeTau",
    "mutationChangedKdVSign",
    "mutationDroppedMixedHirotaTerm",
)
starts = []
for name in names:
    marker = f"def Stage1Instances.THM_M_1553.{name} : Prop :="
    position = statement.find(marker)
    assert position >= 0, f"missing elaborated declaration: {name}"
    starts.append(position)
chunks = []
for index, start in enumerate(starts):
    stop = starts[index + 1] if index + 1 < len(starts) else len(statement)
    chunks.append(statement[start:stop].strip())
assert len(set(chunks)) == len(chunks), "a structural mutation matched the target"
assert hashlib.sha256(chunks[0].encode()).hexdigest() == \
    "ef5d4bb909f3eba6d2a347e8bad055e3a4a08402beb725499259bb9bf1a9c3bc"


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for output, declarations in (
    (obligation, obligation_declarations),
    (proof, proof_declarations),
    (validation, validation_declarations),
):
    for declaration in declarations:
        assert observed_axioms(output, declaration) == allowed, declaration

assert proof.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation.count("Declarations are sorry-free!") == len(validation_declarations)
combined = obligation + proof + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
