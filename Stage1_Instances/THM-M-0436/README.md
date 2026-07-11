# THM-M-0436 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Shimura lifting. The metadata phrase
"lifting of modular forms" is not an exact theorem statement, and the historical `S1_M_085.lean`
module is discovery input only.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | Shimura's correspondence from suitable half-integral-weight cusp forms to integral-weight modular forms | Exact 1973 theorem number, parameters, and conclusion must be transcribed from an immutable primary-source copy |
| Source object | weight, level, character, multiplier/slash law, cuspidality, Fourier coefficients | Kohnen plus-space terminology is later and is not silently imposed on the 1973 root |
| Target object | integral-weight cusp/modular form at the source-specified level and character | Exact target weight and level formula remain unfrozen |
| Compatibility | Fourier-coefficient/Dirichlet-series identity and resulting Hecke-eigenvalue correspondence | The exact logical conclusion and admissible indices remain unfrozen |
| Lean boundary | candidate `StatementShape` and ordinary `CuspForm` wrappers in `S1_M_085.lean` | Proposition fields are not a formalization of the analytic definitions and receive no proof credit |
| Foundations | Lean kernel, pinned mathlib, complex analysis and modular-form infrastructure | Environment, axioms, TCB, and computation profiles remain open |

The statement phase must resolve the source ambiguity before selecting ordered binders. In
particular, it must not substitute the later Kohnen plus-space isomorphism or prove a vacuous
existence statement using unconstrained proposition fields.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The dependent statement task must freeze source parameters, elaborate the exact target, add checked
transports, and mutation-test hypotheses and boundary cases. No later node is credited here.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed theorem gate is
source identification/exact-statement fidelity: repository metadata supplies only a short label,
while the likely primary paper contains a family of technical results. The theorem is not complete.

## Validation

The exact commands and results in `validation.md` establish target membership, standard consistency,
JSON syntax, owned-file references, and absence of forbidden proof placeholders. They do not validate
the mathematical theorem or the legacy Lean statement.
