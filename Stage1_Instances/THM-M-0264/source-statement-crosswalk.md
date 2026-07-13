# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1901-1906` records the Chinese title
`波尔查诺-魏尔斯特拉斯定理`, attribution Bernard Bolzano/Karl Weierstrass, year 1817, gloss
`有界数列必有收敛子列`, high importance, and status `已验证`. Git history places all six uncited
lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record provides no formula,
domain, boundedness definition, theorem locator, proof passage, translation, errata record,
reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:7306-7331` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine state, and artifact links
open. The rev-5.6 manifest retains the verified label only as untrusted metadata and resets this
target to `L0 / rework_required`.

No immutable primary edition, theorem/page, complete assumption and proof crosswalk, correction
audit, or independent review is available in the repository. The classical family is sufficiently
identified for provisional `H1`, but not for `H0`.

## Literal component crosswalk

| Catalog component | Conventional mathematical reading | Lean candidate | Intake result |
|---|---|---|---|
| `数列` (sequence) | usually a natural-number-indexed real sequence in this real-analysis entry | `x : Nat -> Real` | strong candidate; source confirmation open |
| `有界` (bounded) | two-sided bounded range, equivalently an absolute-value bound | `Bornology.IsBounded (Set.range x)` | encoding and equivalence transport open |
| `子列` (subsequence) | terms chosen in their original order | `phi : Nat -> Nat` with `StrictMono phi`; sample `x \circ phi` | candidate matches standard encoding |
| `收敛` (convergent) | convergence to some real number | `Filter.Tendsto (x \circ phi) Filter.atTop (nhds a)` | topology and binder order open |
| title/category | classical real-analysis Bolzano-Weierstrass theorem | specialization of a proper-metric theorem to `Real` | family match, not statement identity |
| `已验证` | untrusted inventory label | accepted source and kernel receipts | no credit |

A conventional candidate root is therefore:

```text
for every x : Nat -> Real, if Set.range x is bornologically bounded, then there exist
a : Real and a strictly increasing phi : Nat -> Nat such that x composed with phi tends to a.
```

This prose is a resolution target only. It is not a frozen canonical statement or a source
quotation.

## Pinned Lean candidate crosswalk

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.MetricSpace.Sequences` explicitly says that it proves two Bolzano-Weierstrass
versions for proper metric spaces.

| Declaration | Exact-topic role | Identity boundary |
|---|---|---|
| `tendsto_subseq_of_bounded` | every term in a bounded set has a subsequence converging to a point in its closure | direct candidate; more general carrier and stronger closure conclusion than the likely real root |
| `tendsto_subseq_of_frequently_bounded` | frequently many terms in a bounded set suffice | alternate stronger extraction premise pattern, not supplied by the catalog |
| `Bornology.IsBounded.isCompact_closure` | bounded closure is compact in a proper space | Heine-Borel bridge used by the candidate, not the target by itself |
| `IsCompact.tendsto_subseq` | a sequence contained in a compact set has a convergent subsequence | compact-set bridge and close to separate target `THM-M-0619` |
| `SeqCompactSpace.tendsto_subseq` | every sequence in a sequentially compact space has a convergent subsequence | general compactness interface, not boundedness itself |

For the conventional real candidate, one may instantiate `s := Set.range x` and use range
membership for every term, then discard the additional proof that the limit lies in
`closure (Set.range x)`. That route has not been credited as the root: statement selection,
elaborated identity, checked specialization, proof provenance, trust, and composition belong to
later phases.

`IntakeProbe.lean` authenticates the displayed pinned interfaces and prints axiom reports for the
two direct declarations. Passing that probe supports API discovery only.

## Duplicate-name boundary

`Docs/researches/math_theorems.md:4594-4599` contains a second target with the same Chinese name,
`THM-M-0619`, whose gloss is `紧度量空间序列有收敛子列` (a sequence in a compact metric space has
a convergent subsequence). This is not duplicate evidence for `THM-M-0264`. The real-analysis
bounded-sequence wording must retain its own source identity, statement fingerprint, obligation
registry, proof credit, and receipts.

## Open gates

Before H0, reviewers must admit and hash a primary edition, pinpoint the exact proposition and
incorporated definitions, map every assumption and proof transition, resolve attribution and date,
audit translations and errata, and independently approve the result. Before statement acceptance,
Lean work must freeze exact binders, minimal imports, expression and environment fingerprints,
checked alternate encodings or specializations, and the required hypothesis, domain, binder-scope,
and boundary mutations. Exhaustive candidate, proof-body, dependency, axiom, placeholder, and trust
audits remain later work.
