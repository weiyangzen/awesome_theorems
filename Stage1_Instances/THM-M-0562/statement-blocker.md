# Statement gate blocker

Item: `S56-M-0562-STATEMENT`  
Theorem: `THM-M-0562`  
Base revision: `d30ab383279f10fe53d90d3c5b5421638c550b25`

Verdict: blocked. No exact canonical Lean target is claimed, and this phase is not self-tested.

## First failed gate

The repository's complete claim-bearing record gives only the title "Thom isomorphism", the
attribution Rene Thom, the year 1954, and the gloss "the Thom isomorphism for vector bundles".
It does not cite a publication, theorem, page, or definitions. That phrase identifies a theorem
family but does not determine a proposition. In particular, it leaves open:

- the bundle category and rank convention, and the separation, compactness, paracompactness, or
  CW hypotheses on the base;
- the coefficient ring or local coefficient system and the meaning of orientability;
- whether an orientation or a normalized Thom class is data, or merely asserted to exist;
- ordinary, compactly supported, relative, or reduced cohomology and its concrete construction;
- disk/sphere bundles, the complement of the zero section, or the Thom-space quotient;
- the cup-product map, grading shift, map direction, and whether naturality is part of the root;
- treatment of rank zero, empty or disconnected bases, and nonorientable bundles.

Each choice changes binders, hypotheses, or the conclusion. Selecting a familiar variant without
an immutable pinpoint source would invent missing mathematics, while encoding the desired
isomorphism as an input field would assume the conclusion. Thus there is no source-justified
ordered binder list, canonical Lean expression, checked transport, normalized expression hash,
minimal import set, or meaningful mutation suite. The rev-5.6 exact-statement gate fails before
proof or anchor evidence may receive credit. The intake vector remains `[H1, M4, R4]`, with audit
completion and theorem completion both false.

## Pinned-environment inspection

The existing pinned environment is usable but cannot resolve the missing proposition. Lean is
`4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The pinned mathlib does contain a `VectorBundle`
structure, but scoped exact-name searches found no Thom class/space/isomorphism declaration and no
files mentioning the singular, reduced, or relative cohomology and cup-product APIs needed by the
intake's intended classical formulation. This is infrastructure evidence only, not the later
formal-anchor audit and not evidence that no external formalization exists.

The worker's `Formalizations/Lean/.lake` is the pre-existing symlink to the canonical pinned
artifacts and was used read-only. No `lake update`, build, clone, fetch, or other dependency
mutation was run. `lake env lean` was deliberately not run on a fabricated target: successful
elaboration of an invented abstract interface would not satisfy exactness.

## Commands and exact results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | exit 0; `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0562` | exit 0; rank 610, lifecycle `planned`, `L0`, `rework_required: true`, legacy artifacts unaccepted, theorem completion false |
| `lake env lean --version` (cwd `Formalizations/Lean`) | exit 0; `Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)` |
| `git -C .lake/packages/mathlib rev-parse HEAD` (cwd `Formalizations/Lean`) | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` (cwd `Formalizations/Lean`) | exit 0; `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `rg -l -w 'Thom' .lake/packages/mathlib/Mathlib -g '*.lean' \| wc -l` | exit 0; `0` |
| `rg -l 'ThomClass\|ThomSpace\|thomIsomorphism\|thom_isomorphism' .lake/packages/mathlib/Mathlib -g '*.lean' \| wc -l` | exit 0; `0` |
| `rg -l 'SingularCohomology\|ReducedCohomology\|RelativeCohomology\|CohomologyTheory\|CupProduct' .lake/packages/mathlib/Mathlib -g '*.lean' \| wc -l` | exit 0; `0` |
| `rg -l 'class VectorBundle\|structure VectorBundle' .lake/packages/mathlib/Mathlib/Topology -g '*.lean' \| wc -l` | exit 0; `1` |

## Retry condition

Provide or approve one immutable primary-source theorem and exact locator, including every
referenced definition. It must fix the bundle and base categories, rank, coefficients, orientation
and Thom-class convention, cohomology and support theory, model of the target pair or Thom space,
grading, map, hypotheses, conclusion, and boundary cases. A pinned Lean dependency must then
provide the required concrete APIs, or they must be implemented without assuming the root. The
statement phase can then transcribe the proposition, minimize imports, elaborate it with the
pinned toolchain, fingerprint it, check any alternate encoding, and mutation-test every material
domain and hypothesis choice.

Until that retry condition is met, no `.stage1-worker-selftest.json` is emitted.
