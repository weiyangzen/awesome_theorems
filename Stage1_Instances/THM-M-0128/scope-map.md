# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Arithmetic datum | CM field/algebra, CM type, reflex field | Exact representation and universe levels open |
| Reciprocity input | ideles or idele classes and an explicitly normalized Artin map | Geometric/arithmetic Frobenius convention must be frozen |
| Reflex operation | reflex norm from the reflex field into the CM/Shimura datum | Variance and quotient descent open |
| Geometric object | canonical model of the relevant Shimura variety and its CM special point | Construction is assumed input, not claimed as part of this target |
| Root compatibility | Galois action equals reflex-norm-induced action on the special point | Exact equality/action expression not elaborated |
| Lean infrastructure | pinned mathlib CM-field, adeles, schemes, and class groups as possible foundations | Availability is not a bridge to the root theorem |

The target is deliberately the CM-special-point reciprocity compatibility, not
the vague phrase "class field theory for CM fields." It excludes a full general
canonical-model construction and also excludes weakening the conclusion to
mere existence of unrelated structures.

Expected statement work must fix left/right actions, Artin-map normalization,
connected component/level data, reflex-norm codomain, and equality versus orbit
formulation. Degenerate or trivial data may not be silently used to make the
statement vacuous. The historical `CMReciprocityInput` in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_046.lean` is only a discovery
inventory: its `Prop` fields are explicitly placeholders and cannot be credited.

