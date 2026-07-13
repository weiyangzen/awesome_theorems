# THM-M-1029 proof-phase attempt

Item: `S56-M-1029-PROOF`

Attempt date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `823dfcd5e231e84436ac3d88948d8e669c168fdb`

## Verdict

`blocked`; no proof body was added and no proof credit is claimed.

The exact target `Stage1Instances.THM_M_1029.LevyMartingaleCharacterizationTarget` re-elaborates in
the pinned Lean environment. The existing `root_of_incrementLawPackage` declaration also
kernel-checks, with the axiom report `[propext, Classical.choice, Quot.sound]`, but it is conditional
composition: it accepts all Gaussian increment laws and independence conclusions as the single
premise `IncrementLawPackage`. It does not inhabit that premise or prove Levy's characterization.

The first unavailable frozen obligation is `M1029-N-QUADRATIC-VARIATION`. Pinned mathlib defines
the statement vocabulary (`Martingale`, `Indep`, `HasLaw`, and `gaussianReal`) and characteristic-
function substrate, but its probability tree contains no Brownian/Wiener process, continuous
quadratic-variation theorem, stochastic integral, exponential-martingale bridge, or Levy converse.
The audited external Brownian project is absent from this Lake manifest, uses incompatible Lean and
mathlib revisions, and contains no converse theorem. It therefore cannot supply a pinned proof body.

Closing the exact root would require the full frozen route: derive deterministic quadratic variation
from the two martingale hypotheses, construct the complex exponential process, prove its martingale
property, derive the conditional characteristic function, and then obtain both the Gaussian law and
independence of each increment. The immediate semantic root cut remains `M1029-T-INCREMENTS`.
Postulating any package, importing an incompatible partial API as though it were exact, or retaining
the package as an assumption would be a placeholder or a substituted theorem. The root therefore
remains `[H2, M3, R4]`, and `theorem_complete=false`.

Because the assigned proof deliverable is incomplete, `.stage1-worker-selftest.json` is deliberately
absent. This blocker is not a proof receipt and does not satisfy the proof item.

## Narrow validation evidence

All commands ran in this worker clone using the existing pinned `.lake` artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1029` | 0 | rank 222; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1029/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `f5ba78d2...fb4`; root open `M3`, increment package `M4` |
| isolated temporary-olean `lake env lean --trust=0` recipe for `Statement.lean` and `ObligationTree.lean` | 0 | exact target and conditional composition elaborated; `#print axioms` reported `propext`, `Classical.choice`, and `Quot.sound` |
| pinned probability-tree search for Brownian/Wiener, quadratic variation, stochastic integral, exponential martingale, or Levy characterization | 1 | no matches; ripgrep exit 1 is the expected no-match result |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386...a95`; tree `bdc39a...c2b` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e...fab16740`, Release |
| `sha256sum` on the statement, obligation tree, registry, typed graphs, and Lake manifest | 0 | exact hashes recorded in `proof-blocker-2026-07-14.json` |
| `python3 -m json.tool Stage1_Instances/THM-M-1029/proof-blocker-2026-07-14.json` | 0 | structured blocker syntax passed |
| prohibited-construct scan over owned `*.lean` sources | 1 | no matches; ripgrep exit 1 is the expected no-match result |
| `test ! -e .stage1-worker-selftest.json` | 0 | incomplete proof phase has no completion self-test manifest |
| `git diff --check -- Stage1_Instances/THM-M-1029` | 0 | no scoped whitespace errors |

## Reopen condition

Resume after implementing the frozen analytic packages without placeholders, or after locating an
immutable compatible Lean 4 Levy-characterization proof whose exact type, terminal bodies,
dependencies, axioms, license, and provenance can be validated against the pinned environment.
