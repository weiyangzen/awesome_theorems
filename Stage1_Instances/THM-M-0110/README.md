# THM-M-0110: Kodaira vanishing theorem

This directory is the rev-5.6 `planned` instance. The statement phase has now
elaborated and mutation-tested the intake-selected algebraic
characteristic-zero formulation as
`Stage1Instances.THMM0110.KodairaVanishingTarget`. The worker evidence remains
provisional pending dependency-ordered master acceptance; it is statement
evidence only, not a proof of Kodaira vanishing.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Integral `X` smooth and projective over a characteristic-zero field, ample invertible sheaf `L`, and `H^i(X, omega_X tensor L) = 0` for `i > 0` | Elaborated in `Statement.lean`; proof and master acceptance remain open |
| Object model | Concrete mathlib `Scheme`, structure map, smoothness, and `Scheme.Modules` carriers; semantic predicates for missing native projectivity, line-bundle, ampleness, canonical/dualizing-sheaf, and tensor APIs | Native transports remain downstream obligations |
| Cohomology | Concrete pinned `Sheaf.H` of the underlying abelian sheaf; vanishing encoded by `Subsingleton` | Comparison and trust audit remain open |
| Transport | dual form `H^i(X,L^{-1}) = 0` for `i < dim X` | Requires checked Serre-duality and dimension/index transports |
| Historical form | compact Kahler/positive line-bundle analytic theorem | Outside canonical credit unless an explicit comparison bridge is checked |
| Exclusions | positive characteristic, singular/nonprojective varieties, degree zero, nef-only bundles | No broadened generalization or special case may substitute for the root |
| Trust | Lean 4 kernel and pinned mathlib; imports and environment fingerprint recorded | Transitive trust/proof-body audit and independent replay remain open |

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The statement node freezes the scheme/variety model, universe constraints,
ordered hypotheses, positive-degree boundary, and concrete cohomology functor.
It explicitly records the native API boundaries rather than pretending those
objects have already been integrated. The anchor audit must re-audit the
legacy `S1_M_034.lean` file without inheriting proof credit.

The anchor phase has now frozen and self-tested a bounded inventory at pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. It found
concrete `Sheaf.H`, stronger-premise zero-sheaf/injective-Ext lemmas, and Proj
properness as substrate, but no exact mathlib or external Kodaira terminal
theorem. The legacy file is a different statement shape, and public Kodaira
name matches are unrelated or placeholder-bearing. More importantly, the
frozen target's semantic proposition fields do not constrain its actual
`K`, `L`, or `KTensorL` objects. The object model therefore needs repair and
checked transports before an ordinary Kodaira theorem could be an exact
candidate. See `anchor-audit.md` and `anchor-audit.json`.

## Intake verdict

Lifecycle remains `planned`; the provisional root vector remains
`[H1, M3, R3]`. The statement and bounded anchor inventory are self-tested
locally, while dependency-ordered master acceptance remains pending. The full
source audit, object-model repair, obligation architecture, proof, validation,
readability, and release gates remain open. The theorem is not complete and no
kernel closure of its root is claimed.
