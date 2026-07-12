# THM-M-0342 proof-phase validation

Item: `S56-M-0342-PROOF`. Base revision:
`396f523f7db5499e43d86728d9cfe073ac081dfa`.

`Proof.lean` discharges the frozen `ExactNormAnchor` by applying the exact
pinned theorem `MeasureTheory.Lp.norm_fourier_eq` to `hf.toLp f`. It then uses
the already checked `root_of_exact_norm_anchor` composition to prove the exact
`PlancherelTarget`, including every natural dimension and the zero-dimensional
case. No hypothesis, domain, measure, scalar field, or conclusion is changed.

This is proof-phase kernel evidence only. It does not claim master acceptance,
human-source closure, readable reconstruction, hermetic validation, independent
verification, release acceptance, or theorem completion.

## Commands and results

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, clone, or `.lake` mutation was
performed.

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0342
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" Proof.lean
rm -f Statement.olean ObligationTree.olean
  exit 0
  exactNormAnchor_proof : ExactNormAnchor
  exactNormAnchor_proof depends on axioms:
    [propext, Classical.choice, Quot.sound]
  plancherelTarget_proof : PlancherelTarget
  plancherelTarget_proof depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0342
  exit 0: rank 835, planned, theorem_complete false
rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0342/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder
python3 -m json.tool Stage1_Instances/THM-M-0342/proof-receipt.json
  exit 0: valid JSON
git diff --check -- Stage1_Instances/THM-M-0342 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The proof-phase exact root is closed provisionally by a pinned imported proof
body and checked local composition. The remaining root cut for overall theorem
completion consists of the separate source, foundation/trust, provenance,
documentation/readability, validation, independent-verification, and release
gates.
