# Exact-statement validation record

Item: `S56-M-1176-STATEMENT`  
Theorem: `THM-M-1176`  
Base revision: `54743c8a753017ec2ce50ffebf85facec9112b95`

## Gate decision

The exact-statement gate is blocked before Lean target construction. The
repository source says only "a Harnack inequality for nondivergence-form
equations." The intake proposes an elliptic, leading-coefficient-only,
strong-solution formulation, but explicitly labels it provisional. Its only
identified primary article is parabolic, and the secondary monograph lead has
no fixed edition artifact, exact theorem/page transcription, or errata audit.

These omissions are mathematically material. Elliptic and parabolic Harnack
inequalities have different geometries and quantifier order; strong and
viscosity solution formulations require nontrivial bridges; pointwise and
essential extrema depend on representative regularity. The record also does
not freeze the operator convention, lower-order terms, coefficient symmetry,
dimension, exact radii, or all dependencies of the estimate constant.
Choosing any of those values from general mathematical familiarity would
broaden or substitute the received theorem.

Accordingly no canonical `Statement.lean`, declaration, minimal-import claim,
expression digest, transport, or mutation suite is emitted. The structured
blocker is `statement-blocker.json`.

## Inspected Lean boundary

The historical `THM-M-1051` module at
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_244.lean` was elaborated only
as discovery evidence. Its abstract `KrylovSafonovData` accepts the operator,
coefficients, solution predicate, uniform ellipticity, stochastic
representation, ABP package, and growth package from the caller. Its
`StatementShape` therefore does not select a concrete PDE semantics or an
exact source theorem for `THM-M-1176`. Successful elaboration of that module
does not pass this statement gate.

## Commands and results

Commands ran from the worker clone on 2026-07-12 (Asia/Shanghai). The Lean
command reused the canonical pinned `.lake` artifacts. No dependency update,
build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1176` | 0 | rank 376; planned; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_244.lean)` | 0 | the historical abstract boundary elaborated; it is not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Retry requires a pinned,
pinpointed source formulation and reviewed assumption crosswalk. The assigned
phase is not self-tested or complete, so `.stage1-worker-selftest.json` is not
created.
