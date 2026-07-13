# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6173-6178` records only the Chinese title `Erdos-Stone定理`,
Erdos/Stone, 1946, high importance, the gloss `极值图论的基本定理` ("a fundamental theorem of
extremal graph theory"), and `已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 explicitly leaves definitions, assumptions,
proof route, axioms, and formal artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

This record identifies a theorem family but not a proposition. In particular it does not choose
the original complete-equipartite containment form or the now-standard forbidden-graph
chromatic-density form.

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
the iterated-log exponent. Exact transcription, errata/corrections, complete proof-node mapping,
and independent review remain open, so this evidence is `H1`, not `H0`.

## Component crosswalk

| Mathematical component | Repository | 1946 source | Pinned Lean lead | Intake result |
|---|---|---|---|---|
| finite simple graph and edge count | unnamed | definitions, p. 1087 | `SimpleGraph`, `edgeFinset` | compatible nouns only |
| complementary graph | omitted | definition and main theorem, p. 1087 | `SimpleGraphᶜ` | convention not frozen |
| `epsilon` and `r` | omitted | `0 < epsilon < 1`, `r >= 2`, p. 1087 | `Real`, `Nat` | binders not frozen |
| eventual vertex threshold | omitted | `exists n0, forall n > n0`, p. 1087 | `Filter.atTop` or explicit threshold | encoding open |
| equal independent groups | omitted | `r` groups, explicit iterated-log size, p. 1087 | complete equipartite graph in complement | exact size formula open |
| complete cross-group form | omitted | complement restatement, p. 1088 | `completeEquipartiteGraph r t` containment | transport open |
| extremal sharpness | omitted | disjoint complete graphs, p. 1090 | Turan/complete-multipartite APIs | not audited as a root |
| modern fixed-`H` density formula | omitted | not stated in this notation | `extremalNumber`, `turanDensity`, `chromaticNumber` | proposition/source bridge open |

## Pinned formal-source inspection

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides an exact API
substrate but no pinned Erdos-Stone conclusion:

- `Mathlib.Combinatorics.SimpleGraph.Extremal.TuranDensity` defines Turan density, proves its
  convergence, and forces containment above `turanDensity H + epsilon`.
- `Mathlib.Combinatorics.SimpleGraph.CompleteMultipartite` defines equal-part complete graphs and
  their containment witness.
- `Mathlib.Combinatorics.SimpleGraph.Coloring` computes the chromatic number of nonempty complete
  multipartite graphs.

A documentation index lists the theorem title without a declaration. The package git object store
also happens to contain later commit `b9df47b72b287802f6d40cf7588dada976bc657d`, whose unpinned file
adds a minimum-degree Erdos-Stone theorem. That commit is not an ancestor of the pinned revision,
the file is absent from the pinned tree, and worker policy forbids changing `.lake`; it is only a
downstream discovery lead, never local validation or proof evidence.

## Honest status

- `H1`: the primary paper and theorem page are identified and inspected, but exact transcription,
  modern-equivalence mapping, corrections, full premise/proof mapping, and review are unfinished.
- `M3`: pinned definitions and interfaces elaborate, but no canonical target, exact pinned theorem,
  checked transport, or proof closure is credited.
- `R4`: this crosswalk is an intake boundary, not a readable proof reconstruction.

No canonical obligation ID or statement fingerprint is emitted before statement freeze.
