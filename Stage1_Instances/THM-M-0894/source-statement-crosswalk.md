# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6544-6549` supplies exactly the title `距离正则图`, attribution
`众多数学家`, period `20世纪`, gloss `距离正则图的理论`, importance `高`, and status `已验证`.
All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
identifier, formula, definition, theorem number, proof boundary, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:24386-24411` mechanically expands the same record. It explicitly leaves
the target formal system, precise definitions and premises, proof route, dependent lemmas,
equivalent forms, axioms, machine state, and artifact links as `待补充`. The rev-5.6 manifest retains
`已验证` only as `source_status_untrusted`, assigns rank 1443 and the uniform
`L0 / rework_required` baseline, and records `theorem_complete=false`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `距离正则图` | the class of distance-regular graphs or any theorem about it | one exact predicate and proposition over a fixed graph model | subject identified; proposition open |
| `理论` | definitions, characterizations, parameters, spectra, constructions, classifications, or bounds | exact ordered binders, hypotheses, conclusion, and relationship to alternate encodings | no result is selected |
| `众多数学家`, `20世纪` | broad historical attribution | immutable edition and theorem/section/page with source-to-node mapping | no source credit |
| `已验证` | untrusted inventory metadata | inspected human proof and kernel evidence would be required | no H or M credit |

## Reference-family lead

Crossref metadata identifies Andries E. Brouwer, Arjeh M. Cohen, and Arnold Neumaier,
*Distance-Regular Graphs*, Springer, 1989, DOI `10.1007/978-3-642-74341-2`. The observed CSL JSON
has SHA-256 `6e9703f168491b9d4fc427e3a678e6a908f859ea1474a97b59df4037f5a320ed`.
Springer's book description says that the concept is a common setting for several regular graph
families and that the book also covers association schemes, representations, groups, geometries,
and codes. This is a strong subject reference, but it confirms breadth rather than selecting one
root. The repository does not cite the book; no complete edition, numbered proposition, proof,
correction or errata map, or independent review was admitted. It supplies no H0 evidence.

## Missing source-to-statement map

An H0 crosswalk would have to name an immutable primary or authoritative edition, stable locator,
incorporated definitions, every material premise and transition, exact conclusion, dependent source
IDs, corrections or errata, and an independent reviewer. None is present. In particular, the
repository does not decide:

- finite versus locally finite graphs, connectedness, simplicity, or nontriviality;
- natural versus extended distance and diameter conventions;
- which constant-intersection-count or algebraic definition is canonical;
- whether intersection numbers or arrays are data, hypotheses, or derived conclusions;
- which characterization, identity, spectral result, existence theorem, classification, or bound is
  the target; or
- how empty, disconnected, small-diameter, and out-of-range cases are treated.

The provisional human-source classification is therefore `H5`: the received subject wording is not
yet a stable truth-valued proposition. This classifies the repository target, not the truth or
human-proof status of standard distance-regular graph theorems.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded literal queries
found no `DistanceRegular`, distance-regular graph, or intersection-array declaration in the 7,871
Lean source files under mathlib. Nearby substrate exists in
`Mathlib.Combinatorics.SimpleGraph.Diam`, `Metric`, `Finite`, and `StronglyRegular`.

The intake probe checks representative distance, diameter, neighborhood, regularity, and strongly
regular declarations only. This is neither a global absence claim nor the downstream immutable
anchor audit. Generic APIs do not determine a source proposition, expression fingerprint, checked
transport, or proof body.

## Exact-statement gate

The dependent statement phase is blocked until accountable source selection resolves every row
above. It must then freeze domains and universes, ordered binders, all hypotheses, the exact
conclusion, degenerate cases, minimal pinned imports, an elaborated expression fingerprint, checked
alternate encodings, and removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. Intake creates no canonical mathematical or Lean statement and claims none of that gate.
