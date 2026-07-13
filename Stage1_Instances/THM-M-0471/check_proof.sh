#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0471"
lean_cache="$repo_root/Formalizations/Lean/.lake"
tmp="$(mktemp -d /tmp/stage1-m0471-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$lean_cache/build/lib/lean:$lean_cache/packages/mathlib/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/batteries/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/Qq/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/aesop/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/proofwidgets/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/importGraph/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/LeanSearchClient/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/plausible/.lake/build/lib/lean"
test -x "$lean_bin"
test -f "$lean_cache/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Nat/Factors.olean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" -o Statement.olean Statement.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" Proof.lean | tee proof.out

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
namespace = "Stage1Instances.THM_M_0471.Proof."
local_declarations = (
    "nonzeroNormalization",
    "primeDvdProduct",
    "primeDivisorMembership",
    "erasePermutation",
    "cancelCommonHead",
    "primeProductPermutation",
    "witnessNonempty",
    "witnessPrimality",
    "witnessProduct",
    "primeFactorUniqueness",
    "primeFactorUniqueness_via_components",
    "exactPrimeListAnchor",
    "fundamentalTheoremOfArithmetic_via_frozen_composition",
    "fundamentalTheoremOfArithmetic",
)
upstream_declarations = (
    "Nat.primeFactorsList_ne_nil",
    "Nat.prime_of_mem_primeFactorsList",
    "Nat.prod_primeFactorsList",
    "Nat.primeFactorsList_unique",
    "perm_of_prod_eq_prod",
    "Prime.dvd_prod_iff",
    "mem_list_primes_of_dvd_prod",
    "List.perm_cons_erase",
    "mul_right_inj'",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in upstream_declarations + tuple(namespace + name for name in local_declarations):
    marker = f"'{declaration}' does not depend on any axioms"
    if marker in output:
        continue
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == 24
assert "sorryAx" not in output
assert "error:" not in output
print("PASS THM-M-0471 Lean proof: 24 declarations sorry-free; axiom closure allowlisted")
PY
