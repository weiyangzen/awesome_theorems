# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:575-580` supplies exactly the title `扎森豪斯定理`, Hans
Zassenhaus attribution, year 1937, gloss `关于群扩张的分类` ("about the classification of group
extensions"), importance medium, and formalization status `已验证`. All six uncited fields originate
in repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2244-2269` repeats the gloss while explicitly leaving the formal system,
definitions and premises, proof route, dependencies, alternate forms, axioms, machine status, and
artifact links open. The rev-5.6 manifest keeps `已验证` only as untrusted metadata and resets the
target to uniform `L0 / rework_required`.

Neither record states a proposition. There is no source edition, theorem/page, classified-object
definition, equivalence relation, fixed action or endpoint data, invariant, ordered binder list,
hypothesis list, conclusion, proof boundary, translation/correction history, errata review, or
reviewer. The received description is consequently provisional `H5`: it is not yet a stable claim
to which human proof debt can be assigned. It is neither H0 evidence nor an elaboratable statement.

## Bibliographic leads, not credited sources

Crossref and Semantic Scholar metadata identify Hans Zassenhaus, *Beweis eines Satzes ueber
diskrete Gruppen*, *Abhandlungen aus dem Mathematischen Seminar der Universitaet Hamburg* 12(1)
(1937), pp. 289-312, DOI `10.1007/BF02948950`. This matches the author and year but its title does
not identify the catalog's extension-classification gloss. The publisher endpoints returned
closed-access HTML rather than primary article text. No theorem passage or definition was inspected,
so the paper is not mapped to this target.

Crossref and Semantic Scholar also identify Charles Edward Johnson and Hans Zassenhaus, *On
equivalence of finite group extensions*, *Mathematische Zeitschrift* 123(3) (1971), pp. 191-200,
DOI `10.1007/BF01114788`. Its title matches the subject more closely, but its date and coauthorship
conflict with the catalog. Its primary text was likewise unavailable. It is a discovery lead only,
not an exact source-statement crosswalk.

No complete published proposition or proof has been admitted from either record. A source reviewer
must resolve the target identity rather than combining the catalog's 1937 date with the 1971 title.

## Component crosswalk

| Catalog component | Candidate reading | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| group extension | short exact sequence `1 -> N -> E -> G -> 1` | `GroupExtension N E G` | useful vocabulary; catalog convention unknown |
| equivalence | middle-group isomorphism commuting with endpoint maps | `GroupExtension.Equiv S S'` | one possible relation; source relation unknown |
| classification | equivalence classes correspond to factor/cohomology data | no complete classification declaration found | classifying invariant and theorem direction unknown |
| split case | split extension corresponds to a semidirect product | `GroupExtension.Splitting.semidirectProductToGroupExtensionEquiv` | adjacent special case, not the unstated root |
| `已验证` | untrusted inventory label | an accepted exact-type/kernel receipt would be required | no H or M credit |

## Lean discovery anchors

At the manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks the extension,
equivalence, section, splitting, semidirect-product, and split-extension interfaces. The two
inspected nontrivial boundary declarations report `propext`, `Classical.choice`, and `Quot.sound`
through `#print axioms`.

The same pinned source explicitly lists the desired-looking abelian-kernel `H^2` classification as
a TODO, and `groupCohomology.LowDegree` lists the relationship between `H2` and group extensions as
a TODO. These are source-boundary observations only. No exact target, wrapper, terminal proof body,
or machine completion is credited. The anchor-audit phase must repeat a precommitted search after a
canonical proposition exists.

## Source gate

Before statement acceptance, accountable reviewers must preserve an immutable primary edition;
select and transcribe the exact theorem and incorporated definitions; resolve author/date/title
conflicts; map every premise and conclusion to one canonical Lean expression; inspect corrections
and errata; and approve all boundary cases. Until then the canonical statement, formal expression,
environment fingerprint, alternate transports, and proof architecture remain null or open.
