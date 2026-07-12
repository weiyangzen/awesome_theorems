# Exact-statement gate: blocked

Item: `S56-M-1071-STATEMENT`  
Theorem: `THM-M-1071`  
Base revision: `f738f601d691d8975b71361215fed3140d03a8e4`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the frozen intake. The repository
source record says only "decomposition of a Levy process," and the intake explicitly leaves the
source convention and Lean expression open. Its Applebaum Theorem 2.4.16 and Ito 1942 citations
are discovery leads: no stable source text, exact hypothesis list, definition crosswalk, or errata
record has been inspected. Choosing a standard textbook variant would therefore invent the
missing mathematics rather than elaborate the assigned exact target.

The unresolved choices are mathematically material:

- the state space (`R^d` or a general finite-dimensional space), time domain, filtration,
  adaptedness, stochastic continuity, and cadlag modification;
- construction on the original probability space versus a representation on an extension;
- the truncation function/cutoff and the corresponding sign and normalization of the drift;
- pathwise equality outside one null set, indistinguishability, or per-time almost-sure equality;
- the precise Gaussian covariance object and independence asserted between components;
- the definition of the jump Poisson random measure, its compensation, and the mode in which the
  small-jump integral converges;
- whether uniqueness, the Levy-measure integrability condition, and change-of-truncation behavior
  belong to the theorem conclusion or are premises/adjacent results.

These alternatives cannot be recovered from the theorem name. The prerequisite intake is also
only provisional worker state (`[_]`) rather than a master-accepted receipt. The first substantive
failure is exact human-claim identity, before minimal-import certification, canonical expression
serialization, checked transports, or meaningful mutation tests. No `Statement.lean` is created,
and no statement or theorem completion is claimed.

## Pinned Lean boundary

`StatementProbe.lean` checks the closest independent facilities found in the pinned snapshot:
independent increments, Gaussian processes and multivariate Gaussian measures, ordinary Poisson
distributions on natural numbers, and measure integration. A scoped search of
`Mathlib/Probability` found no Brownian-process, Levy-process, Poisson-random-measure, jump-measure,
compensated stochastic-integral, or Levy-Ito declaration. In particular, `poissonMeasure` is a
one-dimensional Poisson law on `Nat`, not the random measure needed by the decomposition. The
probe is discovery evidence only and does not replace the canonical target.

## Required unblock

An accountable source review must pin and inspect one stable edition, exact theorem/page, wording,
definitions, assumptions, and errata, then freeze all choices above. The statement phase can then
define the missing stochastic-calculus objects without making their desired properties opaque
hypotheses, elaborate the complete proposition, minimize its imports, and run removed-hypothesis,
changed-domain, binder-scope, and boundary-case mutations.

## Narrow validation evidence

Commands ran in the existing canonical pinned environment on 2026-07-12 (Asia/Shanghai). No Lake
update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1071` | 0 | rank 513; planned; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1071/StatementProbe.lean)` | 0 | five substrate interfaces elaborated and printed; not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

Known failures are the canonical target, minimal imports, expression fingerprint, checked
transports, and all required mutation classes. The assigned phase is not self-tested or complete,
so no `.stage1-worker-selftest.json` is emitted.
