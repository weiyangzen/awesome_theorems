# THM-M-0396 proof-phase validation

## Implemented body

`Proof.lean` closes the elementary normalization obligation `M0396-N1` for the
frozen multiplicative formulation. It proves that exponentiating the finite
sum of integer coefficients times real logarithms recovers exactly
`algebraicProduct`, using the root's positivity hypothesis. It also supplies a
proof-phase copy of the checked `CoreEstimate`-to-`Statement` composition.

These are real proof bodies, but they do not prove or assume the Baker-Matveev
estimate. The determinant construction, its nonvanishing, arithmetic lower
bound, analytic upper bound, explicit constant optimization, terminal estimate,
and root remain open. Root status stays `M3`; theorem completion is not claimed.

## Commands and results

Commands ran from base revision
`a4db97af3ce0f2ed97c808ae6085a1df22608ba1` on 2026-07-12 (validation
timestamp `2026-07-11T19:35:36Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0396
  exit 0: execution rank 9; planned; theorem_complete=false

cd Formalizations/Lean &&
  tmp=$(mktemp -d ./.m0396-proof.XXXXXX); trap 'rm -rf "$tmp"' EXIT;
  cp ../../Stage1_Instances/THM-M-0396/{Statement,ObligationTree,Proof}.lean "$tmp/";
  lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean" &&
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean
    -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" &&
  LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean "$tmp/Proof.lean"
  exit 0: all three modules elaborated; each proof declaration reports only
  propext, Classical.choice, and Quot.sound

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0396/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder

python3 -m json.tool Stage1_Instances/THM-M-0396/proof-receipt.json >/dev/null
  exit 0: proof receipt is valid JSON

git diff --check -- Stage1_Instances/THM-M-0396 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
temporary `.olean` files were removed by the command trap. This proof phase is
a truthful partial execution result pending master acceptance. Validation and
release remain separate downstream items.
