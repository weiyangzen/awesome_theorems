# Exact-statement gate: blocked

Item: `S56-M-1169-STATEMENT`  
Base revision: `f4aeafc83b9d0ab5a752188bd83124ddf69f5435`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is `解在边界的正则性` ("regularity of solutions at the boundary"),
under the label "boundary estimates". It does not determine any of the data needed to identify one
proposition:

- the differential operator or whether the equation is elliptic, parabolic, or another class;
- the weak, strong, or classical solution concept and the forcing data;
- the ambient dimension, domain class, boundary smoothness, and boundary condition;
- the source and target regularity spaces, derivative order, exponents, and endpoint policy;
- the qualitative or quantitative conclusion, including the norm, constant, and its dependencies;
- the compatibility, coefficient, locality, uniqueness, and degenerate-case assumptions.

These choices produce inequivalent theorems. Selecting a trace theorem, Schauder estimate,
Calderon-Zygmund estimate, harmonic-function result, or compact-support zero-trace special case
would therefore invent missing mathematics rather than elaborate the exact target. The Stage0
record confirms that precise definitions, hypotheses, proof, and machine artifacts are all
`待补充` (to be supplied). The metadata value `已验证` is not a source or kernel receipt.

The intake dependency records the same ambiguity and assigns `[H4, M4, R4]`; it does not select a
theorem family. Consequently this phase fails at the canonical human-claim identity gate, before
minimal imports, an elaborated expression fingerprint, checked transports, or meaningful
hypothesis/domain/binder/boundary mutations can be established.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_146.lean` was checked only as discovery input. Its
`StatementShape` universally quantifies over an arbitrary `BoundaryRegularityProblem`. That record
supplies the solution space, trace, admissibility predicate, desired regularity predicate, three
unconstrained real-valued "norms", and a distribution-valued residual. The proposition then asks
for a `BoundaryRegularityEstimate` for every such record. It neither encodes a concrete PDE nor
crosswalks to an identified primary-source theorem. Its own caveat calls it an abstract statement
boundary, and the intake explicitly excludes it from statement credit.

The legacy file elaborates with eight broad mathlib imports in the existing pinned environment.
That check shows only that the old abstract module is syntactically and type-correct. It cannot show
that those imports are minimal for an exact target, because no exact target exists, and it supplies
no rev-5.6 statement acceptance evidence.

## Required unblock

An accountable source reviewer must identify a stable primary source by edition, theorem/page, and
exact wording, then freeze the operator, solution notion, domain and boundary assumptions,
coefficient and data hypotheses, boundary condition, regularity spaces, quantitative conclusion,
constant dependencies, and boundary/endpoint cases. A later statement worker can then encode that
claim without substitution, minimize its pinned imports, print and hash the elaborated expression,
and run the required structural mutations.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. No `lake update`, build, dependency fetch,
or mutation of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1169` | exit 0; rank 146, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_146.lean)` | exit 0; no output; legacy abstract boundary only |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transport, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted. No theorem completion or downstream-node credit is claimed.
