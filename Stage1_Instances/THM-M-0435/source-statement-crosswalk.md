# Source-statement crosswalk

## Candidate primary source

Goro Shimura, "Construction of class fields and zeta functions of algebraic curves," *Annals of
Mathematics* (2) **85** (1967), 58-159, DOI `10.2307/1970526`, is a primary candidate for the
classical construction and canonical models of curves arising from quaternion algebras. The exact
theorem number, pages, definitions, hypotheses, and relevant errata have not yet been inspected from
a stable copy. This bibliographic anchor is therefore discovery evidence only, not `H0`.

## Crosswalk

| Repository phrase | Source information still required | Lean-side consequence | Disposition |
|---|---|---|---|
| "Shimura curves" | exact construction and asserted property | root conclusion is unknown | blocking |
| "attached to quaternion algebras" | center field, algebra, ramified places, order and level | arithmetic binders and typeclasses cannot be frozen | blocking |
| "modular curves" | whether this means a moduli interpretation or an arithmetic quotient | quotient/moduli equivalence may be part of the theorem | blocking |
| no boundary cases | compactness, torsion, connected components and bad primes | hypotheses and degeneracies are unknown | blocking |

## Legacy Lean discovery boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_084.lean` checks useful mathlib substrate for
`QuaternionAlgebra`, number fields, schemes, and morphism predicates. Its header says the arithmetic
moduli problem, orders, level structures, and representability theorem remain parameters. Thus it
does not identify or prove an exact source statement and receives no rev-5.6 statement/proof credit.

Before `H0`, reviewers must record a stable source identity, theorem/page span, every invoked
definition and assumption, errata search, node-by-node crosswalk, and independent approval.

## Statement-phase disposition

No row above determines one proposition. In particular, the repository wording does not map the
premises needed for a source-faithful Lean declaration: it omits the base field, quaternion
algebra and its split/ramified places, order or compact-open level, connected-component and
torsion conventions, and the analytic, algebraic, coarse-moduli, or stack model. It also leaves the
conclusion open between construction, algebraicity or a canonical model, representability,
smoothness/properness, and uniformization.

The target-owned `Statement.lean` therefore checks only adjacent pinned vocabulary. Its imports,
object probes, and successful elaboration do not select a theorem and receive no exact-statement or
proof credit. A parameterized predicate, assumed representing object, arbitrary smooth proper
curve, classical modular-curve special case, or legacy statement shape is not source-admitted.

Retry requires an immutable primary-source edition with a named theorem/page and definition chain,
every premise and ordered quantifier, the exact conclusion and boundary cases, errata disposition,
and independent source-fidelity approval. Until that record exists, the exact premise/boundary
mapping required by rev-5.6 remains visibly open and `S02-EXACT-TARGET` fails closed.
