# Scope map

## Included target

The intended root is a relative cone theorem for a projective Q-factorial klt pair `(X, Delta) -> S`: decomposition of the closed effective cone into the log-canonical nonnegative part and negative extremal rays, rational-curve generators, local finiteness in negative regions, and contractions of negative rays.

## Domains and binders to freeze

The statement phase must choose explicitly: base field and characteristic; whether `S` is a point or a scheme; finite type, normality and projectivity/properness assumptions; an effective Q-boundary `Delta`; Q-factoriality; the precise klt predicate; `N_1(X/S)_R`; numerical equivalence; the closed effective cone; the pairing with `K_X + Delta`; ray extremality; and the contraction morphism's universal property. It must also decide whether the rational-curve length bound is root content.

## Degenerate and boundary cases

Empty negative-ray families, zero-dimensional varieties, a trivial relative cone, numerically trivial `K_X + Delta`, non-Q-factorial varieties, non-klt pairs, nonprojective morphisms, and positive-characteristic inputs must be either covered with correct semantics or explicitly excluded. No vacuous opaque `Prop` field may stand in for these objects.

## Excluded claims

The intake does not claim unconditional finite generation or rational polyhedrality of the full cone. It also excludes the flip theorem, termination of the minimal model program, base-point-free theorem, and rationality theorem except where a precisely cited prerequisite is later required. Absolute smooth/projective formulations are possible specializations, not silently interchangeable roots.

## Lean boundary

Mathlib's scheme, proper morphism, noetherian, convex cone, and Picard-group APIs are only substrate candidates. No exact Lean declaration is accepted at intake. The legacy `MoriConeStatementData` encodes core mathematics as arbitrary `Prop` fields and is therefore not the canonical expression.
