# Source-statement crosswalk

## Available record and source boundary

The repository inventory supplies the Chinese title, the names Kazimierz Kuratowski and Max Zorn,
the year `1922`, and only the phrase "existence of a maximal element in a partially ordered set".
It supplies no bibliography, theorem number, page, hypotheses, definitions, proof, or errata record.
Its `已验证` label is untrusted under rev-5.6.

No primary source is asserted at intake. The later source audit must inspect immutable scans or
stable editions for the historically intended Kuratowski and/or Zorn formulation, record exact
bibliographic and theorem/page anchors, and reconcile the date and attribution. A modern textbook
may clarify terminology but cannot silently replace the historical source boundary.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "partially ordered set" | carrier with reflexive, antisymmetric, transitive order | universe and `[PartialOrder alpha]` | domain family identified; exact binders open |
| omitted premise | every chain admits an upper bound | `forall c : Set alpha, IsChain (fun x y => x <= y) c -> BddAbove c` or source-equivalent | essential hypothesis missing from repository wording |
| "existence" | existential conclusion, normally nonconstructive | `Exists` plus frozen choice/foundation profile | included provisionally; foundation open |
| "maximal element" | no distinct strictly larger element | `IsMax m` or a checked equivalent | included; must not become greatest element |
| Kuratowski / Zorn / 1922 | historical locator | no Lean proof component | exact source and attribution unresolved |

## Machine-discovery boundary

A scoped repository search found no theorem-specific legacy module for `THM-M-0774`. The canonical
pinned mathlib tree contains `Mathlib/Order/Zorn.lean`, including `zorn_le`, whose source type is a
close match to the provisional whole-poset form. This is discovery evidence, not an anchor audit:
the declaration has not been selected as the canonical target, its elaborated expression and trust
closure have not been recorded, and it receives no `M0` credit here.

Before `H0`, an independent reviewer must approve the exact source edition, statement, all
assumptions, definitions, attribution, and errata. Before statement credit, the approved source
components must be mapped row by row to an elaborated Lean expression, with checked transports for
any alternate chain or maximality encoding.
