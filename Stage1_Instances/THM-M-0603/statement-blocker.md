# Statement-phase blocker

Item: `S56-M-0603-STATEMENT`  
Base revision: `a755bddf3ef1127293a161eabda268d04a9877b3`

## Verdict

The exact Lean 4 target cannot yet be frozen truthfully. The intake dependency deliberately records
the received claim only as "classification of manifolds by bordism" and leaves the following
inequivalent readings unresolved:

- unoriented bordism classified by Stiefel-Whitney numbers;
- oriented bordism classified using Stiefel-Whitney and Pontryagin numbers; or
- a Pontryagin-Thom identification with stable homotopy of a Thom object.

These readings require different orientation data, coefficient rings, characteristic classes,
degree and partition conventions, and conclusions. The intake also lacks an immutable primary-source
copy, an exact theorem/page locator, and a reviewed premise map. Choosing a familiar version would
therefore substitute an inferred theorem for the repository claim and fail the rev-5.6 exact
statement gate.

The pinned `Mathlib.Geometry.Manifold.Bordism` module does not resolve the ambiguity. Its own module
documentation describes the file as the beginnings of unoriented bordism theory and lists bordisms,
the bordism relation, bordism groups, and the bordism ring as future work. The checked probe in
`StatementInfrastructureProbe.lean` only confirms that `SingularManifold` and its elementary
`map`, `comap`, `empty`, `toPUnit`, `prod`, and `sum` operations elaborate. It is not a classification
statement and receives no theorem credit.

Consequently this phase is blocked at `exact_source_statement`. No canonical declaration,
expression fingerprint, minimal-import claim, checked transport, mutation-test acceptance, proof
credit, audit completion, or theorem completion is asserted. No `.stage1-worker-selftest.json` is
emitted.

## Required unblock

An accountable source reviewer must pin and transcribe the exact primary theorem, including its
theorem/page locator and all category, orientation, dimension, boundary, coefficient, invariant,
and equality-versus-null-bordism choices. Concrete pinned Lean interfaces for the selected bordism
and characteristic-invariant objects must then be available. A later statement worker can encode
that proposition without weakening it, minimize imports, serialize its elaborated expression,
check any alternate transports, and perform the required hypothesis/domain/scope/boundary
mutations.

## Narrow validation evidence

Commands were run from the worker clone on 2026-07-12. No update, fetch, build, or mutation of
`.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0603` | exit 0; rank 641, `planned`, `theorem_complete: false` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0603/StatementInfrastructureProbe.lean)` | exit 0; printed the seven checked pinned declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-0603/statement-blocker.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0603` | exit 0 |

Known failure: there is no uniquely selected human proposition to elaborate, and the pinned formal
surface lacks even the bordism relation and groups required by every candidate classification.
