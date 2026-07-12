# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` give the author, year, and summary
"Banach spaces need not have a basis." They do not define basis, identify a scalar field, state
separability/reflexivity, or supply a theorem locator. They are catalog metadata, not H0 evidence.

## Primary source anchor

- Per Enflo, "A counterexample to the approximation problem in Banach spaces," *Acta
  Mathematica* **130** (1973), 309-317, DOI `10.1007/BF02392270`, Theorem 1.

Crossref confirms author, title, journal, volume, year, and pages. OpenAlex's indexed abstract says
that the paper gives a negative answer to whether every Banach space has the approximation
property, constructs a separable reflexive Banach space failing a property weaker than the bounded
approximation property, identifies the exact result as Theorem 1, and notes that a Banach space with
a Schauder basis has the bounded approximation property. Direct retrieval of the publisher PDF was
blocked by its anti-automation page during intake. Therefore the exact formula of Theorem 1,
notation, real/complex convention, implication chain, and errata have not been inspected and H0 is
not claimed.

## Crosswalk

| Repository phrase | Primary-source role | Required Lean component | Intake status |
|---|---|---|---|
| "Banach space" | Enflo constructs a separable reflexive example | existentially bundled complete normed space and scalar field | family identified; packaging open |
| "basis" | source abstract connects Schauder bases to bounded approximation | `Nonempty (SchauderBasis K X)` and finite-rank partial projections | basis API checked; bridge unproved |
| "need not have" | consequence of the constructed counterexample | existential `X` with negated basis existence | human scope frozen; exact expression open |
| approximation failure | stronger construction underlying the consequence | exact approximation-property predicate and failure certificate | mathlib object model not found at intake |
| separable/reflexive | strength preventing a trivial nonseparability example | Lean structures/predicates plus source assumption map | inclusion in root deferred |

## Source gate still required

Before H0, an independent qualified reviewer must inspect a stable copy of pages 309-317, transcribe
the exact Theorem 1 statement, locate the Schauder-basis implication, map every hypothesis and
conclusion, check corrections/errata, record a content hash, and sign the crosswalk. Before the Lean
statement gate, the selected source-level claim and its consequence must be expressed with fixed
universes, scalar conventions, typeclass packaging, and checked implication/transport witnesses.

The stronger approximation-property result may support the no-basis root; it may not be replaced by
an easier nonseparable-space argument or by assuming an opaque predicate that already states the
counterexample. These open source and statement gates prevent theorem completion.
