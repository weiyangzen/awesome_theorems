# Source-statement crosswalk

## Repository source boundary

`Docs/researches/math_theorems.md:6474-6479` contains exactly the title `Ramanujan graphs`, the
attribution `many mathematicians`, the period `twentieth century`, the phrase `optimal spectral
expander graphs`, importance `high`, and an untrusted `verified` label. All six uncited lines
originate at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no
formula, definition, quantifiers, hypotheses, conclusion, source locator, proof boundary, errata
status, formal revision, or reviewer.

`Docs/Stage0_Blueprint.md:24116-24141` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifacts open. Its generic scheduling prose about a known closed result does
not select or prove a proposition.

## Exact-topic source lead

Alexander Lubotzky's *Ramanujan Graphs*, `arXiv:1711.06558v1` (submitted 2017-11-15), is an
immutable exact-topic exposition. The inspected arXiv PDF has SHA-256
`cfcdc1d023eb9ab8bb7397fefa98b216cce74770fcbb9177b84ee2534f65a32e`; the arXiv source gzip has
SHA-256 `a6c798d891916bb39ff4c3ae59126ce2d8a45072abd801287429dba0f953ab80` and its decompressed TeX
has SHA-256 `1a213fc53eb5a6a7d56d78cb65dc8c011aa0fe50576516517ea4064745d77b64`.

The opening text gives the standard object boundary:

```text
X is a finite connected k-regular graph, k >= 3. It is Ramanujan when every adjacency
eigenvalue lambda satisfies |lambda| = k or |lambda| <= 2 * sqrt(k - 1).
```

It notes that `k` is always an eigenvalue, `-k` occurs exactly in the bipartite case, invokes
Alon-Boppana to explain why the bound is best possible for an infinite family, and separately says
Ramanujan graphs are optimal expanders from the spectral point of view. It also discusses Cheeger
expansion, existence, LPS/Morgenstern constructions, and later all-degree bipartite existence.

This source is an `E5` intake lead, not H0. It is an exposition rather than a catalog-cited
pinpoint root, and no source reviewer has approved which definition or theorem the repository owns,
mapped its proof nodes, or audited corrections. Its exactness to the subject helps delimit choices
but does not authorize choosing one for the catalog.

The original LPS article, A. Lubotzky, R. Phillips, and P. Sarnak, *Ramanujan graphs*,
*Combinatorica* 8(3) (1988), 261-277, DOI `10.1007/BF02126799`, is another exact-subject source
lead. Publisher metadata describes explicit regular Cayley graphs whose eigenvalues obey the same
bound and calls the property optimal. That construction belongs to neighboring target
`THM-M-0883`; it cannot be substituted for this general topic target.

## Clause crosswalk

| Catalog/source phrase | Candidate mathematical component | Lean surface required later | Intake assessment |
|---|---|---|---|
| `Ramanujan graph` | a finite connected regular graph satisfying a nontrivial adjacency-spectrum bound | graph type, finiteness, connectedness, degree, adjacency operator, spectrum, trivial-eigenvalue predicate | standard source lead only; no selected root |
| `k-regular`, `k >= 3` | uniform finite vertex degree and lower-degree convention | `SimpleGraph.IsRegularOfDegree k`, finite vertex type, arithmetic coercions | omitted by catalog |
| `|lambda| = k` | positive and, for bipartite graphs, negative trivial eigenvalues | eigenvalue occurrence and absolute-value exclusion with multiplicity policy | omitted by catalog |
| `|lambda| <= 2 sqrt(k-1)` | closed Ramanujan spectral boundary | real adjacency spectrum and exact natural-to-real coercion | omitted by catalog |
| `optimal` | Alon-Boppana asymptotic necessity, optimal universal-cover spectrum, or best expansion/mixing behavior | a separately selected theorem with family limit and normalization | ambiguous slogan |
| `spectral expander` | relation between adjacency spectrum, Cheeger expansion, or mixing | exact expansion predicate and bridge theorem | omitted by catalog |
| `verified` | untrusted inventory value | accepted source and kernel receipts would be required | no H or M credit |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the narrow probe
checks `SimpleGraph.IsRegularOfDegree`, real adjacency matrices, Hermitian symmetry and indexed
Hermitian eigenvalues, spectrum membership, and `Real.sqrt`. A bounded literal search found no
graph-theoretic `Ramanujan`, `Alon-Boppana`, or spectral-expander declaration in repo-local or
pinned-mathlib Lean sources. The unrelated Ramanujan name in analytic number theory is not a
candidate.

These APIs are substrate only. They neither choose how to represent a spectrum with multiplicity
nor prove connectedness, regularity, the Ramanujan bound, existence, construction, or optimality.
This is bounded intake discovery, not the downstream immutable anchor audit or a global absence
claim.

## Exact-statement gate

The statement phase must first select and independently approve an immutable pinpoint source root.
It must then freeze every incorporated definition, ordered binder, domain, hypothesis, conclusion,
degenerate case, graph and spectrum convention, family/limit quantifier, minimal import, expression
and environment fingerprint, checked transport, and required hypothesis/domain/scope/boundary
mutation. Until that happens the canonical claim remains null and no proof evidence may be credited.
