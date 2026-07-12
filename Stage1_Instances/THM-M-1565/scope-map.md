# Scope map

## Included claim family

- Hairer's Definition 2.1 data: a locally finite, bounded-below homogeneity set, graded Banach
  model space, and triangular structure-group action.
- A source-exact model with its algebraic identities and analytic bounds under an explicitly fixed
  scaling on finite-dimensional Euclidean space.
- Modelled distributions and a reconstruction map with the source's local test-function estimate,
  continuity, uniqueness regime, and two-model stability bounds.
- If an SPDE application rather than reconstruction is selected, every necessary multiplication,
  composition, abstract integration, Schauder, fixed-point, model construction, renormalisation,
  probability, and convergence premise on the path to that application.
- The exact source conclusion, constants, compact-set enlargements, norms, exponent restrictions,
  approximation topology, and boundary cases of the approved root.

Theorem 3.10 is the leading single-root candidate. In the inspected author revision it asserts a
continuous linear reconstruction map from modelled distributions to scaled Holder/Besov
distributions, estimate (3.3), stability estimates (3.4)-(3.5), and uniqueness for positive
regularity. This is a candidate scope, not an accepted statement.

## Decisions required at statement freeze

The statement phase must pin one immutable source edition and approve one exact root. It must then
freeze:

- whether the target is Theorem 3.10, the locally-subcritical regularity-structure construction of
  Theorem 8.24, the Gaussian-model convergence criterion of Theorem 10.7, or a named application;
- all definitions incorporated by reference, notation conventions, scaling, norms, compact-set
  operations, implicit constants, and quantifier order;
- the complete uniqueness and stability conclusion rather than only the easiest existence clause;
- for an application, the equation, dimension/domain, noise law, mollifier, counterterms, initial
  data, solution concept, lifetime, convergence topology, and universality/independence claim;
- Lean universes, scalar fields, topological and measurable structures, imports, classical-choice
  use, and alternate encodings with checked transports;
- the primary edition hash, theorem/page crosswalk, corrections or errata disposition, and an
  independent scope review.

## Explicit exclusions

- The phrase "a theory of singular SPDEs" treated as though it were a proposition.
- A record or typeclass whose fields assume reconstruction, solvability, convergence, or the final
  SPDE result, followed by a theorem that merely projects the assumed field.
- The polynomial regularity structure, ordinary Taylor expansion, or a classical distribution
  lemma alone as a substitute for the source theorem.
- Only the uniqueness paragraph of Theorem 3.10 if the approved root includes existence,
  continuity, estimates, and stability.
- KPZ, parabolic Anderson, or dynamical Phi^4_3 results unless a precise source theorem is selected;
  neighboring Stage1 targets are not interchangeable with this one.
- Legacy interface or audit declarations for `THM-M-1566`; they concern the distinct
  Gubinelli-Imkeller-Perkowski target and confer no proof credit here.

No obligation registry or Lean expression is frozen during intake. Those require an exact root and
premise-by-premise statement review.

