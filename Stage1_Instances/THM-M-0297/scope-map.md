# Scope map

## Preserved theorem family

The intake preserves only the family named by the catalog: weak endpoint estimates for an operator
imply a strong estimate at intermediate exponents. A later statement phase may select an exact root
only from an immutable, independently reviewed source. Candidate components, none yet credited as
the theorem, include:

- measure spaces `(X, mu)` and `(Y, nu)`, their finiteness or sigma-finiteness assumptions, and
  scalar or vector-valued measurable functions;
- endpoint exponent pairs `(p0, q0)` and `(p1, q1)`, an interpolation parameter `theta`, and the
  exact relations defining the intermediate `p` and `q`;
- a linear, sublinear, quasilinear, or midpoint-subadditive operator, including its domain and its
  behavior under scalar multiplication and addition;
- endpoint weak-type distribution estimates, with threshold strictness, zero conventions, and
  endpoint constants;
- a strong intermediate `Lp -> Lq` estimate and the source-specific dependence of its constant;
  and
- an extension from simple functions or an intersection of endpoint spaces to completed `Lp`
  spaces, including representative-independence and uniqueness.

## Decisions required at statement freeze

1. Preserve and hash a lawful complete source edition, select a precisely delimited theorem, map
   all incorporated definitions and its proof boundary, audit corrections or errata, and obtain
   independent source approval.
2. Fix both measure spaces, sigma-algebras, measures, scalar and codomain types, function
   representatives, and every measurability assumption.
3. Fix the operator class and domain. In particular, distinguish a genuinely sublinear map from
   a quasilinear map with a source-specific loss constant, and state whether values are functions,
   equivalence classes, or extended nonnegative magnitudes.
4. Fix the definition of weak type: the superlevel set (`>` or `>=`), threshold domain, powers,
   zero and infinity conventions, and whether the inequality is expressed through distribution
   functions or a Lorentz/weak-`Lp` quasi-norm.
5. Fix the endpoint ordering and all restrictions on `p0`, `p1`, `q0`, `q1`, including equality,
   infinity, and the relation between source and target exponents.
6. Fix `theta`, the formulas for the intermediate exponents, and whether endpoints `theta = 0` or
   `theta = 1` are excluded or stated separately.
7. Fix the conclusion: membership, existence of a bounded extension, an `eLpNorm` inequality, an
   operator-norm inequality, or a quantitative formula with exact constant dependencies.
8. Fix the density, truncation, convergence-in-measure, almost-everywhere, and representative
   arguments required to pass from the initial operator domain to completed `Lp` spaces.
9. Freeze all ordered binders, universes, typeclass assumptions, logical principles, alternate
   encodings, checked transports, and boundary cases before inspecting proof closure.

## Degenerate and boundary cases

Source review must explicitly dispose of zero or infinite measures; null functions; the zero
operator; zero or infinite endpoint constants; coincident endpoint pairs; `p = 0`; exponents below
one where `Lp` is only quasi-normed; endpoint exponent infinity; a zero interpolation denominator;
`theta` at or outside `[0, 1]`; nonmeasurable operator outputs; functions belonging to only one
endpoint space; simple-function density failure; non-sigma-finite spaces; and changes from strict
to non-strict superlevel sets in the presence of atoms.

Endpoint weak-type results, restricted weak type, Lorentz-space interpolation, and quasi-Banach
extensions can be valid theorems but cannot be folded into one generic root without exact source
selection and checked transports.

## Neighbor and substitution exclusions

- `THM-M-0296` Riesz-Thorin interpolation uses strong endpoint bounds and a linear/complex-analytic
  route; it does not replace weak-to-strong Marcinkiewicz interpolation.
- `THM-M-0374` is a generic interpolation-family catalog entry and explicitly treats this target as
  separately owned; it supplies no statement or proof credit.
- `THM-M-0289` Hardy-Littlewood maximal and `THM-M-0299` singular-integral boundedness may consume
  weak-type interpolation, but a particular application is not the general interpolation theorem.
- A theorem that assumes the desired strong intermediate bound, or a structure storing endpoint
  and intermediate bounds as fields, is circular data rather than a proof.
- Chebyshev-Markov estimates derive a distribution bound from an existing `Lp` bound; alone they do
  not perform operator interpolation in the reverse direction.
- `MemLp`, `eLpNorm`, `Lp`, measure, superlevel-set, and simple-function APIs are substrate only.
- The catalog's `verified` label, the bounded name search, and the intake probe confer no source or
  machine-proof credit.

## Formal boundary

Pinned mathlib exposes `MemLp`, `eLpNorm`, `Lp`, almost-everywhere strong measurability, and
Chebyshev-Markov inequalities. The probe authenticates only these adjacent interfaces. It neither
defines the source-selected weak-type operator predicate nor states or proves an interpolation
theorem. No canonical Lean target, expression fingerprint, checked alternate encoding, mutation
suite, proof body, or obligation registry is claimed at intake.
