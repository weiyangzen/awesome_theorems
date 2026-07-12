# Exact-statement gate: blocked

Item: `S56-M-1051-STATEMENT`  
Theorem: `THM-M-1051`  
Base revision: `87a5a772b2a40a6b42b5951e3477471611d55d6c`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire source claim is "a Harnack inequality for nondivergence-form equations," while the intake
correctly leaves the elliptic/parabolic choice unresolved. Those are not interchangeable statement
encodings. In particular, the record does not freeze:

- the elliptic ball theorem or the time-directed parabolic-cylinder theorem;
- the displayed operator, sign convention, lower-order terms, or homogeneous/inhomogeneous case;
- dimension restrictions, coefficient symmetry, and the ordered ellipticity constants;
- classical, strong/Sobolev, or viscosity solution semantics;
- the outer domain and the exact inner or earlier/later comparison regions;
- pointwise versus essential supremum/infimum, or the structural constant and all of its
  dependencies.

The only primary bibliographic lead in `source-statement-crosswalk.md` is Krylov and Safonov's
parabolic paper, but the intake has no immutable source artifact, theorem/page pinpoint, exact
wording, or accepted assumption/errata crosswalk. Selecting a familiar textbook formulation would
therefore invent missing mathematics rather than elaborate the assigned exact target. The
dependency remains a provisional worker intake (`[_]`), not a master-accepted statement choice.

Consequently this phase fails at canonical human-claim identity, before minimal imports, expression
serialization, checked alternate transports, or meaningful removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations can be established. No canonical `Statement.lean` is
created, and no statement or theorem completion is claimed.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_244.lean` was inspected and elaborated only as
discovery input. Its `KrylovSafonovData` makes the operator, coefficients, solution predicate,
uniform ellipticity, and even the ABP and growth-lemma packages caller-supplied abstract fields.
Its `StatementShape` also assumes the stochastic representation, ABP package, and growth package
before returning a `LocalHarnackConclusion`; that conclusion combines an essential-supremum
comparison with Holder regularity. This does not crosswalk to an identified source theorem and
cannot select between the unresolved elliptic and parabolic roots. The module itself labels the
declaration a statement-shape candidate and explicitly disclaims a terminal theorem.

The legacy module's four broad direct imports are therefore not evidence of minimal imports for an
exact target. Its successful elaboration proves only that this abstract historical boundary is
type-correct in the pinned environment.

## Required unblock

An accountable source reviewer must pin a stable primary source and record its edition, exact
theorem/page, wording, assumptions, definitions, and errata. The review must choose the elliptic or
parabolic root and freeze the operator, solution notion, coefficient and ellipticity conventions,
geometry, quantifier order, comparison regions, conclusion semantics, constant dependencies, and
all degenerate cases. A later statement worker can then encode that claim, minimize pinned imports,
serialize the elaborated expression and environment, and execute the four required mutation
classes.

## Narrow validation evidence

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). Lean reused the canonical pinned
`.lake` artifacts; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1051` | 0 | rank 244; planned; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_244.lean)` | 0 | historical abstract boundary elaborated; this is not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and all four mutation
classes. The assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is
emitted.
