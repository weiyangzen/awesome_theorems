# Exact-statement gate: blocked

Item: `S56-M-0997-STATEMENT`  
Theorem: `THM-M-0997`  
Base revision: `25fbac874308ef58f14fc38921bfd8d904f258f7`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is "isoperimetric inequality for sets on the sphere," attributed to
Paul Levy in 1951. It contains no edition, theorem/page, quoted statement, or immutable primary
source. This does not decide among inequivalent perimeter, Minkowski-content, open-neighbourhood,
and closed-neighbourhood formulations, or fix their regularity and boundary conventions.

The accepted intake chooses the closed geodesic-neighbourhood formulation only provisionally and
explicitly requires the statement phase to confirm it against a primary source. That requirement
cannot be discharged from the repository-held material. In particular, the following components
remain undetermined:

- the sphere dimension convention and allowed dimensions;
- unit radius versus a scaled round sphere;
- normalized Riemannian surface measure and its completion convention;
- Borel, Jordan, or another admissible class of sets;
- open or closed intrinsic geodesic neighbourhoods and the radius range;
- the parameterization and endpoint conventions for the equal-measure cap;
- whether the conclusion is a neighbourhood inequality or a perimeter statement.

Choosing these data from a modern secondary formulation would invent the missing source identity.
It would also violate the intake dependency rather than elaborate its exact target. Consequently
there is no honest canonical expression, normalized expression hash, checked alternate transport,
or meaningful removed-hypothesis/domain/binder/boundary mutation suite. The statement remains
`M3`: a provisional claim and checked object-model infrastructure exist, but exact statement
identity is blocked.

## Pinned Lean boundary

`StatementInfrastructure.lean` checks only the smallest pinned object model found for the intended
domain. It imports the sphere manifold instance and Hausdorff measure, defines a unit-sphere subtype
and its intrinsic Hausdorff measure, and checks the ambient `Metric.closedBall` interface. It does
not define the theorem target, an intrinsic geodesic distance, normalized Riemannian surface
measure, or a proxy predicate.

The historical `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_277.lean` is not an acceptable
statement substitute. Its own documentation calls `StatementShape` a proposition boundary. More
importantly, it states codimension-one Hausdorff measure of the relative frontier is minimized,
whereas the intake root is minimization of every closed geodesic-neighbourhood measure. It also
uses the sphere subtype's inherited chordal metric and unnormalized Hausdorff measure, includes
`n = 0`, and records that no normalized Riemannian surface-measure or intrinsic-geodesic bridge has
been proved. Reusing it would broaden or substitute the theorem and would grant legacy evidence
that rev-5.6 expressly rejects.

## Environment fingerprint

- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Narrow validation evidence

Commands were run from this worker clone using the existing canonical pinned `.lake` artifacts.
No update, build, clone, fetch, or mutation of `.lake` was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0997` | 0 | rank 277, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0997/StatementInfrastructure.lean)` | 0 | pinned sphere/Hausdorff object-model probe elaborated and printed three checked declarations |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_277.lean)` | 0 | historical perimeter-surrogate boundary elaborated; no exact-statement credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 at the commit above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision equals the pinned revision above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | toolchain and manifest hashes equal the fingerprints above |
| `git diff --check -- Stage1_Instances/THM-M-0997` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must provide an immutable primary edition and exact theorem/page
for the intended Levy result, including its assumptions and conventions. The statement phase can
then select the matching Lean object model, add missing geodesic/normalized-measure definitions if
needed, serialize the elaborated target, and run the required structural mutations and checked
transports.

Until then, statement acceptance and theorem completion are false. Because the assigned phase is
not self-tested to completion, no `.stage1-worker-selftest.json` is emitted.
