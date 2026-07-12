# Exact-statement gate: blocked

Item: `S56-M-1310-STATEMENT`  
Theorem: `THM-M-1310`  
Base revision: `08421a58e672ceace1eb99b6ba8b479e5bbb3b05`

## Decision

The exact Lean 4 statement cannot be truthfully frozen from the available authoritative material.
The source record says only "the fundamental equation of general relativity." It neither states a
proposition nor selects among the 1915 gravitational equations, the modern matter-coupled equation,
the 1917 cosmological extension, a vacuum specialization, or a mathematical consequence of one of
these equations. The intake's Einstein and 1916 citations are discovery anchors; no immutable
equation/page transcription or convention audit is present.

This is a logical problem as well as missing detail. A field equation asserted as a physical model
law is not a theorem to prove. A theorem could instead establish a derivation inside fixed axioms,
an existence result, a consequence, or equivalence of two encodings, but the repository wording
does not choose one. Defining `G = Ric - (1/2) R g` and proving by unfolding that
`G + Lambda g = kappa T` is equivalent to its expanded form would only prove a definitional
wrapper. Assuming the field equation in an input structure and projecting it would be circular.
Neither is the exact source claim.

Before a canonical expression can exist, a source audit must also freeze dimension, smoothness,
Lorentzian signature, Riemann/Ricci signs, index placement, units, constants, the matter model, and
whether `Lambda` is present. Changing any of those changes the domain, binders, hypotheses, or
conclusion. Machine state therefore remains `M4`; statement acceptance and theorem completion are
false.

## Lean candidate boundary

The repository-local historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_196.lean` was inspected and elaborated in the
pinned environment. It is labeled `THM-M-1528`, not this target. Its pointwise predicate uses
already-supplied real bilinear forms, scalar curvature, and constants. Its manifold-level
`StatementShape` stores the desired field equation itself as a `Prop` field in abstract input data.
Thus it provides an algebraic shape and an honest infrastructure-gap record, but it neither
constructs Lorentzian curvature nor identifies the exact `THM-M-1310` proposition. It receives no
statement or proof credit here. The candidate SHA-256 is
`71691e1e0ba20cb62b9040d64d48479a3b516312658f0989698ab08c230ec02d`.

## Validation record

Commands ran from the worker-clone root on 2026-07-12. Lean used the existing pinned `.lake`
artifacts; no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1310` | 0 | rank 477, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the target and Einstein-equation terms | 0 | found only underspecified metadata plus the separate historical `THM-M-1528` module; no exact source-frozen proposition |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_196.lean` | 0 | candidate module elaborated; it remains a noncanonical infrastructure/algebra probe |

There is no applicable `lake env lean <canonical statement>.lean` command: the exact proposition
has not been identified. Creating such a file now would manufacture the missing mathematics rather
than validate the assigned statement.

## Retry condition

Retry after an accountable reviewer preserves an immutable primary-source edition, transcribes and
audits the selected equation/page and its surrounding definitions, decides the claim's logical
force, and freezes all conventions. The statement phase can then select minimal pinned imports,
elaborate and serialize the exact expression, check any alternate transports, and execute removed-
hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This artifact records the first failed gate. It does not complete the statement node, accept a
receipt, alter the execution DAG, or claim audit/theorem completion. No
`.stage1-worker-selftest.json` is emitted because the assigned phase is not genuinely self-tested.
