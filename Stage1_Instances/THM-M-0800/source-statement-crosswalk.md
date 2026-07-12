# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `拉姆齐基数`, attributes the topic to
"many mathematicians", dates it only to the twentieth century, and states `拉姆齐基数的性质`
("properties of Ramsey cardinals"). Stage0 repeats this metadata while leaving the exact definition,
premises, proof, equivalent statements, axioms, and formal artifact open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`.

This is secondary inventory metadata, not a statement-bearing source. It supplies no definition,
partition notation, quantified cardinal, color set, arity convention, conclusion, publication,
edition, theorem number, page, errata, proof, or formal artifact. Neighboring large-cardinal entries
do not disambiguate it.

## Candidate source work

Standard set-theory references and original papers are candidate locators, but no edition or
passage is accepted during intake. The source audit must locate and inspect an immutable primary or
authoritative statement, record edition, definition/theorem and page, all assumptions and notation,
proof boundary and errata, and obtain independent review. A familiar textbook definition cannot
silently turn the source phrase "properties" into a particular theorem.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Ramsey cardinal" | a cardinal satisfying a strong finite-subset partition property | a source-faithful predicate on a represented cardinal/type | family identified; exact convention open |
| finite subsets | subsets of every finite size, together or arity by arity | `Set.powersetCard` or a checked equivalent encoding | pinned API probed; binder shape open |
| coloring | a map from finite subsets to a specified color type | a function with exact domain and codomain | number of colors open |
| homogeneous | constancy on subsets of each relevant arity | restriction/constancy predicate with exact quantifier scope | simultaneous versus separate witnesses open |
| size `kappa` | a homogeneous subset equinumerous with the carrier | `Cardinal.mk` equality or checked equivalent | universe lifts and representation open |
| "properties" | a consequence, characterization, or consistency statement | a concrete proposition with all hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports finite-subset cardinality and cardinal cofinality modules and checks the types of
`Set.powersetCard`, `Cardinal.mk`, `Cardinal.aleph0`, pairwise relations, and set restriction.
These are encoding ingredients only. The probe does not define a Ramsey cardinal, select a
partition convention, or prove any property. The later anchor audit must run its precommitted
declaration search independently.
