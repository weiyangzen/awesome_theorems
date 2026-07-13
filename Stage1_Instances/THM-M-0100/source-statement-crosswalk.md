# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:733-738` supplies exactly the title `卡查丹性质(T)`, attribution to
David Kazhdan, the year 1967, the gloss `关于群表示的刚性性质` ("a rigidity property concerning
group representations"), importance `high`, and status `verified`. Git history places all six
uncited fields in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2848-2873` repeats the metadata while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, equivalent forms, axiom
policy, machine-checked status, and artifact links open. The rev-5.6 manifest preserves `verified`
only as untrusted metadata and resets the target to `L0 / rework_required`.

The catalog contains no group domain, definition of a unitary representation, topology or
continuity condition, quantified proposition, compact subset, positive constant, vector contract,
proof boundary, bibliography, theorem/page locator, correction history, or reviewer. It names a
property family but does not state a theorem.

## Source leads

The author-hosted draft by B. Bekka, P. de la Harpe, and A. Valette, *Kazhdan's Property (T)*,
dated February 23, 2007, was inspected on 2026-07-13. It gives these distinct source surfaces:

- printed pages 31-32 define strongly continuous unitary representations, `(Q, epsilon)`-invariant
  vectors, almost invariant vectors, and nonzero invariant vectors;
- Definition 1.1.3 on printed page 33 defines a Kazhdan set and says that a topological group has
  Property (T) exactly when it has a compact Kazhdan set;
- Proposition 1.2.1 on printed page 36 states the equivalent implication from weak containment of
  the trivial representation to its containment;
- Theorem 1.2.5 on printed page 40 gives a locally compact group/Fell-topology characterization;
- Theorem 1.3.1 on printed page 41 gives compact generation, and the introduction separately lists
  higher-rank examples, lattice inheritance, and the Delorme-Guichardet equivalence.

Crossref metadata for D. A. Kazhdan, *Connection of the dual space of a group with the structure of
its close subgroups*, *Functional Analysis and Its Applications* 1(1) (1967), 63-65, DOI
`10.1007/BF01075866`, was also inspected. It confirms the original-paper bibliography but does not
supply proposition text. A publisher PDF request returned an HTML access page, not the article.

These leads expose the ambiguity rather than resolving it. No exact root has been selected; the
original proposition has not been transcribed; and no complete incorporated-definition,
assumption, conclusion, proof-node, correction/errata, translation, repository-preservation, or
independent-review record is accepted. The source identifies a standard definition family, but the
received catalog target remains provisional `H5`, not `H0`, because it is not a stable theorem
proposition.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "group" | topological group; locally compact group for some characterizations; sigma-compact locally compact group for Property (FH) equivalence | `Group G`, `TopologicalSpace G`, topological-group and compactness typeclasses | exact source domain absent |
| "representation" | strongly continuous unitary representation on a complex Hilbert space | a group homomorphism into continuous linear isometries/unitaries plus orbit continuity | pinned algebraic `Representation` is only partial substrate |
| "rigidity" | almost invariant vectors force a nonzero invariant vector | compact `Q`, positive `epsilon`, norm estimates, `Representation.invariants` or an analytic refinement | conclusion not selected |
| Property (T) | compact Kazhdan set, weak-containment characterization, Fell isolation, Property (FH), consequence, or example theorem | a predicate plus separately checked theorem statements and transports | property name is not a unique theorem |
| `verified` | untrusted inventory label | no declaration, wrapper, or proof body | explicitly rejected as evidence |

## Variant boundary

The compact-Kazhdan-set definition and the almost-invariant-vector implication are equivalent at the
mathematical level, while Fell-topology and Property (FH) forms require additional hypotheses and
substantial definitions. Compact generation, higher-rank examples, and lattice inheritance are
consequences, not definitions. None is adopted as the root without a pinpoint source crosswalk.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
checks `Representation`, `Representation.invariants`, `Representation.mem_invariants`, and
`Representation.invariants_eq_inter`. These model algebraic group representations and invariant
vectors only. They do not provide strong continuity, unitarity, almost invariant vectors, compact
Kazhdan sets, or Property (T). A bounded case-insensitive search found no Kazhdan Property (T)
definition or theorem in repo-local Lean or pinned mathlib; Kazhdan hits concerned Kazhdan-Lusztig
theory. This is not an exhaustive external-project audit and cannot prove absence.

## Required source admission

The statement phase must preserve and hash a lawful complete source edition, select an exact result
and proof boundary, map every incorporated definition, ordered binder, hypothesis, conclusion and
boundary case, audit corrections and translation, and obtain independent review. It must then
freeze and mutation-test the same exact Lean expression. Until then the canonical mathematical and
Lean targets remain null and the source classification remains `H5`.
