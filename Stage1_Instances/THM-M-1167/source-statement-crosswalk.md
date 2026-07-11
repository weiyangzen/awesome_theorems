# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` records only the title "Schauder estimates", attribution to
Juliusz Schauder, year 1934, statement "Holder continuity estimates", importance "high", and the
untrusted status `已验证`. `Docs/Stage0_Blueprint.md` repeats those fields while explicitly leaving
definitions, hypotheses, proof, dependencies, axioms, and machine artifacts open. No bibliography,
edition, theorem number, page, translation, or errata record is supplied.

Accordingly, no primary-source theorem is asserted at intake. The named family contains
inequivalent interior, boundary, elliptic, and parabolic estimates with materially different
hypotheses and conclusions. Selecting one now would substitute mathematics not present in the
source record, so the exact-statement gate remains blocked.

## Crosswalk

| Source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "Schauder estimates" | a regularity-estimate family | one concrete proposition | unresolved |
| "Holder continuity estimates" | Holder regularity/norms are involved | Holder-space definitions, exponents, norm inequality | unresolved |
| PDE category | differential/PDE context | operator, domain, solution predicate, data | unresolved |
| Juliusz Schauder / 1934 | historical metadata | verified primary edition and theorem/page | unresolved |
| `已验证` | repository screening label | inspectable human proof and kernel receipt | no credit |

## Statement boundary

The canonical formal target, module, binders, hypotheses, conclusion, universes, alternate
encodings, expression hash, and environment fingerprint are intentionally unset. The next phase
must first identify and verify a primary theorem, then map every source assumption to an exact Lean
field or binder. Only after that mapping may it elaborate a target or search for proof credit.

The first downstream gate is primary-source identification and independent verification of its
edition, theorem/page, definitions, assumptions, conclusion, and errata. Until then the source debt
is `H4`, the machine debt is `M4`, and readable reconstruction debt is `R4`.
