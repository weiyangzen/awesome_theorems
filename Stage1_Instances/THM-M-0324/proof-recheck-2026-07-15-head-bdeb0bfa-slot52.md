# THM-M-0324 proof-phase handoff at bdeb0bfa

Item: `S56-M-0324-PROOF`

Recorded: `2026-07-15T21:26:05+08:00` (`Asia/Shanghai`)

Base revision: `bdeb0bfae66ccfe8b672776c61bc4c74a25bef3d`

Base tree: `440ac842583ec6b7aa7be989ba908e8b745978b9`

## Verdict

`blocked`. The exact root
`Stage1Instances.THM_M_0324.EnfloNoSchauderBasisTarget` remains open. No
placeholder-free local or pinned declaration constructs Enflo's counterexample
space, so this execution adds no proof body and closes no frozen obligation.
The lifecycle remains `planned`, and the root vector remains
`[H1, M3, R4] -> [H1, M3, R4]`.

The existing `Proof.lean` is genuine partial work. It proves that Schauder
partial-sum projections have finite-dimensional ranges and converge uniformly
on compact subsets, and that failure of this local compact-approximation
predicate excludes a Schauder basis. It does not construct the counterexample
or prove the failure premise.

## Failed Gate

The first failed proof gate is `M0324-C-SPACE`. Pinned mathlib provides the
Schauder-basis API, projections, finite ranges, convergence, and uniform norm
bounds, but no Enflo construction, approximation-property failure, or exact
no-basis existential theorem. The repository supplies only this dossier and
open approximation-property vocabulary; pinned `flt-regular` supplies no
relevant terminal declaration.

Consequently `M0324-C-BANACH`, `M0324-L-SEPARABLE`,
`M0324-L-INFINITE`, and `M0324-L-NO-AP` remain unimplemented. The exact
approximation-property convention and primary-source node map also remain
open, so the existing local predicate cannot close the frozen
`M0324-D-APPROX`-dependent obligations.

Conditional composers, an assumed failure premise, a finite-dimensional or
nonseparable shortcut, and failure of one selected sequence do not prove the
frozen target.

## Revalidated Bodies

| Declaration | Checked contribution | Open boundary |
|---|---|---|
| `schauderBasis_hasCompactApproximationProperty` | Finite-rank partial sums and compact-uniform convergence | Exact source convention remains open |
| `noSchauderBasis_of_not_compactApproximationProperty` | No basis follows from failure of the local predicate | Supplies neither failure nor a witness |
| `noBasis_of_basis_implies_property` | Parametric logical contradiction | Consumes both substantive premises |
| `root_of_witness` | Exact existential packaging | Consumes the full witness and three open properties |

All four declarations elaborated at trust level zero with pinned Lean 4.29.0
and existing pinned package artifacts. Every printed axiom set was exactly
`propext`, `Classical.choice`, and `Quot.sound`. The owned Lean sources contain
no prohibited proof device.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, network request, or `.lake` mutation was
performed. Temporary Lean files, oleans, and logs were confined to a
disposable directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0324` | 0 | Rank 820; `planned`; hard-statement-first-partial-verification lane; theorem incomplete |
| `cd Formalizations/Lean && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3...fab16740` |
| Copy the three modules to `/tmp`, obtain pinned `LEAN_PATH`, then invoke `lake env env LEAN_PATH=<temporary module plus pinned path> lean --trust=0 -t0` in dependency order | 0 | `Statement_exit=0 ObligationTree_exit=0 Proof_exit=0`; log hashes `2bfc8d72...a60f0c`, `c8af60b...b1107`, and `7e2bf773...b8c6b`; exact target and four local bodies elaborated |
| `python3 Stage1_Instances/THM-M-0324/check_obligation_tree.py` | 0 | 15 obligations and 55 typed edges passed; denominator `8bfbe341...f101b`; root open at M3 |
| Token-anchored prohibited-device scan over owned Lean files | 1 (expected no-match) | No `sorry`, `admit`, `sorryAx`, `native_decide`, `implemented_by`, `run_tac`, or axiom/constant/opaque/unsafe/extern/external declaration found |
| Bounded exact-topic search over target instances, pinned mathlib, and pinned `flt-regular` | 0 | Relevant hits were confined to this dossier, Schauder substrate, and open approximation-property vocabulary; no exact terminal proof body found |
| `python3 -m json.tool` on the paired structured packet | 0 | Current-base blocker packet parsed successfully |
| `git diff --check -- Stage1_Instances/THM-M-0324`, plus `git diff --no-index --check /dev/null` on both new packet files | 0 for whitespace checks | No whitespace diagnostics; no-index returns 1 only because each new file differs from `/dev/null` |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test absent because the proof phase is incomplete |

The ordered disposable replay is the narrowest real kernel validation for the
target-local modules because their sibling oleans are intentionally not built
in the shared tree. `lake env` selected the pinned compiler and dependency path
for every elaboration. This is nonrelease kernel evidence for existing partial
bodies, not evidence for root closure.

## Scheduler Boundary

Before this handoff, 19 tracked proof-recheck packets already reported an open
root and the same first failed gate. The authoritative proof item still records
`attempts=0` and no children. Blueprint section 10.2 requires an oversized item
to be split after five unresolved execution ticks. The master must reconcile
which packets count and split or redirect this item rather than schedule
another unchanged whole-root recheck. This worker did not edit the
authoritative DAG, checklist, or item state.

The proof prerequisite is also unfinished: the authoritative projection marks
`S56-M-0324-OBLIGATION_TREE` as provisional `[_]`, while the target-local DAG
still calls it open. This recheck is only permitted provisional later-node
preparation; it cannot be accepted ahead of that dependency.

Resume only with placeholder-free implementations of Enflo's construction,
Banach packaging, separability, infinite dimension, exact source-crosswalked
approximation-property failure, foundation, and provenance packages. The only
valid alternative is an immutable compatible Lean 4 proof-bearing integration
with complete dependency, license, trust, and provenance evidence.

This blocker does not satisfy `S56-M-0324-PROOF`, close the root, promote
scheduler state, or claim audit completion, theorem completion, validation,
release, receipt acceptance, or master acceptance. Because the assigned phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
