# THM-M-0586 proof-phase recheck at `40801f37`

Item: `S56-M-0586-PROOF`  
Attempt date: 2026-07-14  
Base revision: `40801f373a9b0443cc58ff8ec365fb5b75c8b8c3`

## Verdict

`blocked`. No proof body was added, and the assigned proof phase is not
self-tested as complete. The exact root still requires both
`M0586-T-FIVE` and `M0586-T-STABLE`; neither frozen terminal package has a
proof-bearing declaration in the repository or the pinned dependency closure.

Pinned mathlib's apparent theorem
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` is only a
`proof_wanted` marker. Batteries elaborates such markers inside
`withoutModifyingEnv`, explicitly discarding them so that they cannot be used
as axioms. A direct environment probe therefore reports `Unknown constant`.
The bounded pinned-package search found no h-cobordism, s-cobordism, surgery,
or high-dimensional sphere-homeomorphism proof supplying either package.

The existing theorem `highDimensionalPoincare_of_dimension_packages`
re-elaborates under `--trust=0`; its axiom report is `[propext,
Classical.choice, Quot.sound]`. It is only the checked composition from the two
missing arguments, not a proof of those arguments. Treating it as root closure
would hide unresolved premises and violate the parent-composition gate. No
axiom, assumption, placeholder, weaker dimension range, or substitute theorem
was introduced.

## Validation evidence

The repository's `.lake` path is the automation-provided symlink to the
canonical pinned artifacts. The top-level Lake manifest has SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`,
and the pinned mathlib checkout is
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No Lake update/build,
explicit dependency clone/fetch, or deliberate `.lake` mutation was requested.
One attempted run of `check_statement.py` nevertheless caused `lake env lean`
to start Lake's automatic fetch path because the shared canonical checkout of
the unrelated optional `flt-regular` package was concurrently incomplete. The
process was terminated, its temporary owned source was removed, and none of
that run is accepted as evidence. The final scoped checks used the now-present
exact manifest revision; their generated Lean output was under `/tmp` and was
removed. This shared-cache run is nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117; lifecycle `planned`; baseline `L0/rework_required`; `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | `PASS THM-M-0586 obligation tree: 18 obligations, 38 typed edges`; denominator `bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e`; root open at M3 and both terminal packages M4 |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | `ok: THM-M-0586 anchor inventory, proof_wanted boundary, 8 probes, and immutable pins` |
| `python3 Stage1_Instances/THM-M-0586/check_statement.py` | terminated (SIGTERM) | Invalid/non-evidence run: nested `lake env lean` attempted an automatic dependency fetch after encountering the concurrently incomplete shared `flt-regular` checkout; the process was stopped and its temporary source was removed |
| Resolve the pinned Lean binary and `LEAN_PATH` with `lake env`; elaborate `Statement.lean` to a temporary `.olean`, then elaborate `ObligationTree.lean` with `LEAN_NUM_THREADS=1`, `--trust=0`, and `-t0` | 0 | Both files elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` SHA-256 was `d0ccb45d0a10e1ed8c96dcbb22f0e203b9c8ca9b0c9d7be998fd8f1110b34cda`, and output SHA-256 values were `13268e72ca35834f922c79bc15e7c8095da9db3291356eadc70fc9e693f2ade7` and `b5b6811e60af5572169faf04689de201889093a68845ce27f5aa5eefaa170f70` |
| Temporary file importing `Mathlib.Geometry.Manifold.PoincareConjecture` and checking `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, elaborated with the same pinned binary and dependency paths | 1 (expected) | `Unknown constant`; output SHA-256 `511e007d3c19a2e7fbac199d7b7b08fbd788a74da0e6dedf1ed924a4265d36e5` |
| `rg -l -i 'nonempty_homeomorph_sphere\|generalized[ _-]*poincar\|high[ _-]*dimensional[ _-]*poincar\|h[- _]?cobord\|s[- _]?cobord\|surgery' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | Sole match: `Mathlib/Geometry/Manifold/PoincareConjecture.lean`, whose relevant Poincare declarations are `proof_wanted` markers |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0586 --glob '*.lean'` | 1 (expected) | No forbidden Lean proof escape in the owned Lean sources |
| `git diff --check -- Stage1_Instances/THM-M-0586` | 0 | No whitespace errors |

The first failed gate is terminal proof-body availability. The remaining root
cut set is exactly `M0586-T-FIVE` and `M0586-T-STABLE`. Retry after either
placeholder-free local implementations of the frozen puncture, disk,
cobordism, h-/s-cobordism, dimension-five, stable-range, and gluing route, or
an immutable compatible Lean 4 declaration that supplies the exact packages
and passes exact-type, provenance, axiom, placeholder, and composition checks.

This file is blocker evidence only. It does not satisfy the assigned proof
item or claim M0, validation, release, theorem completion, or master
acceptance. Because the assigned phase is not genuinely self-tested as
complete, no `.stage1-worker-selftest.json` is emitted.
