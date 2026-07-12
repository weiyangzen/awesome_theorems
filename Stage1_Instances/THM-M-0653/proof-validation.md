# THM-M-0653 proof-phase validation

Item: `S56-M-0653-PROOF`. Base revision:
`6446a4b59b8c8950aa4ba92ab10c8d025ce57fc7`.

## Implemented bodies

`Proof.lean` closes the elementary frozen converse obligation
`M0653-D-CONVERSE`: a single old-language formula defining the new relation in
every model forces two models on the same reduct to agree on that relation.
It also replaces the earlier identity-only root boundary with the truthful
`M0653-T-ASSEMBLE` composition: an explicit premise for the still-open
implicit-to-explicit direction, together with the proved converse, yields the
exact `BethDefinabilityTarget`.

Neither declaration postulates or proves Craig interpolation. The hard
`M0653-D-BETH` branch remains an explicit premise, so the root stays open at
`M3`, and theorem completion is false.

## Commands and results

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, clone, or `.lake` mutation was
performed.

```text
LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
cd Stage1_Instances/THM-M-0653
LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" -o Statement.olean Statement.lean
LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" Proof.lean
rm -f Statement.olean
  exit 0
  explicitToImplicit : ExplicitlyDefines L n T -> ImplicitlyDefines L n T
  explicitToImplicit depends on axioms: [propext, Quot.sound]
  bethDefinability_of_implicitToExplicit :
    (ImplicitlyDefines L n T -> ExplicitlyDefines L n T) ->
      BethDefinabilityTarget L n T
  bethDefinability_of_implicitToExplicit depends on axioms:
    [propext, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0653
  exit 0: rank 698, planned, theorem_complete false
rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-0653/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder
python3 -m json.tool Stage1_Instances/THM-M-0653/proof-receipt.json
  exit 0: valid JSON
git diff --check -- Stage1_Instances/THM-M-0653 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The first open machine cut is the nontrivial Beth direction and its frozen
Craig-interpolation architecture. The anchor audit found no terminal Beth or
Craig theorem in pinned mathlib or a pinnable external Lean project. Thus this
is genuine, narrowly self-tested partial proof progress, not a broadened
theorem, an assumed result, validation/release acceptance, or theorem closure.
