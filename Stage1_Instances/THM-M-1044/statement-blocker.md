# Exact-statement gate: blocked

Item: `S56-M-1044-STATEMENT`  
Base revision: `003528e41c522d26270c91f61e92d738221c03c8`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. Its
entire mathematical claim is `测度变换与鞅` ("change of measure and martingales") under the name
Girsanov theorem. This identifies a theorem family, but it does not determine one proposition. In
particular, the record does not select:

- a Brownian, continuous local-martingale, or semimartingale formulation;
- the time domain and finite or infinite horizon;
- the original and changed measures or the direction and strength of absolute continuity;
- a terminal density, density process, or stochastic-exponential construction;
- the filtration conditions, process measurability, and integrability assumptions;
- the sign convention and exact drift or covariation correction; or
- a local-martingale, true-martingale, Brownian-motion, or characteristics conclusion.

These choices yield materially different theorems. Novikov and Kazamaki conditions also have their
own manifest targets, `THM-M-1046` and `THM-M-1047`, so silently incorporating either criterion
would conflate separate repository claims. The Stage0 record confirms that the precise definitions,
hypotheses, proof route, equivalent forms, and machine artifact are all still `待补充` (to be
supplied). Its metadata label `已验证` is not an exact source statement or a kernel receipt.

The accepted intake deliberately leaves `canonical_statement`, the Lean module/expression, and the
expression and environment fingerprints null. It assigns machine state `M4` and records the same
source ambiguity. Consequently this phase fails at canonical human-claim identity, before minimal
imports, fixed binders, checked alternate encodings, or meaningful removed-hypothesis, changed-
domain, changed-scope, and boundary mutations can be established.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_237.lean` was inspected and elaborated only as
legacy discovery input. Its `GirsanovData` packages the missing stochastic-exponential relation,
stochastic-integral bridge, drift compensation, and integrability condition as unconstrained
`Prop` fields. Its `StatementShape` then assumes those fields and asks for a martingale and a local
Brownian boundary. The module explicitly describes itself as a conservative statement boundary
and says that it does not prove Girsanov's theorem.

That abstract implication does not crosswalk to an identified primary-source proposition and
cannot choose among the source variants above. It also uses six broad mathlib imports, so its
successful elaboration cannot establish minimal imports for an exact target that is not yet known.
No statement, proof, or downstream credit is assigned to it.

## Required unblock

An accountable source reviewer must select an immutable primary-source edition and exact
theorem/page, then freeze every binder and assumption: the probability spaces and measure-change
orientation, time horizon, filtration, process class, density construction, integrability
condition, correction convention, and exact conclusion. A later statement worker can then encode
that claim without substitution, minimize its pinned imports, serialize and hash the elaborated
expression and environment, add checked transports, and run all four mutation classes required by
section 5.1 of the rev-5.6 standard.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing canonical `.lake` artifacts
were used read-only; no dependency update, build, clone, or fetch was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1044` | exit 0; rank 237, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_237.lean)` | exit 0; printed the module's `#check` declarations; legacy abstract boundary only |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_237.lean` | exit 0; `651c8acc...b1d2`, `321626c8...2d81`, and `67117b1c...9c48` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and semantic mutation
tests. The assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is
emitted. No theorem completion or downstream-node credit is claimed.
