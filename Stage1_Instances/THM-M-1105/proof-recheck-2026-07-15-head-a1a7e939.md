# THM-M-1105 proof-phase recheck at `a1a7e939`

Item: `S56-M-1105-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `a1a7e939e58f103f5ff5d23af51437fa8658aa04`

Base tree: `d881fd9641fa3e5f3ebe5082b35672981e90adcf`

## Verdict

`blocked`. No eligible positive proof body was implemented or found for the exact target
`Stage1.THM_M_1105.WignerSemicircleLaw`. The frozen registry has 20 machine-required obligations;
all have `terminal_proof_body_id: null`, the closed-obligation set is empty, and the root remains
open at `[H2, M3, R4]`.

The existing declaration
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence` is a checked conditional
composition only. Its `terminal` binder assumes `SampleWeakConvergence` almost everywhere, which
is precisely the open analytic conclusion. It therefore does not close `M1105-T-WEAK`,
`M1105-T-COMPOSE`, or the root.

The graph-derived minimal root cut is `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. The complete missing
proof route also includes trace expansion, walk classification, independence cancellation,
Catalan enumeration, expected and almost-sure moment convergence, semicircle moments, polynomial
extension, and final weak-convergence composition. Adding one of those results as an axiom,
bodyless declaration, or assumed terminal would be a prohibited placeholder.

## Candidate Recheck

The pinned mathlib revision still has no Wigner or random-matrix semicircle declaration. Its
Hermitian spectrum, trace, independence, and weak-convergence interfaces are supporting APIs, not
proof bodies for the frozen obligations. The earlier immutable audits of
`Wondermonger-daydreaming/semicircle-catalan@95d99de4` and
`dududuguo/HighDimProb@8d4eec8` likewise provide only partial combinatorial or infrastructural
material.

A newly discovered public project was inspected at the immutable revision
`FredRaj3/SemicircleLaw@724f9ad681a2da6ffe6be02fc3e11a38c4b1b701`. Its immutable GitHub archive
has SHA-256 `8082d2c16de9df218d278091ae1c3936c7fa520b63959872d7f89a3fadde94ee`; it is MIT-licensed and
uses Lean 4.24.0 with mathlib `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`. It is not a proof
candidate:

- its Lean sources contain 25 `sorry` tokens, including the Wigner probability-space,
  measurability, law, odd/even moment-limit, variance-limit, and loop-walk packages;
- it contains no Lean declaration for weak or almost-sure empirical spectral convergence, and its
  blueprint root is marked `notready`;
- its planned root is convergence in probability for a specially constructed common-law ensemble,
  not the frozen target's almost-sure theorem for arbitrary bounded triangular arrays on one
  probability space; and
- it is neither in the pinned Lake closure nor toolchain-compatible with the current project.

The archive was inspected under `/tmp` only. It was not installed, built, cloned into the project,
or added to `.lake`. It earns no proof credit and does not convert the remaining work into
repo-local integration debt.

## Validation

All credited checks reused the automation-provided canonical pinned artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
pre-existing untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1,546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | rank 545; planned; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root open at M3 |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean)` | 0 | exact canonical proposition elaborated; only expected unused-hypothesis linter warnings |
| `(cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/ObligationTree.lean)` | 0 | conditional terminal-to-root composition elaborated; only expected unused-hypothesis linter warnings |
| `rg -n --pcre2 '\b(?:sorry\|admit\|sorryAx\|native_decide\|implemented_by)\b\|^[[:space:]]*(?:axiom\|unsafe\|external\|opaque\|constant)[[:space:]]' Stage1_Instances/THM-M-1105 --glob '*.lean'` | 1 | expected no-match exit; no prohibited construct in owned Lean sources |
| immutable archive scan of `FredRaj3/SemicircleLaw@724f9ad6` | 0 | 25 `sorry` tokens found; the three Wigner asymptotic declarations have `by sorry`; no weak-convergence declaration |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386...ea95`, tree `bdc39a31...1c2b` |

Proof-relevant SHA-256 values are `b7e0e83c...fdf75b` for `Statement.lean`,
`922a4b40...84c0` for `ObligationTree.lean`, `f5561115...45cb` for the registry, and
`d3ce5de6...2987` for the typed graphs. The pinned Lake manifest and toolchain hashes are
`321626c8...2d81` and `651c8acc...b1d2`.

## Retry Condition

Resume after placeholder-free implementations of the frozen moment-method and weak-convergence
packages, or after an immutable exact-scope Lean 4 theorem becomes available for dependency-legal
pinning, exact-type transport, and provenance validation. A future update of the FredRaj3 project
would have to remove the relevant placeholders, supply a terminal convergence theorem, and bridge
its weaker/different ensemble and convergence mode before it could be reconsidered.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1105-PROOF`, change scheduler state, or support audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned proof phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` is deliberately absent.
