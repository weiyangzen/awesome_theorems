# THM-M-0586 proof-phase recheck

Item: `S56-M-0586-PROOF`  
Attempt date: 2026-07-14  
Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Verdict

`blocked`. No proof body was added, and this phase is not self-tested as
complete. The frozen exact root still requires both `M0586-T-FIVE` and
`M0586-T-STABLE`; neither terminal package has a proof-bearing declaration in
the repository or pinned Lean dependency closure.

Pinned mathlib's matching name
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` remains a
`proof_wanted` source marker rather than an exported constant. A direct Lean
probe again reports `Unknown constant`. A bounded search of every pinned
package found only mathlib's Poincare statement module, not an h-cobordism,
s-cobordism, surgery, or high-dimensional sphere-homeomorphism proof. The
immutable external candidate already recorded by the anchor audit proves only
the dimension-zero generalized case.

`highDimensionalPoincare_of_dimension_packages` re-elaborates and its axiom
report is limited to `propext`, `Classical.choice`, and `Quot.sound`. It is only
the checked composition of the two missing package arguments. Treating that
conditional theorem as root closure would hide the exact unresolved premises
and violate the parent-composition gate.

## Validation evidence

Commands ran in this worker clone using the existing pinned `.lake` symlink.
The worktree began with only that automation-provided untracked symlink,
pointing to the canonical pinned artifacts; its link-target SHA-256 is
`e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826`.
No Lake update/build, dependency clone/fetch, or `.lake` mutation was performed.
Temporary Lean sources and objects were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117; lifecycle `planned`; baseline `L0/rework_required`; `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | `PASS THM-M-0586 obligation tree: 18 obligations, 38 typed edges`; denominator `bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e`; root open at M3 and both terminal packages M4 |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | Anchor inventory, `proof_wanted` boundary, eight probes, and immutable pins agree |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); LEAN_PATH="$LP" "$LEAN" -t 0 -o /tmp/.../Statement.olean Statement.lean; LEAN_PATH="/tmp/...:$LP" "$LEAN" -t 0 ObligationTree.lean` | 0 | Exact target and conditional composition elaborated; `#print axioms` returned `[propext, Classical.choice, Quot.sound]`; temporary output removed |
| temporary file importing `Mathlib.Geometry.Manifold.PoincareConjecture` and checking `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, run with `lake env lean` | 1 (expected) | `Unknown constant ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`; temporary probe removed |
| `rg -n -i 'nonempty_homeomorph_sphere\|generalized[ _-]*poincar\|high[ _-]*dimensional[ _-]*poincar\|h[- _]?cobord\|s[- _]?cobord\|surgery' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | Only `Mathlib/Geometry/Manifold/PoincareConjecture.lean` matched; its relevant declarations are `proof_wanted` |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0586 --glob '*.lean'` | 1 (expected) | No forbidden Lean proof escape found |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the Lake manifest pin |

## Retry condition

The first failed gate is terminal proof-body availability. The remaining root
cut set is exactly `M0586-T-FIVE` and `M0586-T-STABLE`. Retry after either
placeholder-free local implementations of the frozen puncture, disk,
cobordism, h-/s-cobordism, dimension-five, stable-range, and gluing route, or
an immutable compatible Lean 4 declaration that supplies the exact packages
and passes exact-type, provenance, axiom, placeholder, and composition checks.

This artifact is blocker evidence only. It does not satisfy the assigned proof
item or claim M0, validation, release, theorem completion, or master acceptance.
Because the assigned phase is not genuinely self-tested as complete, no
`.stage1-worker-selftest.json` is emitted.
