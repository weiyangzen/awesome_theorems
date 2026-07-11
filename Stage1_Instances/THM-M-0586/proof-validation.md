# THM-M-0586 proof-phase blocker

Item: `S56-M-0586-PROOF`  
Attempt date: 2026-07-12  
Base revision: `29490c1ef89c2a6c9eb8dcfc4888b8761f710422`

## Verdict

The assigned proof phase is blocked and is not self-tested as complete. No
`.stage1-worker-selftest.json` is emitted.

The frozen exact root needs both `DimensionFivePackage` and
`StableDimensionPackage`. Neither package has a proof-bearing declaration in
the repository or pinned mathlib closure. The only apparent matching mathlib
name, `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, is introduced
by `proof_wanted` and is not an environment constant. The bounded source search
found no additional pinned mathlib file mentioning the needed h-cobordism,
s-cobordism, surgery, or exact homeomorphism result. The already audited
immutable external candidate proves only dimension zero.

`highDimensionalPoincare_of_dimension_packages` was re-elaborated successfully,
but it is only a conditional composition whose two arguments are precisely the
missing mathematical proofs. Treating it as root closure would move those
assumptions out of sight rather than prove them. Closing the root therefore
requires a new formalization of the puncture, disk, cobordism,
h-cobordism/s-cobordism, and gluing packages. No axiom, placeholder, changed
dimension range, or weaker theorem was added.

## Validation Evidence

Commands ran in this worker clone using only the existing pinned Lake artifacts.
No update, build, clone, fetch, or `.lake` mutation was performed. Temporary
`.olean` output was placed under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117, lifecycle `planned`, baseline L0/rework-required, and `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | `PASS THM-M-0586 obligation tree: 18 obligations, 38 typed edges`; denominator `bbeb74...07b3e`; root open at M3 and both packages M4 |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); cd Stage1_Instances/THM-M-0586; LEAN_PATH="$LP" "$LEAN" -o /tmp/thm-m-0586-proof/Statement.olean Statement.lean; LEAN_PATH="/tmp/thm-m-0586-proof:$LP" "$LEAN" ObligationTree.lean` | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0586` | 1 | Expected no-match result: no prohibited Lean declaration token |
| `rg -l -i 'h.?cobord\|s.?cobord\|surgery\|nonempty_homeomorph_sphere' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | Only `Mathlib/Geometry/Manifold/PoincareConjecture.lean` matched |

The first failed proof gate is terminal proof-body availability for
`M0586-T-FIVE` and `M0586-T-STABLE`; these two obligations are the remaining
root cut set. This record is blocker evidence only and claims no proof closure,
M0 status, validation, release, theorem completion, or master acceptance.
