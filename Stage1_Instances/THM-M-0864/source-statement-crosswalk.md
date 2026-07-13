# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6334-6339` supplies exactly the title `Tutte连通度定理`, attribution
to William Tutte, the year 1961, the gloss `3-连通图的轮分解` ("wheel decomposition of 3-connected
graphs"), importance "high," and status `已验证`. Git history attributes all six uncited lines to
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, exact
proposition, definitions, binders, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23576-23601` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Primary bibliographic lead

Crossref's DOI record and Elsevier's metadata endpoint identify W. T. Tutte, *A theory of
3-connected graphs*, Indagationes Mathematicae (Proceedings) 64 (1961), pages 441-455, DOI
`10.1016/S1385-7258(61)50045-5`, PII `S1385725861500455`. Modern bibliographies also cite the
journal numbering as *Indag. Math.* 23 (1961), 441-455.

The article full text was not available through the inspected metadata endpoints, and the
publisher PDF route returned an access-denial page. Consequently the original theorem number/page,
incorporated definitions, precise deletion/contraction operations, proof, translations,
corrections, and errata were not inspected. The metadata establishes primary bibliographic identity
only; it is not an E4 source crosswalk or H0 evidence.

## Inspected modern source lead

Johannes Carmesin and Jan Kurkofka, *Canonical Decompositions of 3-Connected Graphs*, arXiv
`2304.00945v3` (2025), Section 2.7, printed page 56, was inspected from the versioned arXiv PDF.
Immediately before Theorem 2.7.1 it defines `G/e` as the multigraph obtained by contracting edge
`e`, and calls `G` minimally 3-connected when `G` is 3-connected and neither `G - e` nor `G/e` is
3-connected for every edge `e`. Theorem 2.7.1 then states:

> Every minimally 3-connected finite graph G is a wheel.

Its reference [65] is Tutte's 1961 article, pages 441-455. The observed versioned PDF SHA-256 is
`6856032350da337d118b9954cdcecd0558685e2af57f10d78eb262fa30cbbadd`; extracted text SHA-256 is
`8728c815039e306acd3a241785a441bc80b820d378b649a1192b9a97d7df73ac`.

This precise modern theorem strongly identifies a likely core of the catalog family, but the
catalog does not cite it and uses the broader word "decomposition." It does not settle whether the
intended root is this minimal characterization or a reduction/construction-sequence equivalent.
The source supports provisional `H1`, not H0 or a frozen canonical statement.

## Clause crosswalk

| Catalog component | Modern source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| 3-connected graph | finite 3-connected graph/multigraph | future vertex-deletion connectivity predicate over `SimpleGraph` or another graph carrier | ordinary `Connected` exists; exact 3-connectivity encoding absent |
| minimality | every edge deletion and contraction destroys 3-connectivity | `deleteEdges` plus a future contraction and simplification transport | contraction API and carrier transition not located |
| wheel | conclusion up to the source's graph equality/isomorphism convention | future hub-plus-`cycleGraph` predicate and `SimpleGraph.Iso` | `cycleGraph` exists; no ordinary wheel definition located |
| wheel decomposition | not the literal wording of inspected Theorem 2.7.1 | reduction sequence or inductive construction, if source-selected | orientation and allowed operations open |
| finite | explicit in the modern theorem | `Fintype`/`Finite` vertex carriers and possibly finite multigraphs | exact carrier and typeclasses open |
| `已验证` | untrusted inventory label | accepted source review and kernel receipt would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib contains `SimpleGraph.Connected`, `SimpleGraph.Subgraph.deleteVerts`,
`SimpleGraph.cycleGraph`, `SimpleGraph.cycleGraph.cycle`, `SimpleGraph.Iso`,
`SimpleGraph.replaceVertex`, and single-edge addition/deletion infrastructure. These are adjacent
building blocks only. No direct vertex 3-connectivity, ordinary wheel, edge contraction, minimal
3-connectivity, or Tutte wheel theorem declaration was found in the bounded search.

`Mathlib.Combinatorics.SimpleGraph.Tutte` formalizes the perfect-matching theorem, while
`SimpleGraph.IsFiveWheelLike` belongs to a different clique-free extremal construction. Their names
must not be mistaken for anchors or proof bodies for THM-M-0864. Machine debt remains `M4`.

## Source gate

Before leaving H1 or freezing a statement, accountable reviewers must admit an immutable exact
source, locate the original or authoritative theorem and incorporated definitions, decide the
minimal-characterization versus reduction/construction root, map every graph carrier, operation,
binder, hypothesis, conclusion, and boundary case, audit corrections and errata, and independently
approve fidelity to THM-M-0864. Only then may the statement phase elaborate the same proposition,
record expression/environment fingerprints and checked alternate transports, and execute the four
required mutation classes.
