# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `Dinitz猜想`, Jeff Dinitz, 1979, and the full statement
gloss `列表着色的存在性` (existence of list coloring). It supplies no bibliography, definitions,
domains, quantifiers, hypotheses, conclusion, proof, or formal artifact. All six catalog lines date
to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; that is repository provenance,
not a mathematical source revision.

`Docs/Stage0_Blueprint.md` repeats the gloss and explicitly marks precise definitions and premises,
proof process, dependencies, equivalent formulations, axioms, machine status, and artifact links as
open. The rev-5.6 manifest carries `已证明` only as `source_status_untrusted`.

## Intake crosswalk

| Repository phrase | Candidate mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Dinitz猜想` | classical `n x n` array selection problem | functions on `Fin n -> Fin n` | recognized family; exact source not selected |
| "list coloring" | one allowed-color collection per cell | `Finset Color`, `Multiset Color`, or `List Color` | representation and duplicate semantics open |
| "existence" | a chosen entry in every cell | existential choice function `c` | candidate conclusion only |
| row/column condition absent from gloss | pairwise distinct choices in every row and column | `Function.Injective` or `Pairwise` predicates | material conclusion missing from repository wording |
| graph translation | list edge-coloring of `K_(n,n)` | coloring of a line graph plus per-edge membership | transport must be checked; not target identity by name |
| `已证明` | untrusted catalog label | no declaration or proof object | explicitly rejected as evidence |

## Bibliographic source leads, not H0

Fred Galvin, *The List Chromatic Index of a Bipartite Multigraph*, Journal of Combinatorial Theory,
Series B 63(1), January 1995, pages 153-158, DOI `10.1006/jctb.1995.1011`, is the primary proof
lead. Crossref confirms the author, title, journal, date, volume, issue, page range, and DOI. The
publisher full text was not available for statement-level inspection in this run, so theorem
numbering, exact definitions, assumptions, proof boundary, and errata remain unaudited.

Tomaž Slivnik, *Short Proof of Galvin's Theorem on the List-chromatic Index of a Bipartite
Multigraph*, Combinatorics, Probability and Computing 5(1), 1996, pages 91-94, DOI
`10.1017/S0963548300001851`, is an inspected secondary proof source. Its publisher abstract states
that Galvin proved every `k`-edge-colorable bipartite multigraph is `k`-edge-choosable. That confirms
the stronger theorem family and cites Galvin's paper, but it neither supplies the original array
statement nor resolves this repository's boundary with `THM-M-0905`.

Neither record is H0. There is no admitted immutable primary-source packet, pinpoint mapping of all
array premises and conclusions, correction audit, or independent source reviewer.

## Source-family distinction

The classical array assertion is naturally the `K_(n,n)` special case: cells correspond to edges,
and sharing a row or column corresponds to incidence. Galvin's bipartite-multigraph result is
strictly broader. The repository immediately follows `THM-M-0904` with `THM-M-0905`, whose gloss is
`Dinitz猜想的证明` (proof of the Dinitz conjecture). Until an accountable source review fixes the
identity of both roots, this crosswalk treats Galvin's result only as a prospective stronger bridge.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`SimpleGraph.Coloring`, `SimpleGraph.Colorable`, `SimpleGraph.IsBipartite`,
`SimpleGraph.completeBipartiteGraph`, `SimpleGraph.lineGraph`, and its adjacency characterization.
A bounded search found no obvious Dinitz, Galvin, list-coloring, edge-choosability, or list-chromatic
declaration. These are local discovery observations only, not a complete downstream anchor audit or
an absence claim about external Lean projects.

The statement phase must admit an immutable source, freeze its exact array proposition and boundary
with the stronger graph theorem, then elaborate a minimal Lean target and checked transports. Until
that happens, the canonical statement, expression hash, obligation identifiers, and H0 status remain
open.
