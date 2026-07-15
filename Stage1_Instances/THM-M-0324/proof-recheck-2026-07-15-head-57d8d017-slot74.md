# THM-M-0324 proof-phase recheck at 57d8d017

Item: `S56-M-0324-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `57d8d01796f84ffc9de9adf1f5d0723555e7babb`

Base tree: `cdea5b3fad713816ee6c9ed6aae7a10f9009a18e`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open. This
current-base recheck adds no proof body and closes no frozen obligation. The
lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4] -> [H1, M3, R4]`.

The existing `Proof.lean` is genuine placeholder-free partial work. It proves
that Schauder partial-sum projections are finite-rank and converge to the
identity uniformly on compact subsets, and that failure of this local
compact-approximation predicate excludes every Schauder basis. The exact
source-faithful approximation-property interface is still planned, however,
so these bodies cannot yet be promoted as closure of the frozen
`M0324-L-PROJECTIONS` or `M0324-L-BASIS-TO-AP` obligations.

## Failed Gate

The first failed proof gate is `M0324-C-SPACE`: no repository-local or pinned
dependency declaration constructs Enflo's counterexample Banach space. Its
Banach packaging, separability, infinite-dimensionality, and failure of the
exact approximation property remain unimplemented. The root cut also retains
the open primary-source and foundation boundaries `M0324-X-SOURCE` and
`M0324-X-FOUNDATION`.

The bounded exact-topic search found only this dossier, mathlib's Schauder
projection APIs, and the adjacent `S1_M_215` approximation vocabulary, which
explicitly records the infinite-dimensional theorem as open. A conditional
composer, an assumed failure predicate, or a nonseparable shortcut would not
prove the frozen target.

## Revalidated Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Finite-rank partial-sum projections and compact-uniform convergence | Exact source topology and property convention remain open |
| `noSchauderBasis_of_not_compactApproximationProperty` | No basis follows from failure of the local predicate | Does not construct failure or an Enflo witness |
| `noBasis_of_basis_implies_property` | Parametric logical contradiction | Consumes both substantive premises |
| `root_of_witness` | Exact existential packaging | Consumes the full witness and three open properties |

All four declarations elaborated at trust level zero with axiom closure exactly
`propext`, `Classical.choice`, and `Quot.sound`. No prohibited proof device was
found.

## Validation

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary Lean objects were
created in a disposable directory inside this worker clone and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | Rank 820; planned; theorem incomplete |
| `cd Formalizations/Lean && timeout 90 lake env lean --version` | 1 | Lake stopped before Lean because pinned `flt-regular` could not resolve `HEAD`; no repair or mutation was attempted |
| Disposable direct pinned-Lean replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` with `--trust=0 -t0` | 0 | `statement_exit=0 obligation_exit=0 proof_exit=0`; exact target and four bodies elaborated with only the three allowed axioms |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | 15 obligations and 55 typed edges passed; denominator `8bfbe341...f101b`; root open at M3 |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected) | No prohibited construct found |
| Bounded exact-topic source search | 0 | No exact Enflo terminal body found |
| `git diff --check -- Stage1_Instances/THM-M-0324` | 0 | No tracked whitespace error before this packet |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is incomplete |

The direct replay used the pinned Lean `4.29.0` executable, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and `LEAN_PATH` assembled from
the existing pinned package build artifacts. This is narrow nonrelease kernel
evidence. It does not replace the user-required `lake env lean` gate, whose
missing `flt-regular` Git artifact is recorded as an environment blocker.

## Retry And Boundary

Resume after a placeholder-free implementation of Enflo's construction and
all downstream analytic packages, with the exact approximation-property
convention crosswalked. An alternative is immutable compatible integration of
an exact Lean 4 terminal proof with full dependency, license, trust, and
provenance evidence. The authoritative dependency lane must restore the pinned
`flt-regular` artifact before Lake replay can pass.

This is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0324-PROOF`, promote state, close the root, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
