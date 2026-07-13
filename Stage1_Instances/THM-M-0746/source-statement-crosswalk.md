# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5500-5505` supplies exactly the title `创造集` (creative sets),
attribution Emil Post, year 1944, gloss `创造集的性质` (properties of creative sets), importance
`高`, and status `已验证`. All six uncited lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no definition, binders,
hypotheses, conclusion, theorem/page locator, proof boundary, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:20380-20405` repeats the gloss while explicitly leaving precise
definitions and premises, proof route, dependencies, equivalent formulations, axioms, machine
state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted metadata
and resets the target to `L0 / rework_required`.

A separate computer-science row, `Docs/researches/cs_theorems.md:41`, groups creative and simple
sets under the weaker gloss `存在非递归的递归可枚举集` (there exists a nonrecursive c.e. set). It is
neither this target's source statement nor equivalent to creativity.

## Inspected primary source

The matching primary publication is Emil L. Post, *Recursively enumerable sets of positive
integers and their decision problems*, *Bulletin of the American Mathematical Society* 50(5)
(1944), 284-316, DOI `10.1090/S0002-9904-1944-08111-1`. Crossref confirms the bibliographic
metadata. An AMS-scanned, 33-page PDF was inspected with SHA-256
`b2f200e8035696dd82903a2dabc6a179641ae3fe4ad97155508a2777523d0c1d`.

Section 3, `The complete set K; creative sets`, begins on page 295. The definition spans pages
295-296: in Post's basis-indexed formulation, a creative set `C` is c.e. and has a recursive
function which, whenever a c.e. set `alpha` is contained in the complement of `C`, produces an
element of that complement outside `alpha`. Page 296 immediately states existence, with the
complete set `K` as witness. The same page then records several further claims: the class is rich;
every creative set is c.e. but not recursive; its decision problem is recursively unsolvable; and
its complement contains an infinite c.e. subset. Pages 296-297 introduce reduction notions and
state one-one completeness of `K` for c.e. sets.

The preliminary proof boundary was also inspected: section 2, pages 292-294, constructs the
recursively enumerable true-pair set and an effective escape from each c.e. subset of its
complement; pages 295-296 transport that construction through an effective enumeration to `K`.
Post describes the article as an intuitive development and says the claimed complete formal proofs
required further systematization and condensation before publication.

This inspection is strong source-discrimination evidence, but it does not establish `H0`. The
catalog says only "properties" and does not choose the definition, existence theorem, consequence,
or completeness theorem. The OCR was used only for navigation and was checked against page images;
the complete accepted definition chain, notation, premises, proof-node crosswalk, translation to
modern terminology, errata status, and independent review remain open.

## Component crosswalk

| Repository/source-family component | Primary mathematical surface | Pinned Lean surface | Intake result |
|---|---|---|---|
| `创造集` | Post's c.e. set with an effective fresh-complement-element operation | prospective `A : Nat -> Prop`, `REPred A`, an indexed witness function | family identified; no canonical definition frozen |
| "properties" | definition, existence, nonrecursiveness, complement infinitude, or completeness | materially different propositions and binder orders | conclusion absent from catalog |
| positive integers and bases | positive-integer carrier and indices of c.e. sets | `Nat`, `Primcodable`, partial-recursive codes or another numbering | representation and transport open |
| recursively enumerable | Post's generated/c.e. set convention | `REPred` or a checked equivalent range/domain encoding | adjacent API elaborates; source bridge open |
| recursive witness | effective function from a basis/index to a fresh element | `Computable` function plus conditional membership/freshness specification | interface not selected or implemented |
| complete set `K` | Post's witness for existence and later reduction results | a source-mapped code-evaluation or halting predicate | no exact anchor credited |
| reducibility | one-one and many-one reductions in the next section | `OneOneReducible`, `ManyOneReducible` | generic API exists; target and direction open |
| `已验证` | untrusted catalog label | no expression or proof object | no H or M credit |

## Lean and review boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.Halting` supplies `REPred`, `ComputablePred`, c.e. halting predicates, and
c.e./co-c.e. facts. `Mathlib.Computability.Reduce` supplies many-one and one-one reducibility. A
bounded name/phrase search found no computability-theoretic creative-set or productive-set
declaration in repo-local Lean or pinned mathlib; unrelated productive weak sequences were found and
excluded. This is intake discovery, not an exhaustive absence claim.

Before leaving `H5`, accountable reviewers must choose and preserve one exact primary proposition,
map every incorporated definition and assumption, audit correction/errata records, reconcile
Post's positive-integer basis formalism with the chosen modern encoding, and independently approve
the crosswalk. Only then may the statement phase freeze minimal imports, an exact elaborated
expression, checked alternate transports, and the required semantic mutations.
