# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5535-5540` supplies exactly the title `图灵度的上确界`, the
attribution `众多数学家`, the date `20世纪`, the gloss `图灵度的格结构`, importance "high," and
status `已验证`. All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
definition, theorem locator, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:20515-20540` repeats those fields and explicitly leaves the formal system,
precise definitions and premises, proof history and dependencies, equivalent forms, axioms,
machine state, and artifact links open. Its generic tree language and source status provide no
`H`, `M`, or `R` credit under rev-5.6.

## Literal crosswalk

| Repository element | Required mathematical resolution | Pinned Lean surface | Intake result |
|---|---|---|---|
| `图灵度` | carrier, reducibility, equivalence, representatives, quotient order | `TuringReducible`, `TuringEquivalent`, `TuringDegree` | adjacent definition lead only |
| `上确界` | binary, finite, countable, arbitrary, and uniformity policy | no `Sup`, `SemilatticeSup`, `sSup`, or `iSup` surface in the pinned module | arity and strength unresolved |
| `格结构` | upper semilattice versus lattice, complete lattice, or another structure | only `TuringDegree.instPartialOrder` | gloss cannot justify meets or completeness |
| `众多数学家`, `20世纪` | exact work, edition, theorem/page, definitions, proof, corrections | no source identity in the Lean declarations | provenance unresolved |
| `已验证` | independently accepted source and kernel evidence | no exact target theorem | no H0 or M0 credit |

## Historical source leads

S. C. Kleene and Emil L. Post, "The Upper Semi-Lattice of Degrees of Recursive Unsolvability,"
*Annals of Mathematics* 59(3), May 1954, starting at page 379, DOI `10.2307/1969708`, is the
strongest primary bibliographic lead. Crossref and OpenAlex metadata confirm its identity; OpenAlex
reports it closed with no repository full text. The article text, exact theorem passage, definitions,
assumptions, proof nodes, corrections, and errata were not inspected. The lead therefore supports
H1 discovery only, not H0 or selection of a canonical statement.

Encyclopedia of Mathematics, "Degree of undecidability," immutable revision `46619` dated
2020-06-05, states that the degrees of undecidability under the set and function approaches form
isomorphic upper semilattices and cites Rogers (1967), Shoenfield (1971), and Sacks (1963). This is
an inspected secondary source lead. It clarifies that "upper semilattice" is the relevant family,
but gives no exact join formula or proof and is not an independently reviewed primary crosswalk.

These sources also expose the central mismatch: the catalog's broad "lattice structure" gloss must
not be read as a full lattice, while its singular "supremum" title does not identify the family of
inputs. The statement phase must select a source proposition rather than repair the wording from
memory.

## Pinned formal lead

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.TuringDegree` defines:

| Declaration | Role | Boundary |
|---|---|---|
| `TuringReducible` | `RecursiveIn {g} f` for partial functions | reducibility substrate only |
| `TuringEquivalent` | mutual Turing reducibility | equivalence substrate only |
| `TuringDegree` | antisymmetrization of partial functions by reducibility | quotient carrier only |
| `TuringDegree.instPartialOrder` | partial order on the quotient | order substrate only; no join |

The source file is 132 lines and ends at the partial-order instance. A bounded repo-local and pinned
source search found no other `TuringDegree` use and no target-specific join implementation. This is
intake feasibility evidence, not an exhaustive anchor audit or proof of global absence.

## Source gate

Before statement acceptance, accountable reviewers must preserve a lawful immutable source, select
the exact input family and degree model, map all binders and definitions, fix the join construction
and leastness conclusion, distinguish upper semilattice from lattice and completeness, audit
corrections and errata, and approve source-to-Lean transports. Until then the canonical statement,
formal target, expression hash, accepted proof state, and H0/M0/R0 claims remain null.
