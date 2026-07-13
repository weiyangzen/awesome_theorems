# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7064-7069` supplies exactly the title `Lovász-Kneser定理`, the
attribution László Lovász, year 1978, the gloss `Kneser图的色数` ("the chromatic number of the
Kneser graph"), importance "high," and status `已验证`. All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no formula, definition, parameter
range, ordered binders, hypothesis, conclusion, citation, proof locator, correction history,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26362-26387` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate formulations,
axioms, machine status, and artifact links open. Rev-5.6 preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Primary publication lead

Crossref and Semantic Scholar metadata were inspected for L. Lovász, *Kneser's conjecture,
chromatic number, and homotopy*, Journal of Combinatorial Theory, Series A 25(3), November 1978,
pages 319-324, DOI `10.1016/0097-3165(78)90022-5`, PII `0097316578900225`. Crossref also records
the cited 1955 Kneser problem, *Aufgabe 300*.

CORE's secondary abstract says that Kneser's conjecture follows as a corollary: if all `n`-subsets
of a `(2n - k)`-element set are divided into `k + 1` classes, one class contains two disjoint
`n`-subsets. This supports the intended theorem family and the existence of a published proof, but
the article body was not inspected. The exact source notation, parameter range, definitions,
premise map, proof boundary, corrections, errata, and independent review therefore remain open.
The lead supports provisional `H1`, not `H0`.

## Clause crosswalk

| Repository/source element | Modern candidate component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "Kneser graph" | vertices are `k`-subsets of an `n`-set | `{s : Finset (Fin n) // s.card = k}` | standard lead only; representation and parameter names not source-frozen |
| graph adjacency | two vertices are adjacent iff their subsets are disjoint | `SimpleGraph.fromRel fun s t => Disjoint s.1 t.1` | probe elaborates; exact source transport open |
| "chromatic number" | least number of colors in a proper vertex coloring | `SimpleGraph.chromaticNumber : ENat` or `Colorable` minimality | codomain and equality encoding open |
| familiar value | `n - 2 * k + 2` when `0 < k` and `2 * k <= n` | coerced natural equality or colorable/non-colorable pair | not present in the catalog; primary-source confirmation required |
| Kneser-conjecture corollary | any coloring with too few colors has a disjoint monochromatic pair | negation of `Colorable` at one fewer color | secondary abstract only; checked equivalence open |
| Lovász, 1978 | publication and topological proof lead | source/provenance nodes and later proof obligations | bibliography is not statement identity or proof credit |
| `已验证` | untrusted catalog label | no Lean proposition or receipt | explicitly rejected as evidence |

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded search for
Kneser graph and Lovasz-Kneser spellings found no exact graph definition or theorem in repository
Lean sources or pinned mathlib. The only `Kneser` match in mathlib was an unrelated URL concerning
the additive Freiman-Kneser theorem.

`IntakeProbe.lean` checks fixed-cardinality finite subsets, disjointness, `SimpleGraph.fromRel`,
colorability, and chromatic-number interfaces. It also defines a candidate disjointness graph so
that feasibility is tested against the pinned environment. This definition is neither a canonical
target nor a proof. Exhaustive repo-local, mathlib, and external Lean candidate classification is
reserved for the dependent anchor-audit phase.

## Exit gate

Before the statement phase can close, an accountable reviewer must accept an immutable primary
source passage and its complete clause map; then the exact same proposition must be elaborated with
minimal pinned imports, serialized expression and environment fingerprints, checked alternate
transports, and the four required semantic mutations. Until then no H0, exact statement, or proof
credit attaches to this crosswalk.
