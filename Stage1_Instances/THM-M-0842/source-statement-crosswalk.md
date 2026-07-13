# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6180-6185` records only `Simonovits稳定性`, Miklós
Simonovits, 1968, the gloss `极值图的稳定性`, high importance, and `已验证`. All six lines
originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. This establishes
repository provenance only. It gives no bibliography, theorem number, definitions, binders,
hypotheses, conclusion, proof dependencies, errata, or formal artifact.

`Docs/Stage0_Blueprint.md:22982-23007` repeats the gloss while leaving precise definitions and
premises, proof route, dependencies, equivalent formulations, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets the target
to `L0 / rework_required`.

## Primary source

Miklós Simonovits, *A method for solving extremal problems in graph theory, stability problems*,
in *Theory of Graphs (Proceedings of the Colloquium, Tihany, 1966)*, Academic Press, New York,
1968, printed pages 279-319 (41 scanned pages), is the author-identified primary source. The
author's Rényi Institute publication index and author-hosted scan were inspected. Their observed
integrity data are recorded in `instance.json` and the provisional intake receipt.

The following are discovery locators, not an H0 crosswalk:

- printed pp.279-280 / scan pp.1-2: notation for the balanced complete `d`-partite graph and an
  introductory stability description using a quadratic edit budget;
- printed pp.281-282 / scan pp.3-4: the general definition of stability for a graph property,
  including deletion to a `d`-chromatic graph as an example property;
- printed p.309 / scan p.31, Theorem 7: a finite-family/extremal-graph stability result under the
  hypotheses inherited from Theorem 6;
- printed p.309 / scan p.31, Theorem 8(a): the concrete balanced-complete-multipartite exclusion
  theorem with `r >= 2`, `d >= 2`, and deletion to a `d`-chromatic graph;
- printed pp.310-314 / scan pp.32-36: proof of Theorem 8(a); and
- printed p.314 / scan p.36, Theorem 9: a distinct sharper structural result for extremal graphs.

The exact original notation, inherited premises, integer-part convention, source dependencies,
and corrections have not yet been mapped node by node or independently reviewed. The primary
source supports provisional `H1`, not H0.

## Modern statement discriminator

Yongtao Li and Yuejian Peng, *New proofs of stability theorems on spectral graph problems*,
arXiv:2203.03142v1 (2022), Theorem 1.2 on article page 2, states a widely used modern form:
for fixed `F` with chromatic number `r + 1 >= 3` and every positive `epsilon`, suitable `delta`
and `n0` make every sufficiently large `F`-free graph above the Turán-density threshold have edit
distance at most `epsilon*n^2` from `T_r(n)`. Its reference [45] gives the primary citation above.

József Balogh, Felix Christian Clemen, Mikhail Lavrov, Bernard Lidický, and Florian Pfender,
*Making K_(r+1)-Free Graphs r-partite*, arXiv:1910.00028v1 (2019), page 1 abstract and page 2,
records the clique-only deletion form and distinguishes Füredi's later quantitative strengthening.

These modern papers are secondary statement discriminators for this intake. Neither is accepted
as the target source, H0 evidence, or a formal proof body.

## Component crosswalk

| Catalog component | Primary/modern possibilities | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Simonovits, 1968 | original schema, Theorem 7, Theorem 8(a), or later conventional reformulation | immutable source ID plus exact theorem and dependency locators | family identified; root not selected |
| extremal graph | `F`-free, forbidden-family-free, or blow-up-free finite simple graph | `SimpleGraph.Free`, `CliqueFree`, `IsContained`, finite vertex type | forbidden object and finiteness policy open |
| almost extremal | close to `e(T_(n,d))`, `ex(n,F)`, or the asymptotic density | `edgeFinset.card`, `extremalNumber`, casts and inequalities | baseline and strictness open |
| stability | delete few edges to become `d`-colorable, or two-sided edits to `T_d(n)` | `deleteEdges`, `Colorable`, symmetric edge difference, relabeling | conclusion and normalization open |
| `已验证` | untrusted catalog label | no declaration or receipt | no H or M credit |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the pinned modules expose
`SimpleGraph.CliqueFree`, `Colorable`, `turanGraph`, `IsTuranMaximal`,
`isTuranMaximal_iff_nonempty_iso_turanGraph`, `extremalNumber_top`, `deleteEdges`, and
`edgeFinset_deleteEdges`. `IntakeProbe.lean` checks those APIs without declaring a theorem.

A bounded case-insensitive search over pinned mathlib found no `Simonovits`, edit-distance, or
extremal-stability declaration. Mathlib history after the pin contains a minimal-degree
Erdős-Stone module, and the public project
`mitchell-horner/ErdosStoneSimonovitsKovariSosTuran` contains Erdős-Stone-Simonovits asymptotic
density declarations at a different toolchain. Those are neighboring theorem candidates, not the
stability conclusion, and neither supplies repo-local proof closure here. A bounded negative search
is not a complete external anchor audit.

## Required source acceptance

Before exact statement elaboration, accountable reviewers must select one immutable proposition,
justify that it is the catalog target, and map every incorporated definition, ordered binder,
assumption, conclusion, theorem dependency, edit convention, rounding rule, correction, erratum,
and degenerate case. An independent graph-theory source reviewer must approve that mapping. Only
then may the statement phase minimize pinned imports, freeze expression and environment
fingerprints, compile checked transports, and run the required structural mutations.
