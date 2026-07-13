# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:4594-4599` records the Chinese title
`波尔查诺-魏尔斯特拉斯定理`, attribution Bernard Bolzano/Karl Weierstrass, year 1817, gloss
`紧度量空间序列有收敛子列`, high importance, and status `已验证`. Git blame places all six
uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record supplies no
edition, theorem/page, formula, proof passage, incorporated definitions, translation, correction or
errata record, independent reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:16936-16961` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent formulations, axioms, machine state, and
artifact links open. The manifest keeps `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

The theorem family is identifiable, but the catalog does not name a work, edition, or other source,
so even the rev-5.6 `H1` minimum evidence is absent and the human axis remains `unclassified`.
H1 first requires a named source plus this unresolved mapping ledger. H0 additionally requires an
immutable primary edition, pinpoint statement and proof locators, a complete definition/premise/
conclusion and dependent-node crosswalk, translation and errata review, and an identified
independent reviewer.

## Literal component crosswalk

| Catalog component | Mathematical decision required | Pinned Lean lead | Intake result |
|---|---|---|---|
| `紧度量空间` (compact metric space) | compact carrier or compact subset; metric or pseudometric conventions | `[CompactSpace X]` with first-countability; or `IsCompact s` | close candidates; source identity open |
| `序列` (sequence) | carrier, universe, index, and binder order | `x : Nat -> X` | conventional candidate only |
| `子列` (subsequence) | order-preserving selector and sample encoding | `phi : Nat -> Nat`, `StrictMono phi`, `x \circ phi` | direct API match; source encoding open |
| `收敛` (convergent) | topology, existential limit, and set membership | `Tendsto (x \circ phi) atTop (nhds a)` | direct API match; exact conclusion open |
| Bernard Bolzano/Karl Weierstrass; 1817 | primary work, attribution, date, and version | no Lean identity follows | uncited metadata lead only |
| `已验证` | accepted source and kernel evidence | accepted receipts | no credit |

A conventional candidate root is: for every compact metric type `X` and every `x : Nat -> X`,
there are `a : X` and a strictly increasing `phi : Nat -> Nat` such that `x \circ phi` converges to
`a`. This is a resolution target, not a source quotation or frozen canonical statement.

## Pinned Lean candidate crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Topology.Sequences` contains the following discovery candidates.

| Declaration | Exact-topic role | Identity boundary |
|---|---|---|
| `CompactSpace.tendsto_subseq` | every sequence in a compact first-countable carrier has a convergent strictly indexed subsequence | likely compact-metric specialization; library statement is broader than the metric wording |
| `IsCompact.tendsto_subseq` | every sequence contained in a compact first-countable set has a convergent subsequence with its limit in the set | likely set-form alternate; adds a set and membership binders |
| `SeqCompactSpace.tendsto_subseq` | direct extraction from a sequential-compactness typeclass | assumes the conclusion family rather than encoding received compact metric scope |
| `isCompact_iff_isSeqCompact` | compactness equals sequential compactness in a pseudometrizable space | bridge candidate, not the extraction root alone |
| `compactSpace_iff_seqCompactSpace` | carrier-level compact/sequential-compact equivalence | bridge candidate, not the extraction root alone |

`IntakeProbe.lean` checks these exact declarations and prints representative axiom reports. Passing
the probe establishes pinned API availability only. It does not select a candidate, prove a checked
source relationship, audit the terminal proof body and transitive dependencies, or satisfy the
later anchor-audit and validation phases.

## Duplicate-name boundary

`Docs/researches/math_theorems.md:1901-1906` contains `THM-M-0264` with the same Chinese title but
the distinct bounded-sequence gloss `有界数列必有收敛子列` in the real-analysis category; that
record does not fix the carrier as `Real`. The two targets retain separate source
identity, statement fingerprints, obligations, proof credit, and receipts. Proper-space bounded
extraction cannot silently replace this compact-metric target, nor can this target donate status to
the bounded-sequence target.

## Open gates

Before statement acceptance, reviewers must admit and pin the source, decide carrier versus subset,
freeze all domains, binders, assumptions, conclusion and boundary cases, elaborate the exact Lean
expression with minimal imports, fingerprint the expression and environment, compile checked
transports for credited alternates, and run hypothesis/domain/scope/boundary mutations. Exhaustive
candidate, proof-body, dependency, placeholder, axiom, provenance, trust, and source audits remain
downstream.
