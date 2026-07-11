# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies the title "位势的跳跃关系", the statement "位势在边界上的
行为", nineteenth-century dating, attribution to multiple mathematicians, and the label `已验证`.
`Docs/Stage0_Blueprint.md` repeats these fields while leaving definitions, assumptions, proof,
axioms, references, and machine status open. Neither record provides a bibliography, edition,
theorem number, page, or errata information. They are repository metadata, not a primary source.

No primary-source candidate is asserted at intake. Several inequivalent theorems fit the wording,
so selecting one now would invent mathematics rather than preserve the source claim.

## Crosswalk

| Source element | Information fixed | Information still required | Intake result |
|---|---|---|---|
| "potential" | potential theory is intended | layer/type, kernel, normalization, density | unresolved |
| "boundary" | traces at a boundary matter | domain, regularity, orientation, trace notion | unresolved |
| "behavior" | some limiting property | exact equality, topology, pointwise/a.e. scope | unresolved |
| "jump relations" | two traces or related boundary quantities differ | sides, signs, coefficient, principal value term | unresolved |
| nineteenth century / multiple authors | broad historical family | identifiable primary theorem | insufficient |
| `已验证` | untrusted screening label | human proof and kernel receipts | no credit |

## Lean boundary

The manifest assigns no accepted legacy slot, and no target-specific Lean declaration was found.
The later statement gate must first identify the human theorem, then elaborate its exact ordered
binders and hypotheses with minimal pinned imports. Until that occurs there is no expression hash,
checked alternate encoding, mutation suite, or machine proof to credit.

The first downstream gate is primary-source identification with edition, theorem/page, assumptions,
definitions, sign conventions, and errata, followed by an independently reviewable row-by-row map
to the canonical Lean target.

