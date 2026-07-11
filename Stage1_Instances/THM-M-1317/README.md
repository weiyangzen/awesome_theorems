# THM-M-1317 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Witten's spinorial proof of the positive
energy theorem. The Stage0 label is a proof-method label, not by itself a proposition. This intake
therefore freezes the intended root as the positive energy theorem for an asymptotically flat spin
initial data set satisfying the dominant energy condition; it does not claim that the proof method
is itself a separate theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | ADM energy-momentum of an asymptotically flat spin initial data set obeys `E >= |P|` | Precise regularity, ends, decay, boundary, and dimension conventions must be fixed in the statement phase |
| Time-symmetric specialization | Complete asymptotically flat spin Riemannian manifold with nonnegative scalar curvature has nonnegative ADM mass | A consequence/specialization, not a substitute for the spacetime root |
| Rigidity | Equality implies the appropriate flat/Minkowski initial data conclusion | Included in the source theorem family; exact hypotheses and conclusion remain to be frozen |
| Analytic bridge | Existence and asymptotics of a Witten spinor solving the Dirac equation | Architecture only; no Fredholm, regularity, or decay result is credited |
| Positivity identity | Integrated Lichnerowicz/Weitzenbock identity, dominant-energy bulk term, ADM boundary term | Architecture only; conventions and constants remain open |
| Foundations | Lean 4 kernel plus versioned classical/choice/quotient and analytic dependency policy | Exact profile and environment fingerprint remain open |

Excluded are non-spin extensions, asymptotically hyperbolic variants, manifolds with inner
boundaries, and merely physical prose about energy. They may later be checked transports or child
theorems, but cannot silently broaden the denominator.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. A primary source has been
identified, but its assumptions and rigidity clauses have not received independent pinpoint audit.
No exact Lean declaration has been identified or elaborated. The first failed theorem gate is the
exact-statement gate, and the theorem is not complete.

## Open task DAG

`exact source statement -> Lean definitions and target -> anchor audit -> frozen obligation tree ->
proof/integration -> kernel and trust validation -> release review`.

The statement node must resolve the dimension and regularity conventions before downstream work.
The source crosswalk records the currently known ambiguity rather than inventing a formal target.

