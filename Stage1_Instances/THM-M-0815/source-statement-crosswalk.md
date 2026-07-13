# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5991-5996` supplies exactly the title `霍尔婚配定理`, Philip
Hall, 1935, the gloss `二部图完美匹配存在的条件`, importance "high," and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record does not define bipartition, matching,
perfectness, neighborhood, cardinality, finiteness, graph coverage, binder order, or the direction
of the claimed condition. It has no theorem/page citation, proof boundary, errata record, reviewer,
or formal-artifact link.

`Docs/Stage0_Blueprint.md:22253-22278` repeats the gloss while explicitly leaving precise
definitions and premises, proof route, alternate forms, axioms, machine status, and artifacts open.
The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Historical source lead

Pinned mathlib's bibliography and observed Crossref metadata identify P. Hall, *On Representatives
of Subsets*, *Journal of the London Mathematical Society* s1-10 (1935), issue 1, pages 26-30, DOI
`10.1112/jlms/s1-10.37.26`. Crossref and Semantic Scholar metadata were observed with body SHA-256
values `9ce8715df3e4b5f28c6d2bf88f9068f4cfb45c73bcef29461819f6892b251aff` and
`8ac34a248370385b52822465892be26f2b1853a297eb1c8194549cb6b6b90dc8`; the latter marked the
article closed. The publisher and DOI PDF routes returned HTTP 403. Thus the primary text, exact
result locator, literal proposition, proof, and errata were not inspected. This is bibliographic
discovery, not H0 evidence. The observed API bodies were transient network research and are not
vendored or claimed as durable release evidence.

## Inspected secondary formalization source

Alena Gusakov, Bhavik Mehta, and Kyle A. Miller, *Formalizing Hall's Marriage Theorem in Lean*,
arXiv:`2101.00127v1` (2021), was inspected from a 15-page PDF of 284171 bytes, SHA-256
`3521dd4b8f54e13027098c6b069276a1e2a03edf0e07b1e3033d4aa6f4ddb009`. It is a secondary
source and formalization report, not a substitute for an independently reviewed primary-source
packet. The observed PDF bytes are not vendored or release evidence. It states three relevant
versions:

- Theorem 2.1.3: a finite indexed family of finite sets has distinct representatives iff every
  subfamily's index cardinality is at most the cardinality of its union.
- Theorem 2.2.2: a relation between finite sets has a matching saturating its left set iff every
  left subset has cardinality at most that of its relational image.
- Theorem 2.3.4: a bipartitioned graph, with the left part and its vertex neighborhoods finite, has
  a matching saturating the left part iff every left subset is no larger than its neighborhood.

These formulations show that the ordinary graph theorem guarantees saturation of one selected
part, not automatically a perfect matching of the entire vertex set. The catalog's word
`完美匹配` may intend a balanced finite bipartite corollary, a convention that calls one-side
saturation "complete," or an imprecise gloss. Intake cannot silently choose among those meanings.

## Component crosswalk

| Catalog component | Candidate mathematical reading | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| bipartite graph | `G.IsBipartiteWith p1 p2` | `Mathlib.Combinatorics.SimpleGraph.Hall` | coverage of all vertices is not inherent; exact convention open |
| neighborhood condition | every `s` in the selected left part satisfies `|s| <= |N(s)|` | `exists_isMatching_of_forall_ncard_le` | direct one-side sufficient interface; reverse direction and exact finiteness scope must be mapped |
| perfect matching | every graph vertex is incident to exactly one matching edge | `Subgraph.IsPerfectMatching` and `exists_isPerfectMatching_of_forall_ncard_le` | pinned theorem assumes the inequality for every vertex subset, not just the left part |
| standard Hall theorem | matching saturating the finite left part iff its subset condition | finite-family and relation `Iff` declarations | strong candidate, but not identical to the literal word "perfect" without an approved bridge |
| `已验证` | untrusted inventory label | accepted H/M receipts would be required | no source or kernel credit |

Pinned `Mathlib.Combinatorics.SimpleGraph.Matching` defines `Subgraph.IsPerfectMatching` as
`M.IsMatching ∧ M.IsSpanning`, confirming that "perfect" means every vertex of the graph is
matched in this formal vocabulary rather than merely every vertex in one selected part.

## Pinned formal leads

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Finset.all_card_le_biUnion_card_iff_existsInjective'` is the finite-index distinct-representative
  equivalence.
- `Finset.all_card_le_biUnion_card_iff_exists_injective` generalizes the index type through a
  compactness/inverse-system argument while keeping every family member finite.
- `Fintype.all_card_le_rel_image_card_iff_exists_injective` and
  `Fintype.all_card_le_filter_rel_iff_exists_injective` give relation forms.
- `SimpleGraph.exists_isMatching_of_forall_ncard_le` yields a matching covering one selected
  bipartition from its subset condition.
- `SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le` yields a perfect matching from the
  stronger condition quantified over all subsets of the vertex type.

The probe elaborates these interfaces and reports `propext`, `Classical.choice`, and `Quot.sound`
for the four printed declarations. This authenticates pinned APIs only. Exact expression comparison,
reverse graph implication, checked transports, terminal body provenance, dependency closure, and
axiom-policy acceptance belong to later phases.

## First downstream gate

The statement phase must admit one lawful immutable primary statement and independently determine
whether the root is a finite distinct-representative theorem, a matching saturating one side of a
bipartite graph, or a balanced/global perfect-matching theorem. It must then freeze all domains,
finiteness and coverage assumptions, ordered binders, cardinality conventions, conclusion, boundary
cases, minimal imports, checked alternate encodings, and the four required mutation classes. Until
then the status remains `H1 / M3 / R4` and the canonical expression remains null.
