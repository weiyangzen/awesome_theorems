# Statement-phase blocker

Item: `S56-M-1219-STATEMENT`  
Theorem: `THM-M-1219`  
Base revision: `bf8f1a403fb8c22395ec64f92f93fed974f23c83`

## Verdict

The exact-statement gate is blocked before a canonical Lean declaration can be frozen. The complete
repository claim is "global well-posedness of the mass-critical NLS," attributed to Benjamin
Dodson with the year 2012. No repository artifact identifies a primary publication, theorem number
or page, or the definitions imported by that theorem. The metadata therefore does not determine a
unique proposition.

In particular, it leaves open the spatial dimension and domain, focusing or defocusing sign,
normalization and critical power, initial-data space, solution and uniqueness class, maximal
lifespan and continuous-dependence clauses, and whether scattering or a global spacetime bound is
part of the conclusion. A focusing formulation would additionally require an exact mass threshold,
ground-state normalization, and treatment of threshold equality. Dodson's name labels several
dimension- and sign-dependent mass-critical NLS results; selecting one from memory would substitute
an unverified theorem for the repository target.

Consequently there is no truthful canonical expression fingerprint, minimal-import claim, checked
transport to an alternate encoding, or removed-hypothesis/domain/binder-scope/boundary mutation
suite. The intake classification `[H4, M4, R4]` remains unchanged, and this phase claims neither
statement completion nor any proof credit.

## Lean boundary

Pinned mathlib contains general analysis infrastructure but the scoped search found no declaration
whose name or documentation mentions nonlinear Schrodinger equations, mass-critical NLS, or NLS.
`StatementInfrastructureProbe.lean` uses the single direct import
`Mathlib.Analysis.InnerProductSpace.Laplacian` and checks `Laplacian.laplacian` and `Complex.I` in the
pinned environment. This establishes only that two formula-level ingredients elaborate. It does
not encode an evolution equation, solution notion, global well-posedness, or the unidentified
source claim; the import is not asserted minimal for a canonical target that does not yet exist.

## Validation record

Commands ran in this worker clone using the existing canonical `.lake` symlink. No dependency
update, fetch, clone, or other `.lake` mutation was performed.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The toolchain and Lake-manifest SHA-256 values are
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` respectively.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1219` | 0 | rank 410; planned; L0/rework-required; theorem incomplete |
| repository search for `THM-M-1219`, Dodson, and mass-critical NLS | 0 | only underspecified metadata and the intake dossier identify this target; no source-frozen proposition or target Lean artifact |
| pinned-mathlib search for nonlinear Schrodinger, mass-critical, Schrodinger, and NLS terms | 0 | no matching Lean source |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1219/StatementInfrastructureProbe.lean` | 0 | printed types of `Laplacian.laplacian` and `Complex.I`; substrate only |
| scoped prohibited-token scan of `StatementInfrastructureProbe.lean` | 0 | clean |
| `git diff --check -- Stage1_Instances/THM-M-1219` | 0 | no output |

## Retry condition

Retry after an accountable source review selects an immutable primary-source edition and exact
theorem/page and provides enough surrounding definitions to crosswalk every binder, hypothesis,
restriction, and conclusion. The statement phase can then transcribe that result exactly, minimize
pinned imports, serialize its elaborated expression and environment, check alternate transports,
and execute all required mutation classes.

This artifact does not complete the statement node, accept a receipt, modify the execution DAG, or
claim audit/theorem completion. No `.stage1-worker-selftest.json` is emitted because the assigned
deliverable is not genuinely self-tested.
