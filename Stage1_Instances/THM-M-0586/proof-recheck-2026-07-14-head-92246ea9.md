# THM-M-0586 proof-phase recheck at `92246ea9`

Item: `S56-M-0586-PROOF`  
Attempt date: 2026-07-14  
Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

## Verdict

`blocked`. No proof body was added, and the proof phase is not self-tested as
complete. The exact root still requires both `M0586-T-FIVE` and
`M0586-T-STABLE`; neither `DimensionFivePackage` nor
`StableDimensionPackage` has a proof-bearing declaration in the repository or
the pinned Lean dependency closure.

Pinned mathlib's matching source name,
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, is introduced only
by `proof_wanted`. A direct environment probe returns `Unknown constant`. A
bounded search across every pinned package finds no h-cobordism, s-cobordism,
surgery, or high-dimensional sphere-homeomorphism proof that supplies either
frozen package.

A fresh bounded Sourcegraph search, including archived repositories and forks,
found the matching name only in mathlib's `proof_wanted` source. The generalized
name matched only LeanMillenniumPrizeProblems, whose proved terminal result is
dimension zero. The broader `PoincareConjecture` search again found Google
DeepMind's `formal-conjectures` source at immutable commit
`b2e608fc52d765510915a244bb69b1a2741acc3c`; the previously inspected
dimension-at-least-five declaration has body `by sorry`, so it is prohibited
and supplies no proof credit. No `hCobordism` or `sCobordism` Lean match was
found. These are bounded search results, not a claim of global absence.

The local theorem `highDimensionalPoincare_of_dimension_packages` re-elaborates
under `--trust=0`; its axiom report is `[propext, Classical.choice, Quot.sound]`.
It remains only a checked composition from the two missing package arguments.
Using that conditional theorem as root closure would hide unresolved premises
and violate the parent-composition gate. No axiom, assumption, placeholder,
weaker dimension range, or substitute theorem was introduced.

## Validation evidence

Commands ran in this worker clone using the automation-provided `.lake`
symlink to the canonical pinned artifacts. The symlink-target SHA-256 is
`e8714e9ebb75a5da1eeb16fdb6f50831a6cab29f115df43fa8e7535b38f59826`.
No Lake update/build, dependency clone/fetch, or `.lake` mutation was
performed. Narrow Lean output and Sourcegraph responses were placed under
`/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117; lifecycle `planned`; baseline `L0/rework_required`; `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | `PASS THM-M-0586 obligation tree: 18 obligations, 38 typed edges`; denominator `bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e`; root open at M3 and both terminal packages M4 |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | `ok: THM-M-0586 anchor inventory, proof_wanted boundary, 8 probes, and immutable pins` |
| `LEAN=$(cd Formalizations/Lean && lake env which lean); LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH); LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 300s "$LEAN" --trust=0 -o /tmp/thm-m-0586-elab-final/Statement.olean Stage1_Instances/THM-M-0586/Statement.lean; LEAN_NUM_THREADS=1 LEAN_PATH="/tmp/thm-m-0586-elab-final:$LP" timeout 300s "$LEAN" --trust=0 Stage1_Instances/THM-M-0586/ObligationTree.lean` | 0 | Both files elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary output was removed |
| Temporary file importing `Mathlib.Geometry.Manifold.PoincareConjecture` and checking `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, run with `lake env lean` | 1 (expected) | `Unknown constant ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`; temporary probe was removed |
| `rg -l -i 'nonempty_homeomorph_sphere\|generalized[ _-]*poincar\|high[ _-]*dimensional[ _-]*poincar\|h[- _]?cobord\|s[- _]?cobord\|surgery' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | The sole pinned-package match was `Mathlib/Geometry/Manifold/PoincareConjecture.lean`, whose relevant entries are `proof_wanted` markers |
| Sourcegraph streaming searches for `nonempty_homeomorph_sphere`, `GeneralizedPoincareConjecture`, `hCobordism`, `sCobordism`, and `PoincareConjecture`, with `lang:Lean archived:yes fork:yes count:100` | 0 | Match counts were 2, 2, 0, 0, and 17, with `skipped=[]`; exact-name results were the mathlib marker and dimension-zero external project, and the broad search additionally exposed the disallowed formal-conjectures source |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0586 --glob '*.lean'` | 1 (expected) | No forbidden Lean proof escape in the owned Lean sources |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the Lake manifest pin |
| `python3 -m json.tool Stage1_Instances/THM-M-0586/proof-blocker.json` | 0 | Existing structured blocker record remains valid JSON |

The Sourcegraph response SHA-256 values, in query order, were
`4582f8111c96c7cb4fd0cf49b9976398e801aa6f6246255bdc26436b0757c64f`,
`bb88ea007eefe947682296362b69abbed26b9543fab711511106cb04745aa1bf`,
`66f63d0914942284f304848268a6600597ac2de98a84737eed96c289f0fce687`,
`4ef8a8f99c38f73b2c305d3e5c99aa9e554e12f9253c6805905ea6a655b5b5e6`,
and `bb7ce1f0437525b475f3ab520e2cfc454a2fc1e1263e50f4d3acd0ca72662a0e`.

## Retry condition

The first failed gate is terminal proof-body availability. The remaining root
cut set is exactly `M0586-T-FIVE` and `M0586-T-STABLE`. Retry after either
placeholder-free local implementations of the frozen puncture, disk,
cobordism, h-/s-cobordism, dimension-five, stable-range, and gluing route, or
an immutable compatible Lean 4 declaration that supplies the exact packages
and passes exact-type, provenance, axiom, placeholder, and composition checks.

This artifact is blocker evidence only. It does not satisfy the assigned proof
item or claim M0, validation, release, theorem completion, or master
acceptance. Because the assigned phase is not genuinely self-tested as
complete, no `.stage1-worker-selftest.json` is emitted.
