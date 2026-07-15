# THM-M-0324 proof-phase recheck at 90a1d52c

Item: `S56-M-0324-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `90a1d52c43113012c8aa0e2b110da02e58ce1724`

Base tree: `bc399f3ba59411f2a72d4f29d98eb85e7689b28c`

## Verdict

`blocked`. The exact target
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open. This
current-base execution adds no proof body and closes no frozen obligation. The
lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4] -> [H1, M3, R4]`.

The existing `Proof.lean` remains genuine placeholder-free partial work. It
proves that Schauder partial-sum projections have finite-dimensional ranges
and converge to the identity uniformly on compact subsets, and that failure
of this local compact-approximation predicate excludes a Schauder basis. It
does not construct Enflo's counterexample or prove the failure premise.

## Failed Gate

The first failed proof gate is `M0324-C-SPACE`: no repository-local or pinned
dependency declaration constructs Enflo's counterexample Banach space. Its
Banach packaging, separability, infinite dimensionality, and failure of the
source-faithful approximation property remain unimplemented. The source audit
also has not fixed the exact approximation-property convention, so the local
predicate cannot close the frozen source-dependent nodes.

A bounded exact-topic search found only this dossier, mathlib's Schauder
projection substrate, and the adjacent `S1_M_215` approximation vocabulary,
which explicitly records its infinite-dimensional terminal theorem as open.
Three independent read-only audits found no exact local or pinned terminal
body. A conditional composer, an assumed failure predicate, or a nonseparable
shortcut would not prove the frozen target.

## Revalidated Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Finite-rank partial sums and compact-uniform convergence | Exact source topology and property convention remain open |
| `noSchauderBasis_of_not_compactApproximationProperty` | No basis follows from failure of the local predicate | Does not construct failure or an Enflo witness |
| `noBasis_of_basis_implies_property` | Parametric logical contradiction | Consumes both substantive premises |
| `root_of_witness` | Exact existential packaging | Consumes the full witness and three open properties |

All four declarations elaborated through the existing pinned `lake env lean`
environment at trust level zero in a disposable module directory. Every
printed axiom set was exactly `propext`, `Classical.choice`, and `Quot.sound`.
The owned Lean sources contain no prohibited proof device.

## Validation

The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed. Temporary Lean objects and logs
were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | Rank 820; planned; theorem incomplete |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 lake env lean --version` | 0 | Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| Disposable ordered replay with the pinned executable selected by `lake env`, `LEAN_NUM_THREADS=1`, explicit temporary `LEAN_PATH`, and `--trust=0 -t0` on `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | `Statement_exit=0 ObligationTree_exit=0 Proof_exit=0`; log SHA-256 values `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b` |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | 15 obligations and 55 typed edges passed; denominator `8bfbe341...f101b`; root open at M3 |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected no-match) | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, axiom/constant/opaque/unsafe/extern declaration, or `run_tac` found |
| Bounded exact-topic source search | 0 | No exact Enflo terminal body found |
| `python3 -m json.tool Stage1_Instances/THM-M-0324/proof-recheck-2026-07-15-head-90a1d52c-slot54.json` | 0 | Structured blocker parsed successfully |
| `git diff --check` plus no-index checks for both new owned files | 0 | No whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is incomplete |

The successful narrow replay used mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. This is real nonrelease kernel
elaboration evidence for the existing partial bodies, but not root-closure or
release evidence.

## Retry And Boundary

There are 17 earlier structured proof packets: the initial partial
implementation plus 16 unresolved whole-item rechecks, all retaining the same
`M0324-C-SPACE` blocker. The authoritative item still records `attempts=0` and
no children. Blueprint section 10.2 requires a split after five unresolved
execution ticks. The master must reconcile which packets count as execution
ticks and split or redirect this oversized proof item; this worker cannot edit
scheduler state.

Resume the resulting proof children only with placeholder-free implementations
of Enflo's construction, Banach packaging, separability, infinite dimension,
exact source-crosswalked approximation-property failure, foundation, and
provenance packages. The only valid alternative is immutable compatible
integration of an exact Lean 4 terminal proof with complete dependency,
license, trust, and provenance evidence.

This is current-base blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0324-PROOF`, promote state, close the root, or claim audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
