# THM-M-0324 proof-phase recheck at 3c2814a3

Item: `S56-M-0324-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `3c2814a370c2fee02158ca79aa44a48e411c4d18`

Base tree: `e1bd7e27bd922b779322c089410a471b6a1535f0`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open. This
current-base execution adds no proof body and closes no frozen obligation. The
lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4] -> [H1, M3, R4]`.

The existing `Proof.lean` is genuine placeholder-free partial work. It proves
that Schauder partial-sum projections have finite-dimensional ranges and
converge to the identity uniformly on compact subsets. It also proves that
failure of this local compact-approximation predicate excludes a Schauder
basis. It neither constructs Enflo's counterexample nor proves the failure
premise.

## Failed Gate

The first failed proof gate is `M0324-C-SPACE`: no repository-local or pinned
dependency declaration constructs Enflo's counterexample Banach space. Its
Banach packaging, separability, infinite dimensionality, and failure of the
source-faithful approximation property remain unimplemented. The source audit
also has not fixed the exact approximation-property convention, so the local
predicate cannot close the frozen source-dependent nodes.

A bounded exact-topic search found only this dossier, mathlib's Schauder
projection substrate, and the adjacent `S1_M_215` approximation vocabulary,
whose infinite-dimensional terminal theorem is explicitly open. A conditional
composer, an assumed failure predicate, a finite-dimensional or nonseparable
shortcut, or failure of one selected sequence would not prove the frozen root.

Eight earlier recheck packets are present for the same unresolved item while
the authoritative item still records zero attempts. That packet count is
observed evidence rather than an authority edit. The integration lane must
reconcile which runs count as execution ticks and apply the rev-5.6 five-tick
split rule if its threshold has been met.

## Revalidated Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Finite-rank partial sums and compact-uniform convergence | Exact source topology and property convention remain open |
| `noSchauderBasis_of_not_compactApproximationProperty` | No basis follows from failure of the local predicate | Does not construct failure or an Enflo witness |
| `noBasis_of_basis_implies_property` | Parametric logical contradiction | Consumes both substantive premises |
| `root_of_witness` | Exact existential packaging | Consumes the full witness and three open properties |

All four declarations elaborated at trust level zero against the pinned Lean
and already-built package artifacts in a disposable `/tmp` directory. Every
printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound`.
The owned Lean sources contain no prohibited proof device.

## Validation

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary Lean objects and logs
were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | Rank 820; planned; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | Only the pre-existing automation-provided `.lake` symlink was present at start |
| Disposable replay with pinned Lean `--trust=0 -t0` on `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | `statement_exit=0 obligation_exit=0 proof_exit=0`; exact target and four bodies elaborated; log SHA-256 values `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b` |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | 15 obligations and 55 typed edges passed; denominator `8bfbe341...f101b`; root open at M3 |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected no-match) | No prohibited construct found |
| Bounded exact-topic source search | 0 | No exact Enflo terminal body found |

The narrow replay used Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. Its `LEAN_PATH` contained the
disposable module directory and only already-built canonical package
libraries. This is real nonrelease kernel elaboration evidence, but not root
closure or release evidence.

## Retry And Boundary

The master should first reconcile the repeated rechecks and split this
oversized proof node if required. Proof work then needs placeholder-free
implementations of Enflo's construction, Banach packaging, separability,
infinite dimensionality, exact source-crosswalked approximation-property
failure, foundation, and provenance. Alternatively, an immutable compatible
Lean 4 proof of the exact root may be pinned and integrated with full trust and
provenance evidence.

This is a current-base blocker packet, not a proof receipt. It does not satisfy
`S56-M-0324-PROOF`, promote scheduler state, close the root, or claim audit
completion, theorem completion, validation, release, receipt acceptance, or
master acceptance. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
