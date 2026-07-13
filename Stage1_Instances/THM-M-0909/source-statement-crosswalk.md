# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:6649-6654` records exactly the title `Voigt定理`, attribution to
Margit Voigt, year 1993, gloss `非4-可选的平面图`, importance "high," and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The block supplies no bibliography, definitions,
domains, quantifiers, hypotheses, conclusion, construction, proof boundary, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:24791-24816` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent statements,
axioms, machine status, and artifact links open. The rev-5.6 target manifest preserves `已验证`
only as untrusted source metadata and resets the target to `L0 / rework_required`.

## Published source and review leads

Crossref metadata confirms Margit Voigt, *List colourings of planar graphs*, *Discrete Mathematics*
120, issues 1-3 (September 1993), pages 215-219, DOI
`10.1016/0012-365X(93)90579-I`. Crossref does not supply the theorem text or abstract.

Dan S. Archdeacon's zbMATH review, Zbl `0790.05030`, defines a graph as `k`-choosable when every
assignment of lists having at least `k` colors at each vertex admits a proper coloring selecting
from those lists. It reports that Voigt presents a planar graph on 238 vertices that is not
4-choosable, settling the first Erdos-Rubin-Taylor planar-list-coloring conjecture. This is strong
secondary evidence for the theorem family and numerical witness size.

The primary article itself was not available for statement-level inspection. No exact theorem or
page locator, incorporated definitions, graph and planarity conventions, construction audit,
assumption map, complete proof boundary, corrections, errata, or independent source admission is
recorded. The source classification is therefore `H1`, not `H0`.

zbMATH separately records *List colourings of planar graphs. (Reprint)*, *Discrete Mathematics* 306
(2006), 1076-1079, DOI `10.1016/j.disc.2006.03.027`. That bibliographic relationship is recorded,
but the reprint is not treated as the selected edition, a correction, or an independent proof.

## Statement crosswalk

| Source component | Candidate mathematical content | Prospective Lean component | Intake status |
|---|---|---|---|
| "a planar graph" | one finite simple graph, reported to have 238 vertices | finite vertex type, `SimpleGraph`, and an approved planarity witness | family identified; representation and planarity definition open |
| list assignment | an allowed-color set at each vertex | a function from vertices to finite color collections | carrier, palette, `Finset`/set/list semantics, and decidable equality open |
| at least four colors | each assigned list has cardinality at least 4 | a pointwise cardinality inequality | secondary-review wording only; exact primary convention uninspected |
| proper list coloring | adjacent vertices receive different selected allowed colors | ordinary `SimpleGraph.Coloring` plus pointwise membership | ordinary coloring API exists; list-membership interface absent |
| "not 4-choosable" | some list assignment defeats every proper allowed coloring | negation of a universal list-assignment property, or an explicit counterassignment witness | exact binder and witness form open |
| 238 vertices | size of Voigt's reported construction | cardinality equation for the witness carrier | secondary evidence; whether canonical root includes the number is open |
| `已验证` | untrusted catalog status | no declaration or proof object | rejected as evidence |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Coloring` supplies `SimpleGraph.Coloring`, `Coloring.mk`,
`Coloring.valid`, `SimpleGraph.Colorable`, and chromatic-number infrastructure. Its module TODO
explicitly lists planar graphs. A bounded case-insensitive search found no list-coloring,
choosability, Voigt, or graph-planarity declaration in pinned mathlib or repo-local Lean.

These are bounded intake observations, not a complete formal-candidate audit or an external absence
claim. Ordinary colorability is not list choosability. Until a source-approved proposition is
frozen, the canonical Lean module, expression, expression hash, environment fingerprint, checked
transports, and statement mutations remain null.
