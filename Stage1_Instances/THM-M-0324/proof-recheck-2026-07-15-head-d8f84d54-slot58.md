# THM-M-0324 proof-phase recheck at d8f84d54

Item: `S56-M-0324-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `d8f84d5418027a70d6b46b6bdd4eae8b03222636`

Base tree: `c940a8fbfbffa31fd76003aabf250b486fa8a04f`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open. This
current-base execution adds no proof body and closes no frozen obligation. The
lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4] -> [H1, M3, R4]`.

The existing `Proof.lean` is genuine placeholder-free partial work. It proves
that Schauder partial-sum projections have finite-dimensional ranges and
converge to the identity uniformly on compact subsets, and that failure of this
local compact-approximation predicate excludes a Schauder basis. It does not
construct Enflo's counterexample space or prove the failure premise.

The authoritative projection marks prerequisite
`S56-M-0324-OBLIGATION_TREE` provisional, while the target-local task DAG still
marks it open. This worker changes neither state; dependency reconciliation and
acceptance belong to the integration lane.

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
composer, an assumed failure predicate, or a nonseparable shortcut would not
prove the frozen target.

The remaining root cut is `M0324-C-SPACE`, `M0324-X-SOURCE`, and
`M0324-X-FOUNDATION`. The expanded missing proof packages are
`M0324-D-APPROX`, `M0324-C-SPACE`, `M0324-C-BANACH`, `M0324-L-SEPARABLE`,
`M0324-L-INFINITE`, `M0324-L-NO-AP`, `M0324-X-SOURCE`,
`M0324-X-FOUNDATION`, and `M0324-X-PROVENANCE`.

## Revalidated Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Finite-rank partial sums and compact-uniform convergence | Exact source topology and property convention remain open |
| `noSchauderBasis_of_not_compactApproximationProperty` | No basis follows from failure of the local predicate | Does not construct failure or an Enflo witness |
| `noBasis_of_basis_implies_property` | Parametric logical contradiction | Consumes both substantive premises |
| `root_of_witness` | Exact existential packaging | Consumes the full witness and three open properties |

All four declarations elaborated through `lake env lean` at trust level zero
in a disposable module directory. Every printed axiom set was exactly
`propext`, `Classical.choice`, and `Quot.sound`. The owned Lean sources contain
no prohibited proof device.

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
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Disposable ordered replay from the pinned mathlib checkout: `lake env lean --trust=0 -t0` on `Statement.lean`, `ObligationTree.lean`, and `Proof.lean`, using a temporary local module directory and only existing canonical package build paths | 0 | `Statement_exit=0 ObligationTree_exit=0 Proof_exit=0`; exact target and four bodies elaborated; log SHA-256 values `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b` |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | 15 obligations and 55 typed edges passed; denominator `8bfbe341...f101b`; root open at M3 |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected no-match) | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, `run_tac`, or axiom/constant/opaque/unsafe/extern declaration found |
| Exact-topic search over repository Lean sources and existing pinned package sources | 0 | Relevant hits were confined to this dossier, mathlib basis substrate, and open adjacent approximation vocabulary; no exact terminal body found |
| `python3 -m json.tool` on this structured packet | 0 | JSON parsed successfully |
| Whitespace checks on the owned path and both new files | 0 | No whitespace errors; no-index returned only the expected new-file difference status |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is incomplete |

The successful replay used Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. This is real narrow kernel
evidence for the existing partial bodies, not root-closure or release evidence.

## Scheduler Boundary

Eleven earlier unresolved proof-recheck packets existed before this execution,
but the authoritative proof item still records zero attempts and no children.
The integration lane should reconcile the attempt count and split or redirect
the oversized item under blueprint section 10.2 instead of scheduling another
identical whole-root recheck.

Resume proof work only with a placeholder-free implementation of Enflo's
construction and all downstream analytic packages, with the exact
approximation-property convention crosswalked. An alternative is immutable
compatible integration of an exact Lean 4 terminal proof with complete
dependency, license, trust, and provenance evidence.

This is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0324-PROOF`, promote state, close the root, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
