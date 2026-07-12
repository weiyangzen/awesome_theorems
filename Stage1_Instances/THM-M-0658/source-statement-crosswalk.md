# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only the title "Shelah stability theory", attributes it
to Saharon Shelah, gives the year 1978, and repeats "stability theory" as its entire statement.
Stage0 adds no definitions, hypotheses, proof, source locator, or formal artifact. The target
manifest preserves `已验证` as explicitly untrusted metadata. These records establish catalog
identity only; they do not identify an exact theorem.

## Primary-source discovery lead

Saharon Shelah, *Classification Theory and the Number of Non-Isomorphic Models*, North-Holland,
1978, is the natural primary monograph lead suggested by the repository year. A revised edition
also exists, so edition drift may materially change numbering and formulation. No immutable copy
has been inspected for this intake, and no chapter, theorem, page, incorporated definition,
assumption, correction, or erratum is claimed. The monograph is therefore an `E5` discovery lead,
not `H0` evidence and not yet a selected root.

## Crosswalk

| Repository phrase | Possible mathematical reading | Required formal surface | Intake decision |
|---|---|---|---|
| stability | a bound on complete types over parameter sets or models | first-order theories, complete types, cardinality, parameter expansion | candidate only |
| stable theory | stability in specified cardinals, often for a complete theory | completeness plus explicit cardinal and quantifier order | assumptions unresolved |
| stability theory | the wider theory of order property, types, ranks, forking, spectra, and classification | multiple definitions and substantive theorems | topic, not a root proposition |
| 1978 | likely points to the first edition of Shelah's classification monograph | immutable edition and pinpoint locator | unverified metadata |
| verified | historical catalog status | kernel receipt and source review would be required | no credit |

## Pinned Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.ModelTheory.Semantics` supplies theories and model satisfaction, while
`Mathlib.ModelTheory.Topology.Types` supplies complete types and their type-space basic opens.
`IntakeProbe.lean` checks these declarations with the pinned Lean executable.

The scoped mathlib search found no model-theoretic declaration named for Shelah, stable theories,
the order property, forking, superstability, or a stability spectrum. The repo-local legacy
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_299.lean` belongs to `THM-M-0660`; its
`TypeCountingStableAt` is an explicitly limited local proxy and its comments state that
parameter/model-scope stability remains open. Neither this negative search nor that related proxy
is a complete formal-candidate audit or proof evidence.

## Unblock condition

A source reviewer must select one immutable edition and an exact numbered result, crosswalk every
definition and hypothesis, check corrections and edition differences, and independently confirm
that it is the intended meaning of this catalog entry. Until then, choosing a familiar stability
theorem would broaden or substitute the source rather than formalize it.
