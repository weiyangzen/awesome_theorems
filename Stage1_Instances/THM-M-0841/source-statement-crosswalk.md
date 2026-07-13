# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6173-6178` records only the Chinese title `Erdos-Stone定理`,
Erdos/Stone, 1946, high importance, the gloss `极值图论的基本定理` ("a fundamental theorem of
extremal graph theory"), and `已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 explicitly leaves definitions, assumptions,
proof route, axioms, and formal artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

This record alone identifies a theorem family but not a proposition. The statement phase resolves
that ambiguity conservatively by selecting the only theorem named in the attributed 1946 paper,
rather than substituting a later standard corollary.

## Inspected primary source

Paul Erdos and A. H. Stone, "On the structure of linear graphs", *Bulletin of the American
Mathematical Society* **52** (1946), 1087-1091, DOI `10.1090/S0002-9904-1946-08715-7`, was
inspected from the Renyi Institute's collected-papers scan `1946-08.pdf` (432122 bytes, SHA-256
`83ae35a7185e2e6462ccc314c3a20c2b6d85fc142a2cc857603fbf9661f550e1`).

The source defines finite simple graphs, complements, complete graphs, integer rounding, and
iterated natural logarithms on printed page 1087. Its single named theorem on page 1087 says,
without modernizing the symbols, that for positive `epsilon < 1` and integer `r >= 2`, sufficiently
large `n` forces `r` mutually exclusive groups of equal size in any `n`-vertex graph having fewer
than `(1 / (2 * (r - 1)) - epsilon) * n^2` edges; no vertices in different groups are joined. The
group size has an explicit iterated-log lower bound. On page 1088 the paper restates this in the
complement, where every cross-group pair is joined. Pages 1088-1090 prove it by induction on `r`,
using the page-1087 intersection lemma. Page 1090 gives the disjoint-union extremal example.

The page-1088 restatement is not a definitional same-`epsilon` rewrite: a complement has
`n.choose 2`, not `n^2 / 2`, possible edges. An exact formal transport must rename or reduce the
tolerance and absorb the linear `n / 2` discrepancy under the eventual threshold.

The scan was visually inspected because extracted OCR damages comparison signs, subscripts, and
the iterated-log exponent. The page image fixes the statement transcription used by
`ErdosStoneTarget`; errata/corrections, complete proof-node mapping, and independent review remain
open, so this evidence is `H1`, not `H0`.

The paper also says that letters such as `n` and `k` usually denote positive integers. Lean uses
`Nat` binders plus explicit `0 < n0` and `0 < k` conjuncts, so this convention is not silently lost.

## Component crosswalk

| Mathematical component | Repository | 1946 source | Pinned Lean lead | Intake result |
|---|---|---|---|---|
| finite simple graph and edge count | unnamed | definitions, p. 1087 | `SimpleGraph`, `edgeFinset` | compatible nouns only |
| complementary graph | omitted | definition and main theorem, p. 1087 | `SimpleGraphᶜ` | exact sparse-root convention frozen |
| `epsilon` and `r` | omitted | `0 < epsilon < 1`, `r >= 2`, p. 1087 | `Real`, `Nat` | exact ordered binders frozen |
| eventual vertex threshold | omitted | positive integer `n0` and `exists n0, forall n > n0`, p. 1087 | explicit positive threshold | exact source order and integer convention frozen |
| equal independent groups | omitted | `r` groups of some positive natural `k >= sqrt(l_(r-1)(n))`, p. 1087 | `completeEquipartiteGraph r k` in the complement | exact existential size and lower bound frozen |
| complete cross-group form | omitted | complement restatement, p. 1088 | `completeEquipartiteGraph r t` containment | neighboring dense transport remains open |
| extremal sharpness | omitted | disjoint complete graphs, p. 1090 | Turan/complete-multipartite APIs | not audited as a root |
| modern fixed-`H` density formula | omitted | not stated in this notation | `extremalNumber`, `turanDensity`, `chromaticNumber` | proposition/source bridge open |

## Pinned formal-source inspection

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the exact statement
substrate but no pinned Erdos-Stone conclusion:

- `Mathlib.Combinatorics.SimpleGraph.Extremal.TuranDensity` defines Turan density, proves its
  convergence, and forces containment above `turanDensity H + epsilon`.
- `Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite` defines equal-part complete graphs and
  their containment witness.
- `Mathlib.Analysis.SpecialFunctions.Log.Basic` supplies the real logarithm and square root used in
  the source's explicit growing part-size lower bound.

A documentation index lists the theorem title without a declaration. The package git object store
also happens to contain later commit `b9df47b72b287802f6d40cf7588dada976bc657d`, whose unpinned file
adds a minimum-degree Erdos-Stone theorem. That commit is not an ancestor of the pinned revision,
the file is absent from the pinned tree, and worker policy forbids changing `.lake`; it is only a
downstream discovery lead, never local validation or proof evidence.

## Honest status

- `H1`: the primary paper and theorem page are identified and the exact displayed proposition is
  transcribed, but modern-equivalence mapping, corrections, full proof mapping, and review are unfinished.
- `M3`: the canonical target, definition-unfolding transport, mutations, and boundaries elaborate
  with pinned minimal imports, but no Erdos-Stone proof closure is credited.
- `R4`: this crosswalk is an intake boundary, not a readable proof reconstruction.

The statement fingerprint is `sha256:ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733`.
No proof obligation registry is frozen before the later obligation-tree phase.
