# Statement-phase blocker

Item: `S56-M-1214-STATEMENT`  
Theorem: `THM-M-1214`  
Base revision: `b0f46ce08e1b6a797d65cf735b0ccf96bd57ddcb`

## Verdict

The exact-statement gate is blocked before a canonical Lean declaration can be frozen. The
repository phrase is only "NLS critical regularity." The intake identifies Cazenave and Weissler,
"The Cauchy problem for the critical nonlinear Schrodinger equation in H^s," *Nonlinear Analysis*
14 (1990), 807-836, DOI `10.1016/0362-546X(90)90023-A`, but no available repository artifact gives
an exact theorem number/page, its imported definitions, equation convention, dimension and exponent
range, homogeneous or inhomogeneous critical space, solution class, endpoint restrictions, or
precise conclusions. The bibliographic API check confirms the paper metadata but supplies no full
text or theorem statement.

The paper contains multiple results and the label can denote mutually non-equivalent claims:
conditional uniqueness versus uniqueness in the full solution class, local existence versus a
maximal-lifespan theorem, continuous dependence, small-data global existence, or scattering.
Selecting or combining any of these without the primary text would substitute or broaden the
unknown root. Therefore there is no truthful expression fingerprint, checked alternate encoding,
or removed-hypothesis/domain/binder-scope/boundary mutation suite.

## Lean boundary

`StatementCandidateProbe.lean` checks the historical discovery module in the pinned Lean
environment. That module elaborates useful formula-level predicates for classical and mild NLS and
a Fourier-weighted Sobolev membership predicate, but its `CriticalNLSProblem` stores the NLS
equation, trace, solution class, admissibility, scaling relation, and contraction hypotheses as
abstract fields. It is not an exact source theorem and receives no statement or proof credit. Its
five direct imports are also not evidence of a minimal import for an as-yet unidentified target.

## Validation record

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` using the existing pinned
Lake environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1214` | 0 | rank 153; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1214/StatementCandidateProbe.lean` | 0 | `Distribution`, `MemLp`, `MemLp.toLp`, and `Laplacian.laplacian` elaborated; analysis substrates only |
| `git diff --check -- Stage1_Instances/THM-M-1214` | 0 | no output |

## Retry condition

Retry after an authoritative stable copy supplies a pinpoint theorem and enough surrounding
definitions to crosswalk every binder, hypothesis, restriction, and conclusion. The statement
phase can then encode exactly that result, minimize its imports, serialize its elaborated
expression and environment, check any alternate transports, and run all four required mutation
classes.

This artifact does not complete the statement node, accept a receipt, modify the execution DAG, or
claim audit/theorem completion. No `.stage1-worker-selftest.json` is emitted because the assigned
deliverable is not genuinely self-tested.
