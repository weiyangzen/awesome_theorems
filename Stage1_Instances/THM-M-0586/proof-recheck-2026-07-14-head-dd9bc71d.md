# THM-M-0586 proof-phase recheck at `dd9bc71d`

Item: `S56-M-0586-PROOF`  
Attempt date: 2026-07-14  
Base revision: `dd9bc71d70586d022d87833d780fbe15959b89b0`  
Base tree: `d096d4ef8804532c9165b75d369f49b7b74945d8`

## Verdict

`blocked`. No proof body was added, and the assigned proof phase is not
self-tested as complete. The exact root still requires both
`M0586-T-FIVE` and `M0586-T-STABLE`. Neither `DimensionFivePackage` nor
`StableDimensionPackage` has a proof-bearing declaration in the repository or
the pinned Lean dependency closure.

Pinned mathlib's matching source name,
`ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, is introduced only
by `proof_wanted`. A direct environment probe returns `Unknown constant`. A
bounded search across every pinned package finds no h-cobordism, s-cobordism,
surgery, or high-dimensional sphere-homeomorphism proof supplying either
frozen package. The immutable external candidate already recorded in
`anchor-audit.json` proves only the dimension-zero generalized case.

The local theorem `highDimensionalPoincare_of_dimension_packages`
re-elaborates under `--trust=0`. Its axiom report is `[propext,
Classical.choice, Quot.sound]`, but it is only checked composition from the two
missing package arguments. Using it as root closure would hide unresolved
premises and violate the parent-composition gate. No axiom, assumption,
placeholder, weaker dimension range, or substitute theorem was introduced.

## Validation evidence

Commands ran in this worker clone. The worktree began with only the
automation-provided untracked `Formalizations/Lean/.lake` symlink; the SHA-256
of its newline-terminated link target is
`e7d8a6bce8b934a5b0dc162324c830c4f26e1146c65bb31e8063491a3f47bfcc`.
The shared canonical `flt-regular` checkout was concurrently incomplete, so
Lake environment resolution stalled. To avoid fetching or changing that
optional dependency, the recorded narrow elaboration invoked the existing
pinned Lean binary with explicit read-only paths to the eight already-built
mathlib dependency libraries. Temporary Lean sources and objects were under
`/tmp` and were removed. No Lake update/build, dependency clone/fetch, or
`.lake` mutation was performed by this worker.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0586` | 0 | Rank 117; lifecycle `planned`; baseline `L0/rework_required`; `theorem_complete: false` |
| `python3 Stage1_Instances/THM-M-0586/check_obligation_tree.py` | 0 | `PASS THM-M-0586 obligation tree: 18 obligations, 38 typed edges`; denominator `bbeb74bba464fc32a5741776c0e5bfa6784f3d7b57a4f4630347f07e73007b3e`; root open at M3 and both terminal packages M4 |
| `python3 Stage1_Instances/THM-M-0586/check_anchor_audit.py` | 0 | `ok: THM-M-0586 anchor inventory, proof_wanted boundary, 8 probes, and immutable pins` |
| Existing Lean 4.29.0 binary with explicit pinned package `LEAN_PATH`: elaborate `Statement.lean` to a temporary `.olean`, then elaborate `ObligationTree.lean` with `--trust=0 -t0` | 0 | Both files elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; temporary output removed. `Statement.lean` printed the canonical explicit target recorded under SHA-256 `48062820803a28b54a2bcf9b1122a10ce4d4b53b1d9e37e5f0c8b119955346e7` in `statement.json` |
| Direct temporary probe importing `Mathlib.Geometry.Manifold.PoincareConjecture` and checking `ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere`, using the same pinned binary and paths | 1 (expected) | `Unknown constant ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere` |
| `rg -l -i 'nonempty_homeomorph_sphere\|generalized[ _-]*poincar\|high[ _-]*dimensional[ _-]*poincar\|h[- _]?cobord\|s[- _]?cobord\|surgery' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | Sole match: `Mathlib/Geometry/Manifold/PoincareConjecture.lean`, whose relevant entry is a `proof_wanted` marker |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0586 --glob '*.lean'` | 1 (expected) | No forbidden Lean proof escape in the owned Lean sources |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the manifest pin |
| `sha256sum Formalizations/Lean/lake-manifest.json Formalizations/Lean/lean-toolchain` | 0 | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` and `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` |

The exact narrow Lean recipe was:

```bash
ROOT=$PWD
LEAN=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
LP="$ROOT/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean:\
$ROOT/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean"
TMP=$(mktemp -d /tmp/thm-m-0586-direct.XXXXXX)
LEAN_PATH="$LP" LEAN_NUM_THREADS=1 "$LEAN" --trust=0 -t0 \
  -o "$TMP/Statement.olean" \
  Stage1_Instances/THM-M-0586/Statement.lean
(cd Stage1_Instances/THM-M-0586 && \
  LEAN_PATH="$TMP:$LP" LEAN_NUM_THREADS=1 "$LEAN" --trust=0 -t0 \
  ObligationTree.lean)
rm -rf "$TMP"
```

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
