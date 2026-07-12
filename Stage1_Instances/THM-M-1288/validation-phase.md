# THM-M-1288 validation-phase record

Item: `S56-M-1288-VALIDATION`. Base revision:
`aaeade67ccb391b2d10e50e766d54427324b3090`.

## Scope and result

The local validator copied `Statement.lean`, `ObligationTree.lean`,
`Proof.lean`, and `Validation.lean` into a fresh temporary module directory and
elaborated them with the existing pinned Lean environment. `Validation.lean`
imports only the frozen statement and independently reconstructs conditional
root composition plus the domain, gradient, and zero-expression probes. It
does not import or invoke the proof or composition modules.

The narrow kernel, observed-axiom, placeholder/unsafe, frozen-hash, registry,
and pinned local provenance checks passed. This does not close the exact root:
the independent root theorem, like the proof-phase composition theorem, takes
the full admissibility and least-constant packages as explicit premises.

## Commands and exact results

Commands ran from the repository root on 2026-07-12. Existing canonical pinned
`.lake` artifacts were reused; no update, build, clone, fetch, or dependency
mutation was performed.

```text
python3 Stage1_Instances/THM-M-1288/check_validation.py
  exit 0
  ok: exact statement, conditional composition, bounded proof leaves, and independent local probes elaborated
  ok: observed declaration axioms are confined to propext, Classical.choice, and Quot.sound
  ok: placeholder/unsafe scan, frozen hashes, denominator, and clean pinned mathlib provenance checks passed
  open: exact root remains M3 with admissibility and optimality packages unproved
  blocked: cold empty-cache hermetic replay, complete trust/SBOM closure, and distinct-runner independent verification

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups and 1546 uniform-L0 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1288
  exit 0: rank 459, planned lifecycle, theorem_complete=false

python3 Stage1_Instances/THM-M-1288/check_obligation_tree.py
  exit 0: PASS; 19 obligations and 43 typed edges, root open at M3

python3 Stage1_Instances/THM-M-1288/check_proof.py
  exit 0: PASS; bounded local leaves close and root remains conditional

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

git -C Formalizations/Lean/.lake/packages/mathlib status --short
  exit 0: empty output

(cd Formalizations/Lean && lake env lean --version)
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, conditional composition, proof leaves, and differential probes elaborate in a fresh temporary module directory. |
| Exact target identity | pass locally | Both conditional composition implementations conclude the frozen `TalentiSharpSobolevTarget`; neither supplies an analytic premise. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration occurs in the four checked modules. |
| Axiom observation | provisional pass | Checked declarations report only a subset of `propext`, `Classical.choice`, and `Quot.sound`; complete accepted transitive TCB closure is absent. |
| Local provenance | provisional pass | Frozen inputs are hashed, mathlib is clean at its declared pin, and the inspected Sobolev module matches the anchor-audit hash. |
| Root kernel closure | fail closed | `M1288-T-ADMISSIBILITY` and `M1288-T-OPTIMALITY` are explicit unproved premises; root debt remains `M3`. |
| Hermetic replay | fail closed | The run reused shared writable warm `.lake` artifacts and was not an empty-cache, offline, immutable-checkout cold build. |
| Independent verification | fail closed | The differential module is independently written but ran in this worker checkout and shared cache, without a distinct verifier identity or signed runner. |

The first failed node gate is exact root kernel closure. Release-level gates
also fail at cold hermetic reproduction. Therefore `audit_complete=false`,
`theorem_complete=false`, and no release or theorem-completion claim is made.
