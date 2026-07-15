# THM-M-0324 proof-phase recheck at 714fb3bb

Item: `S56-M-0324-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `714fb3bb6a070c2f659ece069f1a7219f9c045a0`

Base tree: `2c99a78c5fa247aebc885f31e6818fc029f17a60`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open. This
current-base execution adds no proof body and closes no frozen obligation. The
lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4] -> [H1, M3, R4]`.

The existing `Proof.lean` is genuine placeholder-free partial work. It proves
that Schauder partial-sum projections have finite-dimensional ranges and
converge to the identity uniformly on compact subsets, and that failure of
this local compact-approximation predicate excludes a Schauder basis. It does
not construct Enflo's space or prove the failure premise.

## Failed Gate

The first failed proof gate is `M0324-C-SPACE`: no repository-local or pinned
dependency declaration constructs Enflo's counterexample Banach space. The
Banach packaging, separability, infinite dimensionality, and failure of the
source-faithful approximation property remain unimplemented. The source audit
also has not fixed the exact approximation-property convention, so the local
predicate cannot be credited as closure of the frozen source-dependent nodes.

The bounded exact-topic search found only this dossier, mathlib's Schauder
projection substrate, and the adjacent `S1_M_215` approximation vocabulary,
which explicitly records its infinite-dimensional terminal theorem as open.
A conditional composer, an assumed failure predicate, or a nonseparable
shortcut would not prove the frozen target.

## Revalidated Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Finite-rank partial sums and compact-uniform convergence | Exact source topology and property convention remain open |
| `noSchauderBasis_of_not_compactApproximationProperty` | No basis follows from failure of the local predicate | Does not construct failure or an Enflo witness |
| `noBasis_of_basis_implies_property` | Parametric logical contradiction | Consumes both substantive premises |
| `root_of_witness` | Exact existential packaging | Consumes the full witness and three open properties |

All four declarations elaborated through `lake env lean` at trust level zero.
Every printed axiom set was exactly `propext`, `Classical.choice`, and
`Quot.sound`. The owned Lean sources contain no prohibited proof device.

## Validation

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary Lean objects and logs
were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | Rank 820; planned; theorem incomplete |
| Disposable replay from the pinned mathlib checkout: `lake env lean --trust=0 -t0` on `Statement.lean`, then `ObligationTree.lean`, then `Proof.lean` | 0 | `statement_exit=0 obligation_exit=0 proof_exit=0`; exact target and four bodies elaborated; log SHA-256 values `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b` |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | 15 obligations and 55 typed edges passed; denominator `8bfbe341...f101b`; root open at M3 |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected no-match) | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, axiom/constant/opaque/unsafe/extern declaration, or `run_tac` found |
| Bounded exact-topic source search | 0 | No exact Enflo terminal body found |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 timeout 90 lake env lean --version` | 124 | Top-level Lake resolution timed out before Lean because the pre-existing `flt-regular` package has unresolved Git metadata; no repair or mutation was attempted |
| `git diff --check -- Stage1_Instances/THM-M-0324` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is incomplete |

The successful narrow replay used Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, through `lake env lean` from the
pinned mathlib checkout. `LEAN_PATH` was assembled from existing pinned package
build artifacts and prepended with the disposable module directory. This is
real kernel elaboration evidence, but not release or root-closure evidence.

## Retry And Boundary

Resume after a placeholder-free implementation of Enflo's construction and
all downstream analytic packages, with the exact approximation-property
convention crosswalked. An alternative is immutable compatible integration of
an exact Lean 4 terminal proof with complete dependency, license, trust, and
provenance evidence. The authoritative dependency lane must also restore the
pinned `flt-regular` artifact before top-level Lake replay can pass.

This is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0324-PROOF`, promote state, close the root, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
